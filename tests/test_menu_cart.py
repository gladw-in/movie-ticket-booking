"""Tests for the food menu and the cart."""

import pytest

from movie_booking.cart import Cart
from movie_booking.menu import (
    MENU,
    all_items,
    all_sections,
    find_category,
    find_section,
)


def item(section, name, size=None):
    return next(
        i
        for i in all_items()
        if i.section == section and i.name == name and i.size == size
    )


def test_menu_shape():
    assert [c.title for c in MENU] == [
        "Dessert",
        "Fast Food",
        "Desi Snacks",
        "Beverage",
    ]
    assert len(all_sections()) == 15
    assert len(all_items()) == 108
    assert len(set(all_items())) == 108


def test_spot_check_prices_against_the_original_menu():
    assert item("Burger", "Chicken crisp (non veg)").price == 420
    assert item("Milkshakes", "Ferro Hazelnut").price == 220
    assert item("Snacks", "Samosa").price == 69
    assert [
        item("Soft drinks", "Coke", s).price for s in ("Small", "Medium", "Big")
    ] == [45, 75, 99]


def test_soft_drinks_are_the_only_sized_section():
    sized = [s for s in all_sections() if s.is_sized]
    assert [s.title for s in sized] == ["Soft drinks"]
    assert sized[0].drinks()[:2] == ["Coke", "Pepsi"] and len(sized[0].items) == 21


def test_lookup_helpers():
    beverage = find_category("Beverage")
    assert find_section(beverage, "Coffee").title == "Coffee"


def test_total_counts_quantity():
    cart = Cart()
    samosa = item("Snacks", "Samosa")
    cart.add(samosa)
    cart.increment(samosa)
    cart.increment(samosa)
    assert cart.quantity(samosa) == 3
    assert cart.total == 69 * 3


def test_decrement_stops_at_one_and_remove_deletes():
    cart, samosa = Cart(), item("Snacks", "Samosa")
    cart.add(samosa)
    cart.decrement(samosa)
    assert cart.quantity(samosa) == 1
    cart.remove(samosa)
    assert cart.is_empty and cart.total == 0


def test_toggle():
    cart, samosa = Cart(), item("Snacks", "Samosa")
    assert cart.toggle(samosa) is True and samosa in cart
    assert cart.toggle(samosa) is False and samosa not in cart


def test_choosing_a_size_replaces_the_other_size_of_that_drink_only():
    cart = Cart()
    small, big = item("Soft drinks", "Coke", "Small"), item(
        "Soft drinks", "Coke", "Big"
    )
    pepsi = item("Soft drinks", "Pepsi", "Medium")
    assert cart.choose_size(small) is True
    cart.choose_size(pepsi)
    assert cart.choose_size(big) is True
    assert small not in cart and big in cart and pepsi in cart
    assert cart.choose_size(big) is False
    assert big not in cart and pepsi in cart


def test_lines_follow_menu_order_not_insertion_order():
    cart = Cart()
    late, early = item("Coffee", "Cappuccino"), item("Ice cream", "Vanilla ice cream")
    cart.add(late)
    cart.add(early)
    assert [line.item for line in cart.lines()] == [early, late]


def test_add_rejects_non_positive_quantity():
    with pytest.raises(ValueError):
        Cart().add(item("Snacks", "Samosa"), 0)


def test_item_labels():
    assert item("Soft drinks", "Coke", "Small").label == "Coke (Small)"
    assert item("Snacks", "Samosa").label == "Samosa"
