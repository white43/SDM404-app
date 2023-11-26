import datetime

from sqlalchemy import Date, SmallInteger, String
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from validation import ValidationException


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    percent_ready: Mapped[int] = mapped_column(SmallInteger)
    due_date: Mapped[datetime.date] = mapped_column(Date(), server_default=func.now())

    @validates("title")
    def validate_title(self, _: str, title: str) -> str:
        if title == "":
            raise ValidationException("task title must be specified")

        if len(title) > 100:
            raise ValidationException("task title must not exceed 100 characters")

        return title

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, title={self.title!r}, percent_ready={self.percent_ready!r}), due_date={self.due_date!r})"
