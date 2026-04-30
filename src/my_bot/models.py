import os
from sqlalchemy import create_engine, String, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/todo.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    date: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)


def init_db() -> None:
    db_path = "./data"
    if DATABASE_URL.startswith("sqlite:///./data") and not os.path.exists(db_path):
        os.makedirs(db_path)

    Base.metadata.create_all(bind=engine)
