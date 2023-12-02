import tkinter as tk

from notifypy import Notify
from sqlalchemy import create_engine

from app import App
from entities import Base
from notifications import Notification
from repositories import TaskRepository

if __name__ == '__main__':
    db = create_engine("sqlite:///foo.db", echo=True)
    task_repository = TaskRepository(db)
    Base.metadata.create_all(db)
    notifications = Notification(Notify(enable_logging=True))

    gui = tk.Tk()
    gui.geometry("640x480")

    app = App(gui, task_repository, notifications=notifications)

    gui.mainloop()

