from unittest.mock import ANY, MagicMock, patch
from my_bot.Telebot import add, help_handler
from my_bot.models import Task
import pytest


def test_help_command_sends_message():
    """Checks for the presence of a list of commands in the help."""
    message = MagicMock()
    message.chat.id = 111

    with patch("my_bot.Telebot.bot") as mock_bot:
        help_handler(message)
        args, _ = mock_bot.send_message.call_args
        sent_text = args[1]

        assert "/add" in sent_text
        assert "/show" in sent_text
        mock_bot.send_message.assert_called_once_with(111, ANY)


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
    """Checks whether instructions are sent to the user when the /add command is entered in an invalid format."""
    message = MagicMock()
    message.chat.id = 333
    message.text = "/add"  # Incorrect format

    with patch("my_bot.Telebot.bot") as mock_bot:
        add(message)
        mock_bot.send_message.assert_called_with(
            333, "Usage: /add <date> <task> @<category>"
        )


def test_show_command(db_session, create_task):
    """Checks whether the task list is displayed correctly for a specific date."""
    user_id = 555
    create_task(user_id=user_id, date="today", text="Test Task", category="General")

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


def test_show_command_empty(db_session):
    """Checks that if there are no tasks for the specified date, the bot returns a corresponding notification."""
    user_id = 888

    message = MagicMock()
    message.chat.id = user_id
    message.from_user.id = user_id
    message.text = "/show today"

    with patch("my_bot.Telebot.bot") as mock_bot:
        from my_bot.Telebot import show

        show(message)

        expected_text = "📅 TODAY:\nNo tasks planned.\n\n"
        mock_bot.send_message.assert_called_with(user_id, expected_text)


def test_clear_command(db_session, create_task):
    """Checks the complete deletion of user tasks from the database."""
    user_id = 777
    create_task(user_id=user_id, text="Task to delete")

    message = MagicMock()
    message.chat.id = user_id
    message.from_user.id = user_id

    with patch.dict("os.environ", {"GEMINI_API_KEY": "fake_key"}):
        with patch("my_bot.Telebot.bot") as mock_bot:
            from my_bot.Telebot import clear_history

            clear_history(message)

    count = db_session.query(Task).filter_by(user_id=user_id).count()
    assert count == 0
    mock_bot.send_message.assert_called_with(
        user_id, "🧹 Your task history has been erased."
    )


def test_clear_history_error():
    """Checking for an error when clearing history."""
    message = MagicMock()
    message.chat.id = 777
    message.from_user.id = 777

    with patch("my_bot.models.SessionLocal", side_effect=Exception("DB Error")):
        from my_bot.Telebot import clear_history

        with pytest.raises(Exception, match="DB Error"):
            clear_history(message)


def test_random_command_success(db_session):
    """Checks that the bot selects a random task from the list and adds it to the database."""
    user_id = 999
    message = MagicMock()
    message.chat.id = user_id
    message.from_user.id = user_id

    with patch("my_bot.Telebot.bot") as mock_bot:
        from my_bot.Telebot import random_add, RANDOM_TASKS

        random_add(message)

        assert mock_bot.send_message.called
        args, _ = mock_bot.send_message.call_args
        sent_text = args[1]

        possible_texts = [t.split("@")[0].strip() for t in RANDOM_TASKS]
        assert any(pt in sent_text for pt in possible_texts)

        from my_bot.models import Task

        task_in_db = db_session.query(Task).filter_by(user_id=user_id).first()
        assert task_in_db is not None
        assert task_in_db.date == "tomorrow"
        assert task_in_db.text in possible_texts


def test_random_command_database_error(db_session):
    """Checks the bot's response if the database returns an error while saving."""
    user_id = 777
    message = MagicMock()
    message.chat.id = user_id
    message.from_user.id = user_id

    with patch("my_bot.models.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_db.add.side_effect = Exception("DB Connection Error")
        mock_session_local.return_value = mock_db

        with patch("my_bot.Telebot.bot") as mock_bot:
            from my_bot.Telebot import random_add

            random_add(message)

            mock_bot.send_message.assert_called_with(
                user_id, "⚠️ Error creating random task."
            )
            mock_db.rollback.assert_called_once()


@patch("my_bot.Telebot.get_new_chat")
@patch("my_bot.Telebot.bot")
def test_handle_gemini_chat_success(mock_bot, mock_get_chat):
    """Testing the AI's successful response to a random text message."""
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "AI Answer"
    mock_chat.send_message.return_value = mock_response
    mock_get_chat.return_value = mock_chat

    message = MagicMock()
    message.from_user.id = 123
    message.text = "Hello, help me with my day"
    message.chat.id = 123

    from my_bot.Telebot import handle_gemini_chat

    handle_gemini_chat(message)

    mock_bot.reply_to.assert_called_once_with(message, "AI Answer")


def test_handle_gemini_chat_no_user():
    """Checking for a situation where there is no user data in a message."""
    message = MagicMock()
    message.from_user = None

    with patch("my_bot.Telebot.logger") as mock_logger:
        from my_bot.Telebot import handle_gemini_chat

        handle_gemini_chat(message)
        mock_logger.warning.assert_called_with(
            "Received a message without a valid user_id"
        )


def test_handle_gemini_chat_error():
    """Check for error handling if the AI does not respond."""
    message = MagicMock()
    message.from_user.id = 123
    message.text = "Hello"
    message.chat.id = 123

    with patch("my_bot.Telebot.user_chats", {123: MagicMock()}):
        with patch("my_bot.Telebot.bot") as mock_bot:
            from my_bot.Telebot import handle_gemini_chat

            mock_chat = MagicMock()
            mock_chat.send_message.side_effect = Exception("AI Fail")

            with patch("my_bot.Telebot.user_chats", {123: mock_chat}):
                handle_gemini_chat(message)
                mock_bot.send_message.assert_called_with(
                    123,
                    "⚠️ Sorry, I'm having trouble processing your request right now. Please try again later.",
                )


def test_add_command_database_error(db_session):
    """Сhecks the handling of a database error when adding a task."""
    message = MagicMock()
    message.chat.id = 444
    message.from_user.id = 444
    message.text = "/add today Buy bread @Food"

    with patch("my_bot.models.SessionLocal", side_effect=Exception("DB Error")):
        from my_bot.Telebot import add

        with pytest.raises(Exception, match="DB Error"):
            add(message)
