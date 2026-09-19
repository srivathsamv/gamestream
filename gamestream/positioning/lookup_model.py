"""Stage 1 positioning model: a (role, phase, attacking) -> mean position
lookup table.

Build this first. It's the fastest path to an end-to-end working pipeline,
and everything downstream (NLP, caching, rendering) can be developed and
tested against it before Stage 2 (gamestream/positioning/knn_model.py)
exists at all.

TODO (this is the actual learning-bearing part — build it yourself):
  - Load cached historical events (see gamestream/ingestion/).
  - Group by (position_role, game_phase, attacking) using
    gamestream.positioning.phases.get_game_phase for the phase bucket.
  - Store mean (x, y) per bucket — and consider also storing variance/
    spread per bucket now, since a pure deterministic mean will make
    every prediction for the same bucket identical (flagged as a known
    weakness — see docs/ARCHITECTURE.md).
  - Decide what to do with buckets that have very few events (too sparse
    to trust the mean).
"""

import pandas as pd


def build_lookup_table(events: pd.DataFrame) -> dict:
    """Build the (role, phase, attacking) -> (x, y) lookup table.

    Args:
        events: historical event data, expected to have at least
            position/role, minute, attacking-flag, and x/y columns —
            exact column names depend on how gamestream.ingestion loads
            and shapes the StatsBomb data.

    Returns:
        A dict keyed by (role, phase, attacking) -> (x, y) tuple (or a
        richer value if you decide to store variance alongside the mean).
    """
    raise NotImplementedError("TODO: build the Stage 1 lookup table")


def predict_position(lookup: dict, role: str, phase: str, attacking: bool):
    """Look up a predicted position for a given role/phase/state.

    Should handle the case where the exact bucket isn't in the lookup
    table (decide: fall back to a coarser bucket? raise? return a default
    formation-slot position?) — that's a real design decision, not just
    an edge case to silence.
    """
    raise NotImplementedError("TODO: implement lookup + fallback behavior")
