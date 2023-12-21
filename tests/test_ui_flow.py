"""Tests the whole booking flow through the real Tk screens."""

import tkinter as tk
from tkinter import messagebox

import pytest

from movie_booking.accounts import AccountService
from movie_booking.bank import BankStore, format_money
from movie_booking.catalog import load_movies
from movie_booking.seating import INOX, PVR
from movie_booking.ui.app import App

from .fakes import FakeRepo

PW = "Passw0rd_"


def walk(widget):
    yield widget
    for child in widget.winfo_children():
        yield from walk(child)


def button(screen, text):
    return next(
        w for w in walk(screen) if isinstance(w, tk.Button) and w.cget("text") == text
    )


def fill(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)


@pytest.fixture
def root():
    try:
        window = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available")
    window.update()
    yield window
    window.destroy()


@pytest.fixture
def dialogs(monkeypatch):
    shown = []
    monkeypatch.setattr(
        messagebox, "showinfo", lambda *a, **k: shown.append(("info", a))
    )
    monkeypatch.setattr(
        messagebox, "showerror", lambda *a, **k: shown.append(("error", a))
    )
    monkeypatch.setattr(messagebox, "askyesno", lambda *a, **k: True)
    return shown


@pytest.fixture
def app(root, tmp_path, dialogs):
    bank = BankStore(tmp_path / "bank.sqlite3")
    application = App(root, AccountService(FakeRepo()), bank, load_movies())
    application.start()
    root.update()
    yield application
    bank.close()


def sign_up_and_log_in(app, root, name="tanishk"):
    app.go("signup")
    screen = app._current
    for entry, value in (
        (screen.username, name),
        (screen.phone, "9820229482"),
        (screen.password, "pass1234"),
        (screen.confirm, "pass1234"),
    ):
        fill(entry, value)
    screen.human.set(True)
    screen._sync_button()
    screen.submit_button.invoke()
    root.update()
    login = app._current
    fill(login.username, name)
    fill(login.password, "pass1234")
    login.submit()
    root.update()


def test_every_route_builds_without_errors(app, root):
    sign_up_and_log_in(app, root)
    session = app.session
    session.movie = app.movies[0]
    session.choose_theatre(INOX)
    session.choose_showtime("Morning")
    session.seats.toggle("A1")
    for route, params in [
        ("login", {}),
        ("signup", {}),
        ("forgot", {}),
        ("movies", {}),
        ("theatre", {}),
        ("seats", {}),
        ("food_prompt", {}),
        ("food", {"path": ()}),
        ("food", {"path": ("Beverage",)}),
        ("food", {"path": ("Beverage", "Soft drinks")}),
        ("food", {"path": ("Desi Snacks",)}),
        ("cart", {}),
        ("checkout", {}),
        ("tickets", {"balance": 12345}),
    ]:
        app.go(route, **params)
        root.update()


def test_sign_up_validation_and_duplicates(app, root):
    app.go("signup")
    screen = app._current
    assert str(screen.submit_button.cget("state")) == "disabled"
    fill(screen.username, "ab")
    screen.human.set(True)
    screen._sync_button()
    screen.submit_button.invoke()
    assert "at least 4" in screen.notice.cget("text")
    assert str(screen.submit_button.cget("state")) == "disabled"

    sign_up_and_log_in(app, root)
    app.log_out()
    app.go("signup")
    screen = app._current
    for entry, value in (
        (screen.username, "tanishk"),
        (screen.phone, "9820229482"),
        (screen.password, "pass1234"),
        (screen.confirm, "pass1234"),
    ):
        fill(entry, value)
    screen.human.set(True)
    screen._sync_button()
    screen.submit_button.invoke()
    assert "already taken" in screen.notice.cget(
        "text"
    ) and "Try" in screen.notice.cget("text")


def test_wrong_password_is_reported_on_the_login_screen(app, root):
    sign_up_and_log_in(app, root)
    app.log_out()
    screen = app._current
    fill(screen.username, "tanishk")
    fill(screen.password, "nope")
    screen.submit()
    assert "Wrong username or password" in screen.notice.cget("text")
    assert app.session is None


