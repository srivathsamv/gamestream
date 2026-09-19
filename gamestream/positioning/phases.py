"""Minute -> game-phase bucketing.

Pure, deterministic wiring around gamestream.config.GAME_PHASES — the
interesting design decision (where the bucket boundaries sit) lives in the
config, not here. Adjust GAME_PHASES once you've looked at how your cached
data is distributed per bucket.
"""

from gamestream.config import GAME_PHASES


def get_game_phase(minute: int) -> str:
    """Return the phase label for a given match minute.

    Extra time (minute > 90) collapses into the last defined bucket.
    """
    for upper_bound in sorted(GAME_PHASES):
        if minute <= upper_bound:
            return GAME_PHASES[upper_bound]
    return GAME_PHASES[max(GAME_PHASES)]
