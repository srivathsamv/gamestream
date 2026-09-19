"""Pitch rendering: draw the current frame — both players' predicted
positions plus a curved arrow for the event connecting them.

mplsoccer's Pitch class handles the pitch outline; the pitch setup below is
implemented since it's boilerplate. The actual per-frame drawing (dots,
labeling, curved arrow direction/style, how this gets wired into the
Streamlit app for the "mock live" feel) is the design-bearing part — see
docs/ARCHITECTURE.md for the intended data flow.
"""

from mplsoccer import Pitch


def new_pitch():
    """Return a fresh (Pitch, matplotlib Figure, Axes) ready to draw on."""
    pitch = Pitch(pitch_type="statsbomb", pitch_color="grass", line_color="white")
    fig, ax = pitch.draw(figsize=(8, 5.2))
    return pitch, fig, ax


def render_frame(event: dict):
    """Draw one frame: both players' positions and a curved arrow for the
    event between them.

    Args:
        event: the structured output of
            gamestream.nlp.commentary_parser.parse_commentary_line, with
            predicted (x, y) for both players already attached (from the
            positioning model + roster cache).

    Returns:
        The matplotlib Figure for this frame — Streamlit can render this
        directly with st.pyplot(fig).

    TODO:
      - Plot both players as dots (pitch.scatter).
      - Draw a curved arrow between them (pitch.arrows, or
        matplotlib.patches.FancyArrowPatch with a curvature for a more
        "cross"-like arc vs. a straight "pass" line — consider varying
        arrow style by event["action"]).
      - Decide on player labeling (name next to the dot?).
    """
    raise NotImplementedError("TODO: implement per-frame rendering")
