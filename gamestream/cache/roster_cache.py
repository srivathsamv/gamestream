"""Team/player roster cache — avoids re-fetching lineup data on every
commentary line during replay.

A minimal in-memory version is implemented below to unblock building the
rest of the pipeline (this is standard caching boilerplate, not a design
decision worth agonizing over). Swap in SQLite or Redis later if an
in-memory dict stops being enough — that's a mechanical swap, not a
redesign, as long as callers only use get()/set().
"""


class RosterCache:
    """Simple in-memory cache, keyed by match_id.

    TODO: decide what actually goes in the cached value — at minimum,
    each of the 22 players' role and a way to look up their predicted
    position (does the cache hold positions directly, or just roles, and
    positions get computed on demand via the positioning model?). That's
    a real design decision — the in-memory dict here is just the
    container, not the schema.
    """

    def __init__(self):
        self._store: dict[str, dict] = {}

    def set(self, match_id: str, roster_data: dict) -> None:
        self._store[match_id] = roster_data

    def get(self, match_id: str) -> dict | None:
        return self._store.get(match_id)

    def has(self, match_id: str) -> bool:
        return match_id in self._store
