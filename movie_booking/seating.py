"""Describes theatre seat layouts, seat prices and the seats a customer picks."""

from dataclasses import dataclass
from functools import cached_property

PREMIUM_ROW = "A"
PREMIUM_PRICE = 250
STANDARD_PRICE = 200


@dataclass(frozen=True)
class SeatRow:
    label: str
    seats: tuple[int, ...]
    gap_after: int | None = None


@dataclass(frozen=True)
class Theatre:
    name: str
    premium_name: str
    rows: tuple[SeatRow, ...]
    gap_label: str = ""

    @cached_property
    def _seat_ids(self):
        return frozenset(seat_id(row.label, n) for row in self.rows for n in row.seats)

    def has_seat(self, seat):
        return seat in self._seat_ids

    @property
    def capacity(self):
        return len(self._seat_ids)

    def is_premium(self, seat):
        return seat.startswith(PREMIUM_ROW)

    def price(self, seat):
        if not self.has_seat(seat):
            raise KeyError(f"No such seat in {self.name}: {seat}")
        return PREMIUM_PRICE if self.is_premium(seat) else STANDARD_PRICE

    def tier(self, seat):
        return self.premium_name if self.is_premium(seat) else "Normal"


def seat_id(row, number):
    return f"{row}{number}"


def _rows(labels, seats, gap_after):
    return tuple(SeatRow(label, tuple(seats), gap_after) for label in labels)


INOX = Theatre(
    name="INOX",
    premium_name="Exclusive",
    gap_label="stairs",
    rows=_rows("A", range(1, 13), 6) + _rows("BCDEFGHIJKLM", range(1, 13), 6),
)

PVR = Theatre(
    name="PVR",
    premium_name="Royal",
    rows=_rows("A", range(1, 16), None) + _rows("BCDEFGHIJKL", range(1, 18), 14),
)

THEATRES = (INOX, PVR)


class SeatSelection:
    def __init__(self, theatre):
        self.theatre = theatre
        self._chosen = set()

    def toggle(self, seat):
        if not self.theatre.has_seat(seat):
            raise KeyError(f"No such seat in {self.theatre.name}: {seat}")
        if seat in self._chosen:
            self._chosen.remove(seat)
            return False
        self._chosen.add(seat)
        return True

    def clear(self):
        self._chosen.clear()

    @staticmethod
    def _sort_key(seat):
        return seat[0], int(seat[1:])

    def __iter__(self):
        return iter(sorted(self._chosen, key=self._sort_key))

    def __len__(self):
        return len(self._chosen)

    def __contains__(self, seat):
        return seat in self._chosen

    @property
    def total(self):
        return sum(self.theatre.price(seat) for seat in self._chosen)
