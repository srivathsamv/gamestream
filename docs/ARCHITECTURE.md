# Architecture & Design Notes

## Data flow

1. **Offline, once:** pull historical match events from StatsBomb open data
   (`gamestream/ingestion/`). Cache to `data/raw/` so this only needs to run
   once, not on every app start.

2. **Offline, once (per model stage):** train/build the positioning model
   (`gamestream/positioning/`) on the cached historical events.
   - Stage 1: a lookup table — group by `(position_role, game_phase,
     attacking)`, store mean `(x, y)` per bucket.
   - Stage 2: a k-NN or small regressor over continuous features (minute,
     score differential, ...) instead of rigid buckets.

3. **On app start, per match:** load the two teams' 22-player rosters into
   the cache (`gamestream/cache/`) so position lookups during replay don't
   hit disk or re-parse anything.

4. **During replay:** read the next line of the commentary transcript
   (`gamestream/replay/`), pass it to the NLP parser
   (`gamestream/nlp/`), which extracts `{player_x, player_y, action}` if the
   line matches the known action vocabulary (skip it if it doesn't — see
   "NLP scope" below).

5. **Per parsed event:** look up (or predict) `(x, y)` for both players
   from the positioning model + roster cache, then hand
   `{player_x, pos_x, player_y, pos_y, action}` to the renderer
   (`gamestream/rendering/`), which draws both players and a curved arrow
   between them on the pitch.

6. **Loop** until the transcript is exhausted, with a timed delay between
   lines to simulate "live."

## Open design questions (decide these as you build, don't let them block starting)

- **Phase buckets:** what minute ranges make sense? A reasonable starting
  point (reused from an earlier project): early minutes, closing out the
  first half, half-time, build-up phase, tension time, late game. Tune
  these against how sparse/dense your cached data actually is per bucket —
  if a bucket has too few events, the mean position is noise, not signal.

- **Action vocabulary:** keep this short and fixed for v1 — e.g. pass,
  cross, shot, tackle, interception, save. Every commentary phrasing that
  doesn't cleanly map to one of these gets skipped, not force-fit. Resist
  the urge to keep adding regex patterns to chase 100% coverage — that's
  the scope trap for this project (see conversation history / mentor
  notes if you have them).

- **Lookup table vs. k-NN:** build the lookup table first. It's the
  fastest path to an end-to-end working pipeline and de-risks everything
  downstream (NLP, caching, rendering) against a known-good data source.
  Swap in k-NN once the plumbing already works, not before. Be ready to
  explain *why* k-NN over another model if you go there — that's a
  legitimate interview question, not a formality.

- **Deterministic mean vs. sampled position:** a pure mean position will
  make every "CAM, build phase, attacking" query return the *identical*
  point — heatmaps built from that will look artificially tight. Consider
  storing variance/spread per bucket (or, with k-NN, the spread of the k
  neighbors) and sampling instead of returning the mean directly.

- **Where "authentic" ends:** the rendered position is a *typical* position
  for that role/phase/state, not this player's actual position in this
  match. State that plainly in the UI or README — it's the difference
  between a defensible claim and an overclaim.

## Why not scrape a live commentary feed?

ESPN (and most live-text-commentary sources) prohibit scraping in their
Terms of Service, and the underlying data is usually licensed from a
provider like Opta rather than owned by the site showing it. "Mock" live
replay — reading a manually-saved, one-time transcript with a timed delay
— gets the same demo experience without an ongoing-scraper legal question.
If you want a genuinely live version later, that needs its own research
pass into a legitimately licensed or free real-time source first.
