import os

from my_bot.Telebot import tasks


def test_telegram_token_is_set():
    """Check if pytest-env correctly injected the fake token from pyproject.toml"""
    token = os.environ.get("TELEGRAM_TOKEN")
    assert token is not None, "TELEGRAM_TOKEN not found in environment variables!"
    assert token == "12345:fake_token_for_tests", (
        "Token found, but it doesn't match the one in pyproject.toml"
    )


def test_tasks_is_empty_initially():
    """Check if the tasks dictionary is imported correctly and is empty (fixture check)"""
    # If the 'autouse=True' fixture is working, tasks will always be {} at the start
    assert isinstance(tasks, dict), "The 'tasks' object should be a dictionary"
    assert len(tasks) == 0, (
        "The 'tasks' dictionary should be empty at the start of the test"
    )
