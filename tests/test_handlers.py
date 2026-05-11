from unittest.mock import ANY, MagicMock, patch
from my_bot.Telebot import add, help_handler
from my_bot.models import Task


def test_help_command():
    message = MagicMock()
    message.chat.id = 111

    with patch("my_bot.Telebot.bot") as mock_bot:
        help_handler(message)
        mock_bot.send_message.assert_called_with(111, ANY)


def test_add_command_valid_format(db_session):
    """Checking if a task with a category has been added to the database."""
    message = MagicMock()
    message.chat.id = 222
    message.from_user.id = 222
    message.text = "/add tomorrow Buy bread @Food"

    with patch("my_bot.Telebot.bot") as mock_bot:
        from my_bot.Telebot import add

        add(message)

    task = db_session.query(Task).filter_by(user_id=222, date="tomorrow").first()

    assert task is not None
    assert task.text == "Buy bread"
    assert task.category == "Food"

    mock_bot.send_message.assert_called_with(
        222, "✅ Task added for tomorrow in category @Food!"
    )


def test_add_command_invalid_format():
    message = MagicMock()
    message.chat.id = 333
    message.text = "/add"  # Incorrect format

    with patch("my_bot.Telebot.bot") as mock_bot:
        add(message)
        mock_bot.send_message.assert_called_with(
            333, "Usage: /add <date> <task> @<category>"
        )


def test_show_command(db_session):
    user_id = 555
    task = Task(user_id=user_id, date="today", text="Test Task", category="General")
    db_session.add(task)
    db_session.commit()

    message = MagicMock()
    message.chat.id = user_id
    message.from_user.id = user_id
    message.text = "/show today"

    with patch("my_bot.Telebot.bot") as mock_bot:
        from my_bot.Telebot import show

        show(message)

        args, _ = mock_bot.send_message.call_args
        sent_text = args[1]

        assert "[General]" in sent_text
        assert "Test Task" in sent_text
        assert "today" in sent_text.lower()
