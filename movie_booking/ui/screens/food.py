"""Screens to choose food and drinks and fill the cart."""

import tkinter as tk

from ...menu import MENU, find_category, find_section
from .. import theme
from ..base import Screen
from ..widgets import ScrollFrame

FOOD_SIZE = (520, 580)


class FoodPromptScreen(Screen):
    title = "Order food"
    size = (330, 260)

    def build(self):
        theme.label(
            self, "Do you want to add on food?", font=theme.FONT_BOLD, pady=24
        ).pack()
        theme.button(self, "Yes", lambda: self.app.go("food", path=()), width=14).pack(
            pady=6
        )
        theme.button(self, "No", lambda: self.app.go("checkout"), width=14).pack(pady=6)
        theme.button(self, "Back", lambda: self.app.go("seats"), width=14).pack(
            pady=(18, 0)
        )


class FoodScreen(Screen):
    title = "BookMyShow.food.com"
    size = FOOD_SIZE

    def build(self, path=()):
        self.path = path
        self.cart = self.session.cart
        self.category = find_category(path[0]) if path else None
        self.section = None
        if self.category is not None:
            sections = self.category.sections
            if len(path) > 1:
                self.section = find_section(self.category, path[1])
            elif len(sections) == 1:
                self.section = sections[0]

        theme.label(
            self, "BookMyShow.food.com", font=("Helvetica", 18, "bold"), pady=10
        ).pack()
        theme.label(
            self, "  >  ".join(path) or "Choose a category", fg=theme.MUTED
        ).pack()

        self._footer()
        if self.section is not None:
            self._items(self.section)
        elif self.category is not None:
            self._choices(
                [s.title for s in self.category.sections],
                lambda t: (self.category.title, t),
            )
        else:
            self._choices([c.title for c in MENU], lambda t: (t,))
        self.refresh_cart_button()

    def _choices(self, titles, to_path):
        box = tk.Frame(self, bg=theme.BG)
        box.pack(expand=True)
        for title in titles:
            theme.button(
                box,
                title,
                lambda t=title: self.app.go("food", path=to_path(t)),
                width=22,
                pady=4,
                font=theme.FONT_BOLD,
            ).pack(pady=6)

    def _items(self, section):
        area = ScrollFrame(self, width=480, height=340)
        area.pack(pady=8)
        self.item_buttons = {}
        if section.is_sized:
            self._sized_rows(area.body, section)
        else:
            for row, item in enumerate(section.items):
                button = theme.button(
                    area.body, item.name, lambda i=item: self.toggle(i), width=34
                )
                button.grid(row=row, column=0, sticky=tk.EW, pady=1)
                theme.label(area.body, f"Rs {item.price}", width=8).grid(
                    row=row, column=1
                )
                self.item_buttons[item] = button
        self.paint()

    def _sized_rows(self, parent, section):
        theme.label(parent, "Item", font=theme.FONT_BOLD, width=16).grid(
            row=0, column=0
        )
        for column, size in enumerate(section.sizes, start=1):
            theme.label(parent, size, font=theme.FONT_BOLD, width=8).grid(
                row=0, column=column
            )
        for row, name in enumerate(section.drinks(), start=1):
            theme.label(parent, name, width=16, anchor=tk.W).grid(
                row=row, column=0, pady=1
            )
            for column, item in enumerate(
                (i for i in section.items if i.name == name), start=1
            ):
                button = theme.button(
                    parent,
                    f"Rs {item.price}",
                    lambda i=item: self.choose_size(i),
                    width=8,
                )
                button.grid(row=row, column=column, padx=1)
                self.item_buttons[item] = button

    def _footer(self):
        row = tk.Frame(self, bg=theme.BG)
        row.pack(side=tk.BOTTOM, pady=12)
        theme.button(row, "Back", self.go_back, width=10).grid(row=0, column=0, padx=6)
        self.cart_button = theme.primary_button(
            row, "", lambda: self.app.go("cart"), width=26
        )
        self.cart_button.grid(row=0, column=1, padx=6)

    def go_back(self):
        if not self.path:
            self.app.go("food_prompt")
        elif len(self.path) == 1 or (len(self.category.sections) == 1):
            self.app.go("food", path=())
        else:
            self.app.go("food", path=self.path[:-1])

    def toggle(self, item):
        self.cart.toggle(item)
        self.paint()

    def choose_size(self, item):
        self.cart.choose_size(item)
        self.paint()

    def paint(self):
        for item, button in self.item_buttons.items():
            button.config(bg=theme.GREEN if item in self.cart else theme.BG)
        self.refresh_cart_button()

    def refresh_cart_button(self):
        count = sum(line.quantity for line in self.cart.lines())
        self.cart_button.config(text=f"Go to cart ({count})  -  Rs {self.cart.total}")


class CartScreen(Screen):
    title = "Your cart"
    size = FOOD_SIZE

    def build(self):
        self.cart = self.session.cart
        theme.label(self, "Your cart", font=("Helvetica", 18, "bold"), pady=10).pack()

        footer = tk.Frame(self, bg=theme.BG)
        footer.pack(side=tk.BOTTOM, pady=12)
        self.total_label = theme.label(footer, "", font=theme.FONT_BOLD)
        self.total_label.grid(row=0, column=0, columnspan=2, pady=(0, 8))
        theme.button(
            footer, "Add more items", lambda: self.app.go("food", path=()), width=16
        ).grid(row=1, column=0, padx=6)
        theme.primary_button(
            footer, "Continue to payment", lambda: self.app.go("checkout"), width=22
        ).grid(row=1, column=1, padx=6)

        self.area = ScrollFrame(self, width=480, height=340)
        self.area.pack(pady=4)
        self.render()

    def render(self):
        self.area.clear()
        body = self.area.body
        lines = self.cart.lines()
        if not lines:
            theme.label(body, "Nothing here yet.", pady=30).pack()
        current_section = None
        row = 0
        for line in lines:
            item = line.item
            if item.section != current_section:
                current_section = item.section
                theme.label(
                    body, current_section, font=("Helvetica", 12, "bold", "underline")
                ).grid(row=row, column=0, columnspan=6, pady=(10, 2), sticky=tk.W)
                row += 1
            theme.button(
                body,
                "x",
                lambda i=item: self.change(self.cart.remove, i),
                width=2,
                borderwidth=0,
            ).grid(row=row, column=0)
            theme.label(body, item.label, width=22, anchor=tk.W).grid(row=row, column=1)
            theme.label(body, f"Rs {item.price}", width=7).grid(row=row, column=2)
            theme.button(
                body,
                "-",
                lambda i=item: self.change(self.cart.decrement, i),
                width=1,
                state=tk.NORMAL if line.quantity > 1 else tk.DISABLED,
            ).grid(row=row, column=3)
            theme.label(body, str(line.quantity), width=3).grid(row=row, column=4)
            theme.button(
                body, "+", lambda i=item: self.change(self.cart.increment, i), width=1
            ).grid(row=row, column=5)
            row += 1
        self.total_label.config(text=f"Food total: Rs {self.cart.total}")

    def change(self, operation, item):
        operation(item)
        self.render()
