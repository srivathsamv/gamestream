"""Stage 2 positioning model: k-NN (or a small regressor) over continuous
features, instead of rigid (role, phase, attacking) buckets.

Stretch goal — build this *after* lookup_model.py is working end-to-end
through the full pipeline (NLP -> cache -> render). Swapping this in later
should mean changing what gamestream.positioning exposes as its "current
model," not rewriting anything downstream.

Before starting this: be ready to explain why k-NN specifically (vs. a
small MLP, vs. linear regression) — that's a legitimate interview
question, not just an implementation detail. The honest answer is usually
something like "positions don't cluster cleanly into discrete buckets, and
k-NN's neighbor spread also gives me a natural way to sample instead of
returning a single deterministic point" — but confirm that's actually true
of your data before claiming it.

TODO:
  - Feature set: role (encoded), minute (continuous, not bucketed),
    attacking flag, score differential, maybe opponent strength.
  - Train/test split — some way to sanity-check predictions aren't
    nonsensical (e.g. a center back predicted at the opponent's byline).
  - Decide how predictions get consumed: a single point, or a sample
    drawn from the neighbor spread (ties into the "deterministic mean"
    weakness noted in lookup_model.py and docs/ARCHITECTURE.md).
"""

import pandas as pd


def train_model(events: pd.DataFrame):
    """Fit the Stage 2 positioning model on historical events."""
    raise NotImplementedError("TODO: Stage 2 — build after Stage 1 works")


def predict_position(model, role: str, minute: int, attacking: bool, **kwargs):
    """Predict a position from continuous features rather than buckets."""
    raise NotImplementedError("TODO: Stage 2 — build after Stage 1 works")
