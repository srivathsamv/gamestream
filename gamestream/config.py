"""Shared constants for GameStream.

Keep this the single source of truth for the action vocabulary and phase
buckets — the NLP parser, positioning model, and renderer should all import
from here rather than hardcoding their own copies.
"""

# Fixed, small action vocabulary for v1. Every commentary line that doesn't
# map cleanly to one of these gets skipped by the NLP parser rather than
# force-fit. Extend this deliberately, not reactively — see
# docs/ARCHITECTURE.md ("NLP scope") before adding entries.
ACTION_VOCAB = [
    "pass",
    "cross",
    "shot",
    "tackle",
    "interception",
    "save",
]

# Game-phase buckets used by the Stage 1 lookup model, keyed by the upper
# bound (inclusive) of the minute range. Adjust these based on how sparse
# your cached historical data actually is per bucket once you've pulled it —
# a bucket with too few events makes for a noisy mean position.
GAME_PHASES = {
    15: "EARLY_MINUTES",
    44: "CLOSING_HALF",
    50: "HALF_TIME",
    60: "BUILD_PHASE",
    70: "TENSION_TIME",
    90: "LATE_GAME",
}
