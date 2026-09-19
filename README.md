# GameStream

A "mock live" football match visualizer. Given a commentary transcript, GameStream
replays it line by line, parses each event with a small NLP layer, predicts where
the two players involved were most likely standing (trained on real historical
positioning data), and renders it on a pitch — approximating a live match feed
without needing real-time tracking data.

This is **not** a replay of a real match's actual player positions. It's a
model of *typical* positioning for a role/phase/game-state, driven by real
commentary text. That distinction matters and should stay explicit anywhere
this project is described (README, demo, resume bullet).

## Why this exists

Built as a from-scratch revamp of an earlier project (JGaffer). Two decisions
shaped this design directly:

1. **Free tracking data doesn't cover current/major European leagues at
   the depth this project wants**, and StatsBomb's open event data has
   unreliable pass-recipient inference — a real problem for building a
   *passing network* directly off it. Sidestepping that: this project
   doesn't need recipient-linked passes. It only needs `(role, phase,
   attacking) -> typical (x, y)`, which StatsBomb's open data supports
   cleanly since every event carries a position label and a location.
2. **Live commentary has no coordinates.** Rather than approximating
   locations from vague text ("down the left wing"), positions are
   *predicted* from a model trained on real historical data, and the
   text is only used to decide *which two predicted positions to connect
   and how* (pass, cross, shot, tackle...).

## Architecture

```
StatsBomb open data (historical events, many matches)
        |
        v
 positioning model  --- Stage 1: lookup table (role, phase, attacking) -> mean pos
   (gamestream/          Stage 2: k-NN / regressor over continuous features
    positioning/)             (minute, score_diff, ...) -> predicted pos
        |
        v
   roster cache  <-------- team/player lookup (avoid re-fetch latency)
 (gamestream/cache/)
        |
        v
commentary transcript --> NLP parser --> {player_x, player_y, action}
 (mock "live" replay,      (gamestream/       |
  gamestream/replay/)       nlp/)             v
                                        pitch renderer
                                     (gamestream/rendering/)
                                              |
                                              v
                                        Streamlit app (app/)
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full data flow and
open design questions.

## Roadmap

**Must-have (v1):**
- [ ] Stage 1 positioning model: lookup table, `(role, phase, attacking) -> (x, y)`
- [ ] Roster cache for team/player data (avoid re-fetch latency)
- [ ] Rule-based NLP parser over a small, fixed action vocabulary
- [ ] Mock-live replay: read a static transcript, render with a timed delay
- [ ] Pitch rendering: player dots + a curved arrow for the current event

**Stretch (v2):**
- [ ] Stage 2 positioning model: k-NN or small regressor over continuous features
- [ ] Variance/spread sampling instead of deterministic mean position
- [ ] Match contribution / player ranking system
- [ ] Broader NLP coverage beyond the fixed action vocabulary

## Setup

```bash
python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Pull and cache historical StatsBomb data (see
`gamestream/ingestion/statsbomb_loader.py` — not yet implemented, that's the
first thing to build):

```bash
python -m gamestream.ingestion.statsbomb_loader
```

Run the app:

```bash
streamlit run app/streamlit_app.py
```

## Data attribution

Historical positioning data comes from
[StatsBomb's open data](https://github.com/statsbomb/open-data), used here
for research/personal-project purposes under their public data user
agreement (CC BY-NC-SA 4.0 — non-commercial, share-alike, attribution
required). See `data/README.md` before adding any new data source.

The commentary transcript in `data_samples/` is a hand-written, original
example for testing the NLP parser locally — **not** scraped from any live
feed. Any real transcript you use for demos should be grabbed manually,
once, for personal non-commercial use — not via an ongoing scraper. See
`docs/ARCHITECTURE.md` for why.

## Project structure

```
gamestream/
  config.py              constants: action vocabulary, phase buckets
  ingestion/              pulling + caching StatsBomb historical data
  positioning/            Stage 1 lookup model, Stage 2 k-NN model, phase bucketing
  cache/                  team/player roster cache
  nlp/                    commentary line -> structured event
  rendering/              pitch + dot + arrow rendering
  replay/                 mock-live transcript playback loop
app/
  streamlit_app.py        thin UI wiring the pieces together
tests/                    unit tests
docs/
  ARCHITECTURE.md         full design notes and open questions
data/                     cached StatsBomb data (gitignored — see data/README.md)
data_samples/             small, original, hand-written test fixtures
```
