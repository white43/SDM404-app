from sqlalchemy import BLOB

from src.entities import Task
from src.repositories import TaskRepository


class ValidationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TaskValidator:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def validate_entity(self, entity: Task, mode: str = "insert"):
        self.validate_title(entity.title, mode)

    def validate_title(self, title: str, mode: str):
        if title == "":
            raise ValidationException("Task title must be specified")

        if len(title) > 100:
            raise ValidationException("Task title must not exceed 100 characters")

        if mode == "insert" and self.task_repository.title_already_present_in_database(title):
            raise ValidationException("Task title must be unique. Enter another title")
