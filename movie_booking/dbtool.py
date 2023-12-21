"""Command-line tool to look after the MySQL accounts database."""

import getpass

import mysql.connector

from . import security
from .config import load_settings, save_settings
from .database import (
    DatabaseError,
    _quote_identifier,
    connect,
    create_database,
    create_tables,
)

DEMO_USERS = [
    ("Abhik", "9822924582"),
    ("Dhruv", "9822724582"),
    ("Admin", "9821024582"),
    ("Tanishk", "9820229482"),
    ("Glad432", "9830229482"),
]
DEMO_PASSWORD = "123456"

MENU = """
 1. Show databases
 2. Create the database
 3. Drop the accounts table
 4. Create the accounts table
 5. Insert demo users (password: 123456)
 6. Delete the database
 7. Exit
"""


def show_databases(settings):
    with connect(settings, use_database=False) as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        for (name,) in cursor.fetchall():
            print("  ", name)


def make_database(settings):
    create_database(settings)
    print(f"Database {settings.database} is ready.")


def make_table(settings):
    create_tables(settings)
    print("Table acc is ready.")


def drop_table(settings):
    with connect(settings) as conn:
        conn.cursor().execute("DROP TABLE IF EXISTS acc")
    print("Dropped table acc.")


def insert_demo_users(settings):
    added = 0
    with connect(settings) as conn:
        cursor = conn.cursor()
        for username, phone in DEMO_USERS:
            try:
                cursor.execute(
                    "INSERT INTO acc (username, phno, `pass`) VALUES (%s, %s, %s)",
                    (username, phone, security.hash_password(DEMO_PASSWORD)),
                )
                added += 1
            except mysql.connector.IntegrityError:
                print(f"  {username} already exists, skipped")
    print(f"Inserted {added} demo user(s).")


def drop_database(settings):
    with connect(settings, use_database=False) as conn:
        conn.cursor().execute(
            f"DROP DATABASE IF EXISTS {_quote_identifier(settings.database)}"
        )
    print(f"Dropped database {settings.database}.")


def _confirmed(prompt, expected):
    return input(f"{prompt} Type '{expected}' to confirm: ").strip() == expected


def main():
    settings = load_settings()
    if settings.password is None:
        settings = settings.with_password(
            getpass.getpass(f"MySQL password for {settings.user}@{settings.host}: ")
        )
        if input("Remember it on this computer? [y/N] ").strip().lower() == "y":
            save_settings(settings, remember_password=True)

    actions = {
        "1": lambda: show_databases(settings),
        "2": lambda: make_database(settings),
        "3": lambda: (
            drop_table(settings)
            if _confirmed("This deletes every account.", "acc")
            else print("Cancelled.")
        ),
        "4": lambda: make_table(settings),
        "5": lambda: insert_demo_users(settings),
        "6": lambda: (
            drop_database(settings)
            if _confirmed("This deletes the whole database.", settings.database)
            else print("Cancelled.")
        ),
    }
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "7":
            return
        action = actions.get(choice)
        if action is None:
            print("Please choose 1-7.")
            continue
        try:
            action()
        except DatabaseError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
