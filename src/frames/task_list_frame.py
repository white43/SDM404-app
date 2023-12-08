import tkinter as tk

from events import Events

from src.dialogs import Dialogs
from src.entities import Task
from src.repositories import TaskRepository


class TaskListFrame(tk.Frame):
    """
    This class is responsible for logic of the task list page
    """
    def __init__(self, gui: tk.Tk, master: tk.Frame, events: Events, dialogs: Dialogs, task_repository: TaskRepository):
        tk.Frame.__init__(self, master)
        self.gui: tk.Tk = gui
        self.dialogs: Dialogs = dialogs
        self.events = events
        self.task_repository: TaskRepository = task_repository

    def reset_page(self) -> None:
        """
        Destroys all elements on the page to recreate them after saving or editing tasks
        """
        for child in self.grid_slaves():
            child.grid_forget()
            child.destroy()

    def draw_page(self) -> None:
        """
        Creates elements of the page from scratch: a table (list) and a button to add new tasks
        """
        entities = self.task_repository.get_all()

        self.grid_columnconfigure(1, weight=1)

        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, text="Title").grid(row=0, column=1)
        tk.Label(self, text="Due date").grid(row=0, column=2)
        tk.Label(self, text="Percent Ready").grid(row=0, column=3)
        tk.Label(self, text="Download").grid(row=0, column=4)
        tk.Label(self, text="Edit").grid(row=0, column=5)
        tk.Label(self, text="Delete").grid(row=0, column=6)

        row_id: int = 1

        for entity in entities:
            id = tk.Label(self, text=entity.id)
            title = tk.Label(self, text=entity.title)
            due_date = tk.Label(self, text=str(entity.due_date))
            percent_ready = tk.Label(self, text=str(entity.percent_ready))

            state = 'disabled' if entity.file_path is None else 'normal'

            download_button = tk.Button(self, text="Download", state=state, command=lambda eid=entity.id: self.download(eid))
            edit_button = tk.Button(self, text="Edit", command=lambda eid=entity.id: self.edit(eid))
            delete_button = tk.Button(self, name='delete' + str(row_id), text="Delete", command=lambda eid=entity.id, rid=row_id: self.delete(eid, rid))

            id.grid(row=row_id, column=0)
            title.grid(row=row_id, column=1)
            due_date.grid(row=row_id, column=2)
            percent_ready.grid(row=row_id, column=3)
            download_button.grid(row=row_id, column=4)
            edit_button.grid(row=row_id, column=5)
            delete_button.grid(row=row_id, column=6)

            row_id += 1

        tk.Button(self, name='add', text="Add Task", command=self.add).grid(row=row_id, column=4, columnspan=4)

    def redraw_page(self) -> None:
        """
        A shorthand method to call all necessary underlying methods to draw the page from scratch
        """
        self.set_title()
        self.reset_page()
        self.draw_page()

    def set_title(self):
        """
        This method changes the title of the page to Student Task Scheduler after navigating to the task list page
        """
        self.gui.title("Student Task Scheduler")

    def add(self):
        """
        This method is called to navigate to the add task page from the task list page
        """
        self.events.on_show_add_task_page()

    def edit(self, entity_id: int) -> None:
        """
        This method is called to navigate to the edit task page from the task list page
        """
        self.events.on_show_edit_task_page(entity_id)

    def delete(self, entity_id: int, row_id: int) -> None:
        """
        This method is called to remove from the database corresponding record from the task list page
        """
        entity = self.task_repository.get_by_id(entity_id)

        if isinstance(entity, Task) and self.task_repository.delete(entity):
            for child in self.grid_slaves(row=row_id):
                child.grid_forget()
                child.destroy()

    def download(self, entity_id: int):
        """
        This method will save your backup file on disk from the database
        """
        entity = self.task_repository.get_by_id(entity_id)

        if isinstance(entity, Task) and entity.file_path is not None:
            self.dialogs.restore_backup(entity)