def test_forgot_password_flow(app, root):
    sign_up_and_log_in(app, root)
    app.log_out()
    app.go("forgot")
    screen = app._current
    fill(screen.username, "tanishk")
    fill(screen.phone, "0000000000")
    screen.verify()
    assert "do not match" in screen.notice.cget("text")
    fill(screen.phone, "9820229482")
    screen.verify()
    fill(screen.new_password, "brandnew1")
    fill(screen.confirm, "brandnew1")
    screen.reset()
    root.update()
    login = app._current
    assert "Password changed" in login.notice.cget("text")
    fill(login.username, "tanishk")
    fill(login.password, "brandnew1")
    login.submit()
    assert app.session is not None and app.session.username == "tanishk"


def test_carousel_buttons_are_disabled_at_the_ends(app, root):
    sign_up_and_log_in(app, root)
    screen = app._current
    assert str(screen.back_button.cget("state")) == "disabled"
    for _ in range(10):
        screen.forward_button.invoke()
    assert screen.index == len(app.movies) - 1
    assert str(screen.forward_button.cget("state")) == "disabled"


def test_seat_maps_have_the_right_number_of_buttons(app, root):
    sign_up_and_log_in(app, root)
    for theatre in (INOX, PVR):
        app.session.choose_theatre(theatre)
        app.session.movie = app.movies[0]
        app.go("seats")
        assert len(app._current.seat_buttons) == theatre.capacity


def test_proceeding_requires_a_time_and_a_seat(app, root, dialogs):
    sign_up_and_log_in(app, root)
    button(app._current, "batman\n---- click to book ----").invoke()
    button(app._current, "INOX").invoke()
    seats = app._current
    button(seats, "Proceed to payment").invoke()
    assert "time" in dialogs[-1][1][1]
    seats.time_buttons["Morning"].invoke()
    button(seats, "Proceed to payment").invoke()
    assert "seat" in dialogs[-1][1][1]
    assert type(app._current).__name__ == "SeatsScreen"


def test_full_booking_flow(app, root):
    sign_up_and_log_in(app, root)
    app.bank.register("bob", PW, PW)
    app.bank.deposit("bob", 1_000_00)

    movies = app._current
    movies.forward_button.invoke()
    assert "mission impossible" in movies.book_button.cget("text")
    movies.book_button.invoke()
    button(app._current, "PVR").invoke()
    seats = app._current
    seats.time_buttons["Evening"].invoke()
    seats.seat_buttons["A2"].invoke()
    seats.seat_buttons["B5"].invoke()
    seats.seat_buttons["B6"].invoke()
    seats.seat_buttons["B6"].invoke()
    assert "2 seats selected  -  Rs 450" in seats.summary.cget("text")
    button(seats, "Proceed to payment").invoke()

    button(app._current, "Yes").invoke()
    button(app._current, "Desi Snacks").invoke()
    food = app._current
    button(food, "Samosa").invoke()
    button(food, "Back").invoke()
    button(app._current, "Beverage").invoke()
    button(app._current, "Soft drinks").invoke()
    sizes = app._current
    coke = [i for i in sizes.item_buttons if i.name == "Coke"]
    sizes.item_buttons[coke[0]].invoke()
    sizes.item_buttons[coke[2]].invoke()
    assert coke[0] not in app.session.cart and coke[2] in app.session.cart
    button(sizes, f"Go to cart (2)  -  Rs {69 + 99}").invoke()

    cart = app._current
    samosa = next(i for i in app.session.cart._quantities if i.name == "Samosa")
    plus = [
        w for w in walk(cart) if isinstance(w, tk.Button) and w.cget("text") == "+"
    ][0]
    plus.invoke()
    assert app.session.cart.quantity(samosa) == 2
    assert app.session.food_total == 69 * 2 + 99
    button(cart, "Continue to payment").invoke()

    checkout = app._current
    total = 450 + 69 * 2 + 99
    assert app.session.grand_total == total
    fill(checkout.account, "bob")
    fill(checkout.password, "wrong")
    checkout.pay()
    assert "Wrong account name or password" in checkout.notice.cget("text")
    assert app.bank.balance("bob") == 1_000_00
    fill(checkout.password, PW)
    checkout.pay()
    root.update()
    assert app.bank.balance("bob") == (1_000 - total) * 100

    tickets = app._current
    labels = [w.cget("text") for w in walk(tickets) if isinstance(w, tk.Label)]
    assert "Seat No: A2" in labels and "Seat No: B5" in labels
    assert any("Royal Ticket (Rs.250)" in t for t in labels)
    assert any(format_money((1_000 - total) * 100) in t for t in labels)

    button(tickets, "Done").invoke()
    assert type(app._current).__name__ == "MoviesScreen"
    assert (
        app.session.username == "tanishk"
        and app.session.cart.is_empty
        and app.session.seats is None
    )


