"""Screen to review the order, pay and see the tickets."""

import tkinter as tk

from ...bank import format_money
from ..base import Screen
from .. import theme
from ..images import photo
from ..widgets import Notice, ScrollFrame
from ...paths import IMG_DIR

QR_PATH = IMG_DIR / "qrcode.png"


class CheckoutScreen(Screen):
    title = "Payment"
    size = (480, 640)

    def build(self):
        session = self.session

        tk.Label(
            self, text="PAYMENT", bg="white", fg="black", font=theme.FONT_TITLE, pady=8
        ).pack(fill=tk.X)

        area = ScrollFrame(self, width=440, height=260)
        area.pack(pady=8)
        body = area.body
        self._heading(
            body, f"{session.movie.title} - {session.theatre.name} - {session.showtime}"
        )
        for ticket in session.tickets():
            self._line(
                body, f"Seat {ticket.seat}  ({ticket.tier})", f"Rs {ticket.price}"
            )
        self._line(body, "Tickets", f"Rs {session.ticket_total}", bold=True)
        if not session.cart.is_empty:
            self._heading(body, "Food & drinks")
            for line in session.cart.lines():
                self._line(
                    body, f"{line.item.label} x {line.quantity}", f"Rs {line.subtotal}"
                )
            self._line(body, "Food", f"Rs {session.food_total}", bold=True)

        theme.label(
            self,
            f"INVOICE: Rs {session.grand_total}",
            font=("Arial", 16, "bold"),
            pady=6,
        ).pack()

        form = tk.Frame(self, bg=theme.BG)
        form.pack(pady=4)
        theme.field_label(form, "BANK ACCOUNT").grid(row=0, column=0, padx=6, pady=4)
        self.account = theme.entry(form)
        self.account.grid(row=0, column=1, padx=6)
        theme.field_label(form, "PASSWORD").grid(row=1, column=0, padx=6, pady=4)
        self.password = theme.entry(form, show="*")
        self.password.grid(row=1, column=1, padx=6)
        self.password.bind("<Return>", lambda _e: self.pay())

        self.pay_button = theme.primary_button(
            self, f"Pay Rs {session.grand_total}", self.pay, width=30, pady=4
        )
        self.pay_button.pack(pady=(10, 2))
        theme.button(self, "Back", lambda: self.app.go("food_prompt"), width=10).pack(
            pady=2
        )
        self.notice = Notice(self, wraplength=420)
        self.notice.pack(pady=4)
        theme.label(
            self,
            "No bank account? Create one with:  python -m movie_booking.bank",
            fg=theme.MUTED,
            font=("Arial", 8),
        ).pack(side=tk.BOTTOM, pady=4)
        self.account.focus_set()

    @staticmethod
    def _heading(parent, text):
        theme.label(parent, text, font=("Helvetica", 11, "bold", "underline")).pack(
            anchor=tk.W, pady=(8, 2), padx=8
        )

    @staticmethod
    def _line(parent, left, right, *, bold=False):
        row = tk.Frame(parent, bg=theme.BG)
        row.pack(fill=tk.X, padx=8)
        font = theme.FONT_BOLD if bold else theme.FONT
        theme.label(row, left, font=font, anchor=tk.W).pack(side=tk.LEFT)
        theme.label(row, right, font=font).pack(side=tk.RIGHT)

    def pay(self):
        session = self.session
        if not session.tickets():
            self.notice.error("There are no seats in this booking.")
            return
        amount_paise = session.grand_total * 100
        note = f"bookmyshow.com - {session.movie.title}"
        result = {}

        def attempt():
            result["balance"] = self.app.bank.charge(
                self.account.get().strip(), self.password.get(), amount_paise, note
            )

        self.pay_button.config(state=tk.DISABLED)
        paid = False
        try:
            paid = self.guard(self.notice, attempt)
        finally:
            if not paid:
                self.pay_button.config(state=tk.NORMAL)
        if paid:
            self.app.go("tickets", balance=result["balance"])


class TicketsScreen(Screen):
    title = "Your tickets"
    size = (480, 560)

    def build(self, balance):
        session = self.session
        theme.label(
            self, "Payment successful!", fg=theme.GREEN, font=theme.FONT_TITLE, pady=8
        ).pack()
        theme.label(
            self,
            f"Paid Rs {session.grand_total}.  Balance left: {format_money(balance)}",
        ).pack()
        theme.label(self, "Make sure to take some screenshots!!", fg=theme.MUTED).pack(
            pady=(4, 8)
        )

        theme.primary_button(self, "Done", self.app.new_booking, width=30).pack(
            side=tk.BOTTOM, pady=12
        )
        area = ScrollFrame(self, width=440, height=380)
        area.pack()
        qr = photo(self, QR_PATH, (75, 75))
        poster = photo(self, session.movie.poster, (75, 75))
        for ticket in session.tickets():
            stub = tk.Frame(
                area.body,
                bg=theme.BG,
                highlightbackground=theme.MUTED,
                highlightthickness=1,
            )
            stub.pack(fill=tk.X, padx=8, pady=6)
            text = tk.Frame(stub, bg=theme.BG)
            text.pack(side=tk.LEFT, padx=10, pady=8)
            theme.label(
                text,
                f"{ticket.tier} Ticket (Rs.{ticket.price})",
                font=("Helvetica", 12, "bold", "underline"),
            ).pack(anchor=tk.W)
            for line in (
                f"Seat No: {ticket.seat}",
                f"Time: {session.showtime}",
                f"Movie: {session.movie.title}",
                f"Theatre: {session.theatre.name}",
            ):
                theme.label(text, line, font=("Helvetica", 11)).pack(anchor=tk.W)
            for image in (qr, poster):
                if image is not None:
                    holder = tk.Label(stub, image=image, bg=theme.BG)
                    holder.image = image
                    holder.pack(side=tk.RIGHT, padx=6)
