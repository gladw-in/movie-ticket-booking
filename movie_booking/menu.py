"""Lists the food and drink items that can be ordered."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MenuItem:
    name: str
    price: int
    section: str
    size: str | None = None

    @property
    def label(self):
        return f"{self.name} ({self.size})" if self.size else self.name


@dataclass(frozen=True)
class MenuSection:
    title: str
    items: tuple[MenuItem, ...]
    sizes: tuple[str, ...] = ()

    @property
    def is_sized(self):
        return bool(self.sizes)

    def drinks(self):
        return list(dict.fromkeys(item.name for item in self.items))


@dataclass(frozen=True)
class MenuCategory:
    title: str
    sections: tuple[MenuSection, ...]


def _section(title, entries):
    return MenuSection(
        title, tuple(MenuItem(name, price, title) for name, price in entries)
    )


def _sized_section(title, sizes, entries):
    items = tuple(
        MenuItem(name, price, title, size)
        for name, prices in entries
        for size, price in zip(sizes, prices, strict=True)
    )
    return MenuSection(title, items, sizes)


MENU = (
    MenuCategory(
        "Dessert",
        (
            _section(
                "Ice cream",
                [
                    ("Butterscotch ice cream", 129),
                    ("Chocolate ice cream", 149),
                    ("Vanilla ice cream", 110),
                    ("Strawberry ice cream", 139),
                    ("Mint chocolate chip ice cream", 149),
                    ("Cookies n' Cream ice cream", 169),
                ],
            ),
            _section(
                "Pastries",
                [
                    ("Pineapple pastry", 119),
                    ("Butterscotch pastry", 149),
                    ("Chocolate pastry", 139),
                    ("Red velvet pastry", 149),
                ],
            ),
        ),
    ),
    MenuCategory(
        "Fast Food",
        (
            _section(
                "Burger",
                [
                    ("Aaloo patty", 269),
                    ("Veggie cheese", 299),
                    ("Aaloo Paneer patty", 170),
                    ("American chicken (non veg)", 399),
                    ("Chicken burger (non veg)", 349),
                    ("Veg zinger burger", 320),
                    ("Classic zinger (non veg)", 360),
                    ("Chicken crisp (non veg)", 420),
                ],
            ),
            _section(
                "Pizza",
                [
                    ("Onion pizza", 199),
                    ("Paneer pizza", 229),
                    ("Plain cheese pizza", 149),
                    ("Chicken pizza (non veg)", 299),
                    ("Extra cheese chicken pizza (non veg)", 399),
                    ("Chicken lasagne", 399),
                ],
            ),
            _section(
                "Sandwich",
                [
                    ("Veg sandwich", 179),
                    ("Double cheese (veg)", 249),
                    ("Chicken sandwich (non veg)", 299),
                    ("Grilled chicken (non veg)", 319),
                    ("Italian sandwich", 210),
                ],
            ),
            _section(
                "Fries",
                [
                    ("Peri Peri fries", 299),
                    ("Schezwan fries", 350),
                    ("Masala fries", 289),
                ],
            ),
            _section(
                "Taco",
                [
                    ("Soft taco", 139),
                    ("Soft Taco supreme", 209),
                    ("Crunchy taco", 139),
                    ("Nacho Cheese", 199),
                    ("Dorito Supreme x6", 281),
                ],
            ),
            _section(
                "Chicken",
                [
                    ("Boneless Strips x8", 249),
                    ("Hotwings x6", 249),
                    ("Hot & Crispy Wings x8", 469),
                    ("Grilled x6", 281),
                    ("Nugget x6", 281),
                ],
            ),
        ),
    ),
    MenuCategory(
        "Desi Snacks",
        (
            _section(
                "Snacks",
                [
                    ("Samosa", 69),
                    ("Samosa chat", 79),
                    ("Bhel chat", 89),
                    ("Vada pav", 99),
                    ("Dahi Vada", 119),
                    ("Pav bhaji", 119),
                ],
            ),
        ),
    ),
    MenuCategory(
        "Beverage",
        (
            _sized_section(
                "Soft drinks",
                ("Small", "Medium", "Big"),
                [
                    (name, (45, 75, 99))
                    for name in (
                        "Coke",
                        "Pepsi",
                        "Fanta",
                        "Sprite",
                        "Mountain Dew",
                        "Blue Berry",
                        "Prime",
                    )
                ],
            ),
            _section(
                "Coffee",
                [
                    ("Filter Coffee", 69),
                    ("Cold coffee", 79),
                    ("Cappuccino", 89),
                    ("Flat White", 139),
                    ("Soya Cappuccino", 119),
                    ("Inverted Cappuccino", 119),
                    ("Honey Cinnamon", 119),
                    ("Cafe Latte", 119),
                    ("Vanilla Cappuccino", 119),
                    ("Vanilla Latte", 119),
                ],
            ),
            _section(
                "Milkshakes",
                [
                    ("Vanilla Milkshake", 150),
                    ("Mango Milkshake", 150),
                    ("Banana Milkshake", 150),
                    ("Chocolate Milkshake", 150),
                    ("Caramel Milkshake", 160),
                    ("Oreo Milkshake", 160),
                    ("Kit Kat Milkshake", 160),
                    ("Bubblegum Milkshake", 160),
                    ("Choco Milkshake", 160),
                    ("Blueberry Milkshake", 160),
                    ("Nutella Milkshake", 160),
                    ("Brownie Milkshake", 170),
                    ("Brownie Mint Milkshake", 170),
                    ("Choco Banana Milkshake", 170),
                    ("Death by Chocolate", 190),
                    ("Swedo Choco Chip", 190),
                    ("Ferro Hazelnut", 220),
                ],
            ),
            _section(
                "Smoothies",
                [
                    ("Strawberry smoothie", 150),
                    ("Mango Smoothie", 150),
                    ("Banana Smoothie", 150),
                    ("Blue Berry Smoothie", 150),
                ],
            ),
            _section(
                "Refreshers",
                [
                    ("Lemonade", 181),
                    ("Berry", 181),
                    ("Strawberry Breeze", 181),
                    ("Watermelon", 181),
                    ("Green Tea", 181),
                ],
            ),
            _section(
                "Chocolate Bliss",
                [
                    ("Gourmet Belgian Hot Chocolate", 240),
                    ("Gourmet Belgian Cold Chocolate", 233),
                    ("Chocolate Overload Drink", 243),
                ],
            ),
        ),
    ),
)


def all_sections():
    return [section for category in MENU for section in category.sections]


def all_items():
    return [item for section in all_sections() for item in section.items]


ITEM_ORDER = {item: index for index, item in enumerate(all_items())}


def find_category(title):
    return next(category for category in MENU if category.title == title)


def find_section(category, title):
    return next(section for section in category.sections if section.title == title)