def test_insufficient_funds_blocks_payment(app, root):
    sign_up_and_log_in(app, root)
    app.bank.register("bob", PW, PW)
    app.bank.deposit("bob", 100_00)
    session = app.session
    session.movie = app.movies[0]
    session.choose_theatre(INOX)
    session.choose_showtime("Morning")
    session.seats.toggle("A1")
    app.go("checkout")
    checkout = app._current
    fill(checkout.account, "bob")
    fill(checkout.password, PW)
    checkout.pay()
    assert "Insufficient funds" in checkout.notice.cget("text")
    assert app.bank.balance("bob") == 100_00
    assert str(checkout.pay_button.cget("state")) == "normal"


def test_cart_editing(app, root):
    sign_up_and_log_in(app, root)
    cart_model = app.session.cart
    from movie_booking.menu import all_items

    for item in all_items()[:2]:
        cart_model.add(item)
    app.go("cart")
    cart = app._current
    remove = [
        w for w in walk(cart) if isinstance(w, tk.Button) and w.cget("text") == "x"
    ]
    assert len(remove) == 2
    remove[0].invoke()
    assert len(cart_model) == 1


def test_delete_account_returns_to_login(app, root):
    sign_up_and_log_in(app, root)
    button(app._current, "Delete account").invoke()
    root.update()
    assert app.session is None and "deleted" in app._current.notice.cget("text")
    assert app.accounts._repo.rows == {}


def test_wheel_bindings_are_released_when_a_scroll_area_is_destroyed(root):
    from movie_booking.ui.widgets import ScrollFrame

    errors = []
    root.report_callback_exception = lambda *exc: errors.append(exc[1])
    area = ScrollFrame(root)
    area.pack()
    root.update()
    area.event_generate("<Enter>")
    root.update()
    area.destroy()
    root.update()
    root.event_generate("<Button-4>")
    root.event_generate("<MouseWheel>", delta=-120)
    root.update()
    assert errors == []


def test_pay_button_is_not_left_disabled_after_an_unexpected_error(
    app, root, monkeypatch
):
    sign_up_and_log_in(app, root)
    app.session.movie = app.movies[0]
    app.session.choose_theatre(INOX)
    app.session.choose_showtime("Morning")
    app.session.seats.toggle("B1")
    app.go("checkout")
    checkout = app._current

    def explode(*args, **kwargs):
        raise RuntimeError("disk on fire")

    monkeypatch.setattr(app.bank, "charge", explode)
    with pytest.raises(RuntimeError):
        checkout.pay()
    assert str(checkout.pay_button.cget("state")) == "normal"


def test_a_busy_bank_is_shown_as_a_message_not_a_crash(app, root, tmp_path):
    sign_up_and_log_in(app, root)
    app.bank.register("bob", PW, PW)
    app.bank.deposit("bob", 1000_00)
    app.bank._conn.execute("PRAGMA busy_timeout = 100")
    other = BankStore(tmp_path / "bank.sqlite3", timeout=0.1)
    app.session.movie = app.movies[0]
    app.session.choose_theatre(INOX)
    app.session.choose_showtime("Morning")
    app.session.seats.toggle("B1")
    app.go("checkout")
    checkout = app._current
    other._conn.execute("BEGIN IMMEDIATE")
    fill(checkout.account, "bob")
    fill(checkout.password, PW)
    checkout.pay()
    other._conn.execute("ROLLBACK")
    assert "busy" in checkout.notice.cget("text")
    assert str(checkout.pay_button.cget("state")) == "normal"
    other.close()


def test_unexpected_callback_errors_open_a_dialog_instead_of_vanishing(
    app, root, dialogs
):
    from movie_booking.bank import BankError

    root.report_callback_exception(ZeroDivisionError, ZeroDivisionError("boom"), None)
    assert dialogs[-1][0] == "error" and "boom" in dialogs[-1][1][1]
    root.report_callback_exception(BankError, BankError("Insufficient funds."), None)
    assert dialogs[-1][0] == "info" and "Insufficient funds." in dialogs[-1][1][1]


def test_pvr_seat_map_is_narrow_enough_for_a_1024_pixel_screen(app, root):
    sign_up_and_log_in(app, root)
    app.session.movie = app.movies[0]
    app.session.choose_theatre(PVR)
    app.go("seats")
    root.update()
    assert root.winfo_reqwidth() < 1000
