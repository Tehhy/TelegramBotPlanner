import pytest

from my_bot.Telebot import tasks


@pytest.fixture(autouse=True)
def clean_tasks():
    tasks.clear()
    yield
    tasks.clear()
