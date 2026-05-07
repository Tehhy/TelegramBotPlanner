from my_bot.models import Task, init_db


def test_init_db_execution():
    """Checks the database initialization function."""
    init_db()
    assert True


def test_task_defaults(db_session):
    """Checks that 'General' is automatically substituted."""
    task = Task(user_id=555, date="2026-01-01", text="Check defaults")
    db_session.add(task)
    db_session.commit()

    assert task.category == "General"


def test_task_structure(db_session):
    """Checks that all field types are saved."""
    task = Task(user_id=1, date="today", text="some long text", category="Work")
    db_session.add(task)
    db_session.flush()

    assert isinstance(task.id, int)
    assert task.text == "some long text"
