"""Tests for the bank simulator window."""

import tkinter as tk
from tkinter import messagebox

import pytest

from movie_booking.bank import BankStore
from movie_booking.bank.app import BankApp, FormDialog

PW = "Passw0rd_"


@pytest.fixture
def ui(tmp_path, monkeypatch):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available")
    infos = []
    monkeypatch.setattr(
        messagebox, "showinfo", lambda title, msg, **k: infos.append((title, msg))
    )
    store = BankStore(tmp_path / "bank.sqlite3")
    app = BankApp(root, store)
    root.update()
    yield app, root, store, infos
    store.close()
    root.destroy()


def dialog(root):
    return [w for w in root.winfo_children() if isinstance(w, FormDialog)][-1]


def submit(root, **values):
    form = dialog(root)
    for field in form._fields:
        widget = form._inputs[field.key]
        if field.key in values:
            if field.choices:
                widget.set(values[field.key])
            else:
                widget.delete(0, tk.END)
                widget.insert(0, values[field.key])
    form.submit()
    return form


def test_register_login_deposit_withdraw_and_history(ui):
    app, root, store, infos = ui
    app.register()
    submit(root, name="bob", password=PW, confirm=PW)
    assert store.exists("bob") and infos[-1][0] == "Registered"

    app.log_in()
    submit(root, name="bob", password=PW)
    assert app.user == "bob"

    app.money("Deposit")
    submit(root, amount="250.50")
    assert store.balance("bob") == 25050 and "250.50" in infos[-1][1]

    app.money("Withdraw")
    form = submit(root, amount="1000")
    assert "Insufficient" in form.notice.cget("text") and form.winfo_exists()
    assert store.balance("bob") == 25050

    app.show_history()
    root.update()
    text = [
        w for w in root.winfo_children()[-1].winfo_children() if isinstance(w, tk.Text)
    ][0]
    assert "Deposit" in text.get("1.0", tk.END)


def test_form_shows_validation_errors_and_stays_open(ui):
    app, root, store, _ = ui
    app.register()
    form = submit(root, name="bob", password="weak", confirm="weak")
    assert form.winfo_exists() and "at least 5" in form.notice.cget("text")
    assert not store.exists("bob")


def test_wrong_login_is_rejected(ui):
    app, root, store, _ = ui
    store.register("bob", PW, PW)
    app.log_in()
    form = submit(root, name="bob", password="nope")
    assert app.user is None and "Wrong account name or password" in form.notice.cget(
        "text"
    )


def test_personal_info_then_password_reset(ui):
    app, root, store, infos = ui
    store.register("bob", PW, PW)
    app.user = "bob"
    app.personal_info()
    submit(
        root,
        phone="9822924582",
        country="India",
        state="Goa",
        pincode="403001",
        age="21",
        gender="Male",
        account_type="Savings Account",
    )
    assert store.get_profile("bob")["state"] == "Goa"

    app.forgot_password()
    submit(
        root, name="bob", phone="9822924582", password="Newpass1_", confirm="Newpass1_"
    )
    assert store.authenticate("bob", "Newpass1_") == "bob"


def test_admin_sets_password_once_then_logs_in(ui):
    app, root, store, infos = ui
    store.register("bob", PW, PW)
    app.admin()
    submit(root, password="longenough", confirm="longenough")
    assert store.has_admin()
    app.admin()
    form = submit(root, password="wrong")
    assert "Wrong admin password" in form.notice.cget("text")
    submit(root, password="longenough")
    root.update()
    tables = [
        w
        for top in root.winfo_children()
        if isinstance(top, tk.Toplevel)
        for w in top.winfo_children()
        if w.winfo_class() == "Treeview"
    ]
    assert tables and len(tables[-1].get_children()) == 1


def test_window_title_shows_who_is_logged_in(ui):
    app, root, store, _ = ui
    store.register("bob", PW, PW)
    assert root.title() == "Bank"
    app.log_in()
    submit(root, name="bob", password=PW)
    assert root.title() == "Bank - logged in as bob"


def test_a_second_login_is_refused_while_someone_is_logged_in(ui):
    app, root, store, infos = ui
    store.register("bob", PW, PW)
    store.register("carol", PW, PW)
    app.log_in()
    submit(root, name="bob", password=PW)
    before = len([w for w in root.winfo_children() if isinstance(w, FormDialog)])
    app.log_in()
    assert infos[-1][0] == "Already logged in" and app.user == "bob"
    assert (
        len([w for w in root.winfo_children() if isinstance(w, FormDialog)]) == before
    )


def test_actions_without_a_login_raise_a_clear_error_not_a_crash(ui):
    from movie_booking.bank import BankError

    app, *_ = ui
    for action in (app.show_balance, app.show_history, app.personal_info):
        with pytest.raises(BankError, match="log in first"):
            action()
