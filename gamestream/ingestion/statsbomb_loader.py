"""Pull and cache historical StatsBomb open-data events.

This is the first thing to build — everything else depends on having
event data on disk in data/raw/.

Use the `statsbombpy` package rather than hand-parsing the raw JSON —
`sb.events(match_id=...)` returns a clean pandas DataFrame directly. Don't
re-implement StatsBomb's JSON parsing by hand; that problem is already
solved.

TODO:
  - Pick a competition/season (StatsBomb's open-data competitions.json
    lists what's available — statsbombpy exposes this via sb.competitions()).
    Keep the initial scope narrow (a handful of matches from one
    competition) rather than pulling everything.
  - Pull events for the chosen matches, keep the columns the positioning
    model actually needs (position/role, minute, location, a way to
    derive the "attacking" flag — e.g. does the event's team currently
    have possession moving toward goal).
  - Cache to data/raw/ (parquet or CSV) so this doesn't need to re-run
    on every app start — see data/README.md for the expected layout.
"""

import pandas as pd


def load_events(competition_id: int, season_id: int) -> pd.DataFrame:
    """Pull and return event data for a competition/season.

    Should cache to data/raw/ and read from the cache on subsequent calls
    rather than re-pulling every time.
    """
    raise NotImplementedError("TODO: implement using statsbombpy")


if __name__ == "__main__":
    # TODO: wire this up to actually pull your chosen competition/season
    # once load_events() is implemented, so `python -m
    # gamestream.ingestion.statsbomb_loader` populates data/raw/ end to end.
    pass
