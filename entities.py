import datetime

from sqlalchemy import Date, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    percent_ready: Mapped[int] = mapped_column(SmallInteger)
    due_date: Mapped[datetime.date] = mapped_column(Date(), server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, title={self.title!r}, percent_ready={self.percent_ready!r}), due_date={self.due_date!r})"
