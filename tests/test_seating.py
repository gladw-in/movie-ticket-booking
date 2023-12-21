"""Tests for seat layouts, prices and seat selection."""

import pytest

from movie_booking.seating import (
    INOX,
    PVR,
    PREMIUM_PRICE,
    STANDARD_PRICE,
    SeatSelection,
)


def test_layout_sizes_match_the_original_theatres():
    assert INOX.capacity == 13 * 12
    assert PVR.capacity == 15 + 11 * 17


def test_row_a_is_premium_everything_else_is_standard():
    for theatre in (INOX, PVR):
        assert theatre.price("A1") == PREMIUM_PRICE == 250
        assert theatre.price("B1") == STANDARD_PRICE == 200
        assert theatre.tier("A1") == theatre.premium_name
        assert theatre.tier("C3") == "Normal"


def test_seats_that_do_not_exist_are_rejected():
    assert INOX.has_seat("M12") and not INOX.has_seat("M13") and not INOX.has_seat("N1")
    assert PVR.has_seat("L17") and not PVR.has_seat("A16")
    with pytest.raises(KeyError):
        INOX.price("Z99")


def test_gap_positions():
    assert {r.gap_after for r in INOX.rows} == {6}
    assert PVR.rows[0].gap_after is None and PVR.rows[1].gap_after == 14


def test_toggle_selects_then_deselects():
    selection = SeatSelection(INOX)
    assert selection.toggle("A1") is True and "A1" in selection
    assert selection.toggle("A1") is False and "A1" not in selection
    assert len(selection) == 0


def test_selection_is_ordered_and_totalled():
    selection = SeatSelection(PVR)
    for seat in ["B10", "A2", "B2", "A15"]:
        selection.toggle(seat)
    assert list(selection) == ["A2", "A15", "B2", "B10"]
    assert selection.total == 250 + 250 + 200 + 200


def test_cannot_select_a_seat_outside_the_layout():
    with pytest.raises(KeyError):
        SeatSelection(INOX).toggle("A13")


def test_selections_are_independent():
    a, b = SeatSelection(INOX), SeatSelection(INOX)
    a.toggle("A1")
    assert len(b) == 0
