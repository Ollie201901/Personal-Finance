from db import Database
import pytest


def test_create():
    db = Database()
    db.create()

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
    assert db.cursor.fetchone() is not None

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendors'")
    assert db.cursor.fetchone() is not None

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='budget'")
    assert db.cursor.fetchone() is not None

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    assert db.cursor.fetchone() is not None

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transaction_sources'")
    assert db.cursor.fetchone() is not None

    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auto_assignment'")
    assert db.cursor.fetchone() is not None

