from gamestream.positioning.phases import get_game_phase


def test_early_minutes():
    assert get_game_phase(10) == "EARLY_MINUTES"


def test_bucket_boundary_is_inclusive():
    assert get_game_phase(15) == "EARLY_MINUTES"
    assert get_game_phase(16) == "CLOSING_HALF"


def test_late_game():
    assert get_game_phase(88) == "LATE_GAME"


def test_extra_time_collapses_into_last_bucket():
    assert get_game_phase(95) == "LATE_GAME"
