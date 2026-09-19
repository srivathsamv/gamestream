"""Mock-live replay: read a static commentary transcript and step through
it with a timed delay, to simulate a live feed without any ongoing
scraping (see docs/ARCHITECTURE.md — "Why not scrape a live commentary
feed?").

This is the easiest piece of the pipeline — a loop with a delay, not a
systems problem. Implemented as a generator here so the Streamlit app can
just iterate it; the actual parsing/positioning/rendering calls are left
as TODOs since those live in their own modules.
"""

import time
from collections.abc import Iterator

from gamestream.nlp.commentary_parser import parse_commentary_line


def load_transcript(path: str) -> list[str]:
    """Read a transcript file, one commentary line per non-comment,
    non-blank line."""
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    return [line for line in lines if line and not line.startswith("#")]


def replay(transcript_path: str, delay_seconds: float = 2.0) -> Iterator[dict]:
    """Yield parsed events one at a time, pausing delay_seconds between
    each to simulate a live feed. Lines that don't parse (see
    gamestream.nlp.commentary_parser) are skipped, not yielded.

    TODO once gamestream.nlp.commentary_parser and the positioning model
    are implemented: this should attach predicted (x, y) for both players
    before yielding, so the caller (Streamlit app) can pass the event
    straight to gamestream.rendering.render_frame without doing that
    wiring itself.
    """
    for line in load_transcript(transcript_path):
        event = parse_commentary_line(line)
        if event is None:
            continue
        yield event
        time.sleep(delay_seconds)
