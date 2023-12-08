import tkinter as tk

from notifypy import Notify
from sqlalchemy import create_engine

from src.app import App
from src.entities import Base
from src.notifications import Notification
from src.repositories import TaskRepository
from src.validation import TaskValidator

if __name__ == '__main__':
    db = create_engine("sqlite:///foo.db", echo=True)
    task_repository = TaskRepository(db)
    task_validator = TaskValidator(task_repository)
    Base.metadata.create_all(db)
    notifications = Notification(Notify(enable_logging=True))

    gui = tk.Tk()
    gui.geometry("640x480")

    app = App(gui, task_repository, task_validator, notifications)

    gui.mainloop()

