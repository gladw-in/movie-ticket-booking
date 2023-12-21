"""Keeps track of one customer's booking: movie, theatre, time, seats and food."""

from dataclasses import dataclass, field

from .cart import Cart
from .catalog import Movie
from .seating import SeatSelection, Theatre

SHOWTIMES = ("Morning", "Evening", "Second")


class BookingError(Exception):
    pass


@dataclass(frozen=True)
class Ticket:
    seat: str
    tier: str
    price: int


@dataclass
class BookingSession:
    username: str
    movie: Movie | None = None
    theatre: Theatre | None = None
    showtime: str | None = None
    seats: SeatSelection | None = None
    cart: Cart = field(default_factory=Cart)

    def choose_theatre(self, theatre):
        self.theatre = theatre
        self.seats = SeatSelection(theatre)
        self.showtime = None

    def choose_showtime(self, showtime):
        if showtime not in SHOWTIMES:
            raise ValueError(f"Unknown showtime: {showtime}")
        self.showtime = showtime

    def require_ready_for_food(self):
        if self.showtime is None:
            raise BookingError("Please select a time.")
        if self.seats is None or len(self.seats) == 0:
            raise BookingError("Please select at least one seat.")

    def tickets(self):
        if self.theatre is None or self.seats is None:
            return []
        return [
            Ticket(seat, self.theatre.tier(seat), self.theatre.price(seat))
            for seat in self.seats
        ]

    @property
    def ticket_total(self):
        return sum(ticket.price for ticket in self.tickets())

    @property
    def food_total(self):
        return self.cart.total

    @property
    def grand_total(self):
        return self.ticket_total + self.food_total
