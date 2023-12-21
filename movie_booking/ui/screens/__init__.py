"""Lists every screen under the name used to open it."""

from .auth import ForgotPasswordScreen, LoginScreen, SignupScreen
from .browse import MoviesScreen, TheatreScreen
from .checkout import CheckoutScreen, TicketsScreen
from .food import CartScreen, FoodPromptScreen, FoodScreen
from .seats import SeatsScreen

ROUTES = {
    "login": LoginScreen,
    "signup": SignupScreen,
    "forgot": ForgotPasswordScreen,
    "movies": MoviesScreen,
    "theatre": TheatreScreen,
    "seats": SeatsScreen,
    "food_prompt": FoodPromptScreen,
    "food": FoodScreen,
    "cart": CartScreen,
    "checkout": CheckoutScreen,
    "tickets": TicketsScreen,
}
