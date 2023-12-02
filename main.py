import tkinter as tk

from notifypy import Notify
from sqlalchemy import create_engine

from app import App
from entities import Base
from notifications import Notification
from repositories import TaskRepository
from validation import TaskValidator

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

