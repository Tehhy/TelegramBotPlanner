from unittest.mock import ANY, MagicMock, patch

from my_bot.Telebot import add, help, tasks


def test_help_command():
    message = MagicMock()
    message.chat.id = 111

    with patch("my_bot.Telebot.bot") as mock_bot:
        help(message)
        mock_bot.send_message.assert_called_with(111, ANY)


def test_add_command_valid_format():
    message = MagicMock()
    message.chat.id = 222
    message.text = "/add tomorrow Buy bread @Food"

    with patch("my_bot.Telebot.bot"):
        add(message)

    assert "tomorrow" in tasks
    assert "Buy bread @Food" in tasks["tomorrow"]


def test_add_command_invalid_format():
    message = MagicMock()
    message.chat.id = 333
    message.text = "/add"  # Incorrect format

    with patch("my_bot.Telebot.bot") as mock_bot:
        add(message)
        mock_bot.send_message.assert_called_with(
            333, "Invalid command format. Use: /add <date> <task> @<category>"
        )
