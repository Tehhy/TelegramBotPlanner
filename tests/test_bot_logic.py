from my_bot.Telebot import add_todo, tasks


def test_add_todo_new_date():
    # Clearing the dictionary before the test
    tasks.clear()
    add_todo("today", "Buy milk @Shopping")
    assert "today" in tasks
    assert tasks["today"] == ["Buy milk @Shopping"]


def test_add_todo_existing_date():
    tasks.clear()
    add_todo("today", "Task 1")
    add_todo("today", "Task 2")
    assert len(tasks["today"]) == 2
    assert "Task 2" in tasks["today"]
