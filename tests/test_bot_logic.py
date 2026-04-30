from unittest.mock import MagicMock, patch
from my_bot.models import Task
from my_bot.Telebot import add


def test_add_new_date(db_session):
    """Test adding a task for a new date (checking the creation of a record in the database)."""
    message = MagicMock()
    message.from_user.id = 123
    message.chat.id = 123
    message.text = "/add 2026-05-01 Buy milk @Shopping"

    with patch("my_bot.Telebot.bot"):
        add(message)

    task = db_session.query(Task).filter_by(user_id=123, date="2026-05-01").first()
    assert task is not None
    assert task.text == "Buy milk @Shopping"


def test_add_multiple_tasks(db_session):
    """Test adding multiple tasks to the same date."""
    user_id = 777
    message = MagicMock()
    message.from_user.id = user_id
    message.chat.id = user_id

    with patch("my_bot.Telebot.bot"):
        message.text = "/add today Task 1"
        add(message)
        message.text = "/add today Task 2"
        add(message)

    count = db_session.query(Task).filter_by(user_id=user_id, date="today").count()
    assert count == 2
