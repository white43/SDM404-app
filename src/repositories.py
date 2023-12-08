from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from src.entities import Task


class TaskRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session = Session(self.engine)

    def get_by_id(self, task_id: int) -> Task | None:
        """
        This method is for getting information about a task from the database by its ID
        """
        stmt = select(Task).where(Task.id == task_id)
        entity = self.session.scalars(stmt).one_or_none()

        return entity

    def title_already_present_in_database(self, title: str) -> bool:
        """
        This method check whether the given title is already present in the database or not
        """
        stmt = select(Task).where(Task.title == title)
        entity = self.session.scalars(stmt).one_or_none()

        return False if entity is None else True

    def get_all(self) -> list[Task]:
        """
        This method return all the tasks saved in the database for displaying in the main page
        """
        stmt = select(Task)
        entities = self.session.scalars(stmt).all()

        return entities

    def insert(self, entity: Task) -> Task:
        """
        This method creates a new record in the database from the given entity object
        """
        self.session.add(entity)
        self.session.commit()

        return entity

    def update(self, entity: Task) -> Task:
        """
        This method updates a record in the database from the given entity object
        """
        self.session.add(entity)
        self.session.commit()

        return entity

    def delete(self, entity: Task) -> bool:
        """
        This method removes from the database a record associated with the given entity object
        """
        self.session.delete(entity)
        self.session.commit()

        return True
