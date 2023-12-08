from sqlalchemy import BLOB

from src.entities import Task
from src.repositories import TaskRepository


class ValidationException(Exception):
    """
    This as a base Exception will be used for displaying messages to end users
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TaskValidator:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def validate_entity(self, entity: Task, mode: str = "insert"):
        """
        This is a base method called for validation an entity object. It will call other methods to validate fields
        """
        self.validate_title(entity.title, mode)

    def validate_title(self, title: str, mode: str):
        """
        This method is responsible for validation the title field for the requirements
        """
        if title == "":
            raise ValidationException("Task title must be specified")

        if len(title) > 100:
            raise ValidationException("Task title must not exceed 100 characters")

        if mode == "insert" and self.task_repository.title_already_present_in_database(title):
            raise ValidationException("Task title must be unique. Enter another title")
