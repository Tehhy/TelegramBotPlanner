import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_bot.models import Base


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(engine):
    """Creates tables once for the entire test session."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Creates a new session for each test and rolls it back after completion."""
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def mock_db(monkeypatch, db_session):
    """Automatically replaces SessionLocal in the code with a test session."""
    monkeypatch.setattr("my_bot.Telebot.models.SessionLocal", lambda: db_session)
