"""Tests for the booking session and its totals."""

import pytest

from movie_booking.booking import SHOWTIMES, BookingError, BookingSession
from movie_booking.menu import all_items
from movie_booking.seating import INOX, PVR


def make_session():
    session = BookingSession("tanishk")
    session.choose_theatre(INOX)
    return session


def test_cannot_continue_without_a_time_or_seats():
    session = make_session()
    with pytest.raises(BookingError, match="time"):
        session.require_ready_for_food()
    session.choose_showtime("Morning")
    with pytest.raises(BookingError, match="seat"):
        session.require_ready_for_food()
    session.seats.toggle("B1")
    session.require_ready_for_food()


def test_unknown_showtime_is_rejected():
    with pytest.raises(ValueError):
        make_session().choose_showtime("Midnight")
    assert SHOWTIMES == ("Morning", "Evening", "Second")


def test_totals_combine_tickets_and_food_with_quantity():
    session = make_session()
    session.seats.toggle("A1")
    session.seats.toggle("C4")
    samosa = next(i for i in all_items() if i.name == "Samosa")
    session.cart.add(samosa, 2)
    assert session.ticket_total == 450
    assert session.food_total == 138
    assert session.grand_total == 588
    assert [(t.seat, t.tier, t.price) for t in session.tickets()] == [
        ("A1", "Exclusive", 250),
        ("C4", "Normal", 200),
    ]


def test_changing_theatre_discards_the_old_seats_and_time():
    session = make_session()
    session.choose_showtime("Evening")
    session.seats.toggle("A1")
    session.choose_theatre(PVR)
    assert len(session.seats) == 0 and session.showtime is None
    assert session.tickets() == []
    assert session.theatre is PVR and PVR.tier("A1") == "Royal"


def test_new_sessions_do_not_share_state():
    first, second = make_session(), make_session()
    first.seats.toggle("A1")
    assert len(second.seats) == 0 and second.cart is not first.cart
