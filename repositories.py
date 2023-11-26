from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from entities import Task


class TaskRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_by_id(self, task_id: int) -> Task | None:
        session = Session(self.engine)
        stmt = select(Task).where(Task.id == task_id)
        entity = session.scalars(stmt).one_or_none()
        session.close()

        return entity

    def get_all(self) -> list[Task]:
        session = Session(self.engine)
        stmt = select(Task)
        entities = session.scalars(stmt).all()
        session.close()

        return entities

    def insert(self, entity: Task) -> Task:
        with Session(self.engine) as session:
            session.add(entity)
            session.commit()
            session.close()

        return entity

    def update(self, entity: Task) -> Task:
        with Session(self.engine) as session:
            session.commit()
            session.close()

        return entity

    def delete(self, entity: Task) -> bool:
        with Session(self.engine) as session:
            session.delete(entity)
            session.commit()
            session.close()

        return True
