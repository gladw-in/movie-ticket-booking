"""Holds the food cart and works out its total price."""

from dataclasses import dataclass

from .menu import ITEM_ORDER, MenuItem


@dataclass(frozen=True)
class CartLine:
    item: MenuItem
    quantity: int

    @property
    def subtotal(self):
        return self.item.price * self.quantity


class Cart:
    def __init__(self):
        self._quantities = {}

    def __contains__(self, item):
        return item in self._quantities

    def __len__(self):
        return len(self._quantities)

    @property
    def is_empty(self):
        return not self._quantities

    def quantity(self, item):
        return self._quantities.get(item, 0)

    def add(self, item, quantity=1):
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        self._quantities[item] = self._quantities.get(item, 0) + quantity

    def remove(self, item):
        self._quantities.pop(item, None)

    def toggle(self, item):
        if item in self._quantities:
            del self._quantities[item]
            return False
        self._quantities[item] = 1
        return True

    def choose_size(self, item):
        already_chosen = item in self._quantities
        for other in [
            i
            for i in self._quantities
            if i.section == item.section and i.name == item.name
        ]:
            del self._quantities[other]
        if already_chosen:
            return False
        self._quantities[item] = 1
        return True

    def increment(self, item):
        if item in self._quantities:
            self._quantities[item] += 1

    def decrement(self, item):
        if self._quantities.get(item, 0) > 1:
            self._quantities[item] -= 1

    def lines(self):
        ordered = sorted(
            self._quantities.items(),
            key=lambda kv: ITEM_ORDER.get(kv[0], len(ITEM_ORDER)),
        )
        return [CartLine(item, quantity) for item, quantity in ordered]

    @property
    def total(self):
        return sum(line.subtotal for line in self.lines())

    def clear(self):
        self._quantities.clear()
