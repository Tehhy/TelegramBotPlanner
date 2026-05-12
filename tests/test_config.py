import os
from my_bot import models
from my_bot.models import Task


def test_telegram_token_is_set():
    """Check if pytest-env correctly injected the fake token from pyproject.toml"""
    token = os.environ.get("TELEGRAM_TOKEN")
    assert token is not None, "TELEGRAM_TOKEN not found in environment variables!"
    assert token == "12345:fake_token_for_tests", (
        "Token found, but it doesn't match the one in pyproject.toml"
    )


def test_database_is_accessible(db_session):
    """Checks that SQLAlchemy and tables are initialized correctly."""
    count = db_session.query(Task).count()

    assert count == 0, "Database should be empty at the start of the test session"

    assert models.SessionLocal is not None
