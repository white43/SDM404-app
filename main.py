import tkinter as tk

from sqlalchemy import create_engine
from repositories import TaskRepository
from entities import Base
from app import App

if __name__ == '__main__':
    db = create_engine("sqlite:///foo.db", echo=True)
    task_repository = TaskRepository(db)
    Base.metadata.create_all(db)

    gui = tk.Tk()
    gui.geometry("640x480")

    app = App(gui, task_repository)

    gui.mainloop()

