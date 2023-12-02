from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from entities import Task


class TaskRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session = Session(self.engine)

    def get_by_id(self, task_id: int) -> Task | None:
        stmt = select(Task).where(Task.id == task_id)
        entity = self.session.scalars(stmt).one_or_none()

        return entity

    def get_all(self) -> list[Task]:
        stmt = select(Task)
        entities = self.session.scalars(stmt).all()

        return entities

    def insert(self, entity: Task) -> Task:
        self.session.add(entity)
        self.session.commit()

        return entity

    def update(self, entity: Task) -> Task:
        self.session.add(entity)
        self.session.commit()

        return entity

    def delete(self, entity: Task) -> bool:
        self.session.delete(entity)
        self.session.commit()

        return True
