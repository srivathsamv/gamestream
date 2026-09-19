"""Rule-based commentary line -> structured event parser.

This is the piece with the real open-endedness in this project — see
docs/ARCHITECTURE.md ("NLP scope") before starting. The guardrail: keep
ACTION_VOCAB (gamestream/config.py) small and fixed, and treat any line
that doesn't cleanly match as skip-not-crash. Chasing high coverage of
every possible commentary phrasing is the scope trap here — a working
parser that confidently handles 6 action types beats a fragile one that
half-handles twenty.

TODO:
  - Decide the matching approach for v1: keyword/regex rules are enough
    to start (e.g. "crosses to" -> action=cross). spaCy NER for player
    name extraction is a reasonable upgrade if regex name-matching against
    the roster cache gets unreliable.
  - Define the output shape this returns and keep it consistent with what
    gamestream.rendering expects to receive.
  - Handle: a line naming a player not in the current match's roster
    cache, a line matching no known action, ambiguous player names
    (partial match against multiple players).
"""

from gamestream.config import ACTION_VOCAB


def parse_commentary_line(line: str) -> dict | None:
    """Parse a single commentary line into a structured event, or None if
    it doesn't match the known action vocabulary.

    Expected return shape (finalize this as you build):
        {"player_x": str, "player_y": str, "action": str, "minute": int}
    """
    raise NotImplementedError(
        f"TODO: implement matching against ACTION_VOCAB={ACTION_VOCAB}"
    )
