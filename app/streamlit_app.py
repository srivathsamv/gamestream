"""GameStream — thin Streamlit UI.

Wires together the replay engine and renderer. Deliberately thin: this app
should not contain positioning-model, NLP, or rendering logic itself — it
just drives gamestream.replay and displays what gamestream.rendering
produces.

Run with: streamlit run app/streamlit_app.py

TODO:
  - Let the user pick/upload a transcript (default to
    data_samples/sample_commentary.txt for now).
  - Load the roster cache for the chosen match before starting replay.
  - Iterate gamestream.replay.mock_live_engine.replay(...), rendering each
    yielded event with gamestream.rendering.pitch_renderer.render_frame
    via st.pyplot(fig).
  - Decide how to show playback controls (start/pause, speed) once the
    core loop works — don't build this before the pipeline underneath it
    is real.
"""

import streamlit as st

st.set_page_config(page_title="GameStream", layout="centered")
st.title("GameStream")
st.caption(
    "Mock live match visualizer — predicted positioning, not real tracking data."
)

st.info(
    "Pipeline not wired up yet. See TODOs in this file and in "
    "gamestream/positioning, gamestream/nlp, and gamestream/rendering."
)
