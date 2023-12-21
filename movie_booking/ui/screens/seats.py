"""Screen to choose a showtime and seats."""

import tkinter as tk
from tkinter import messagebox

from ...booking import SHOWTIMES, BookingError
from ...seating import PREMIUM_PRICE, STANDARD_PRICE
from .. import theme
from ..base import Screen


class SeatsScreen(Screen):
    title = "Choose your seats"

    def build(self):
        self.theatre = self.session.theatre
        self.seat_buttons = {}
        self.time_buttons = {}

        self._header()
        self._legend()
        self._grid()
        self._footer()
        self.refresh()

    def _header(self):
        bar = tk.Frame(self, bg=theme.BG)
        bar.pack(pady=(10, 4))
        theme.label(
            bar,
            f"{self.session.movie.title}  @  {self.theatre.name}",
            font=theme.FONT_BOLD,
        ).grid(row=0, column=0, columnspan=4, pady=(0, 6))
        theme.label(bar, "Timing:", fg=theme.GREEN, font=theme.FONT_BOLD).grid(
            row=1, column=0, padx=4
        )
        for column, name in enumerate(SHOWTIMES, start=1):
            button = theme.button(
                bar,
                name,
                lambda n=name: self.pick_time(n),
                width=9,
                fg=theme.GREEN,
                font=theme.FONT_BOLD,
            )
            button.grid(row=1, column=column, padx=3)
            self.time_buttons[name] = button

    def _legend(self):
        bar = tk.Frame(self, bg=theme.BG)
        bar.pack(pady=4)
        theme.label(
            bar, f"{self.theatre.premium_name}: Rs {PREMIUM_PRICE}", fg=theme.GOLD
        ).grid(row=0, column=0, padx=8)
        theme.label(bar, f"Normal: Rs {STANDARD_PRICE}").grid(row=0, column=1, padx=8)
        theme.label(bar, "Selected", fg=theme.GREEN).grid(row=0, column=2, padx=8)

    def _grid(self):
        hall = tk.Frame(self, bg=theme.BG)
        hall.pack(padx=12, pady=4)
        for seat_row in self.theatre.rows:
            line = tk.Frame(hall, bg=theme.BG)
            line.pack(pady=(0, 10) if seat_row.label == "A" else 0)
            tk.Button(
                line,
                text=seat_row.label,
                state=tk.DISABLED,
                bg=theme.BG,
                fg=theme.FG,
                disabledforeground=theme.FG,
                width=2,
            ).pack(side=tk.LEFT, padx=(0, 6))
            for number in seat_row.seats:
                seat = f"{seat_row.label}{number}"
                premium = self.theatre.is_premium(seat)
                button = theme.button(
                    line,
                    str(number),
                    lambda s=seat: self.toggle(s),
                    width=2,
                    height=1,
                    fg=theme.GOLD if premium else theme.FG,
                )
                button.pack(side=tk.LEFT)
                self.seat_buttons[seat] = button
                if seat_row.gap_after == number:
                    self._gap(line)

    def _gap(self, line):
        if self.theatre.gap_label:
            theme.button(
                line,
                self.theatre.gap_label,
                state=tk.DISABLED,
                disabledforeground="gray",
                width=8,
                relief=tk.FLAT,
            ).pack(side=tk.LEFT)
        else:
            tk.Frame(line, bg=theme.BG, width=28).pack(side=tk.LEFT)

    def _footer(self):
        tk.Label(self, text="screen", bg="gray", width=60, pady=2).pack(pady=(14, 4))
        self.summary = theme.label(self, "")
        self.summary.pack()
        row = tk.Frame(self, bg=theme.BG)
        row.pack(pady=(4, 12))
        theme.button(row, "Back", lambda: self.app.go("theatre"), width=10).grid(
            row=0, column=0, padx=6
        )
        theme.primary_button(row, "Proceed to payment", self.proceed, width=30).grid(
            row=0, column=1, padx=6
        )

    def toggle(self, seat):
        self.session.seats.toggle(seat)
        self.refresh()

    def pick_time(self, name):
        self.session.choose_showtime(name)
        self.refresh()

    def refresh(self):
        for seat, button in self.seat_buttons.items():
            button.config(bg=theme.GREEN if seat in self.session.seats else theme.BG)
        for name, button in self.time_buttons.items():
            chosen = name == self.session.showtime
            button.config(
                bg=theme.GREEN if chosen else theme.BG,
                fg=theme.FG if chosen else theme.GREEN,
            )
        count = len(self.session.seats)
        self.summary.config(
            text=f"{count} seat{'s' if count != 1 else ''} selected  -  Rs {self.session.seats.total}"
        )

    def proceed(self):
        try:
            self.session.require_ready_for_food()
        except BookingError as exc:
            messagebox.showinfo("Almost there", str(exc), parent=self)
            return
        self.app.go("food_prompt")
