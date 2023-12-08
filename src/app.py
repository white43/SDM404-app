import os.path
import sys
import tkinter as tk
from datetime import date
from tkinter import font, messagebox, filedialog

import tkcalendar as tkc

from src.entities import Task
from src.notifications import BaseNotification
from src.repositories import TaskRepository
from src.validation import ValidationException, TaskValidator


class App:
    pages: dict[str, tk.Frame] = {}

    list_tasks_page = None
    task_page = None

    def __init__(self, gui: tk.Tk, task_repository: TaskRepository, task_validator: TaskValidator, notifications: BaseNotification):
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(gui)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.list_tasks_page = ListTasksPage(
            gui=gui,
            parent=container,
            controller=self,
            task_repository=task_repository,
        )

        self.task_page = TaskPage(
            gui=gui,
            parent=container,
            controller=self,
            task_repository=task_repository,
            task_validator=task_validator,
            notifications=notifications,
        )

        for page in (self.list_tasks_page, self.task_page):
            page.grid(row=0, column=0, sticky="nsew")

        self.show_list_tasks_page()

    def show_list_tasks_page(self):
        self.list_tasks_page.redraw_page()
        self.list_tasks_page.tkraise()

    def show_add_task_page(self):
        self.task_page.redraw_page(None)
        self.task_page.tkraise()

    def show_edit_task_page(self, row_id: int | None):
        self.task_page.redraw_page(row_id)
        self.task_page.tkraise()


class ListTasksPage(tk.Frame):
    gui: tk.Tk
    controller: App
    task_repository: TaskRepository

    def __init__(self, gui: tk.Tk, parent: tk.Frame, controller: App, task_repository: TaskRepository):
        tk.Frame.__init__(self, parent)
        self.gui = gui
        self.controller = controller
        self.task_repository = task_repository

    def reset_page(self) -> None:
        for child in self.grid_slaves():
            child.grid_forget()
            child.destroy()

    def draw_page(self) -> None:
        entities = self.task_repository.get_all()

        self.grid_columnconfigure(1, weight=1)

        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, text="Title").grid(row=0, column=1)
        tk.Label(self, text="Due date").grid(row=0, column=2)
        tk.Label(self, text="Percent Ready").grid(row=0, column=3)
        tk.Label(self, text="Edit").grid(row=0, column=4)
        tk.Label(self, text="Delete").grid(row=0, column=5)

        row_id: int = 1

        for entity in entities:
            id = tk.Label(self, text=entity.id)
            title = tk.Label(self, text=entity.title)
            due_date = tk.Label(self, text=str(entity.due_date))
            percent_ready = tk.Label(self, text=str(entity.percent_ready))

            edit_button = tk.Button(self, text="Edit", command=lambda eid=entity.id: self.edit(eid))
            delete_button = tk.Button(self, text="Delete", command=lambda eid=entity.id, rid=row_id: self.delete(eid, rid))

            id.grid(row=row_id, column=0)
            title.grid(row=row_id, column=1)
            due_date.grid(row=row_id, column=2)
            percent_ready.grid(row=row_id, column=3)
            edit_button.grid(row=row_id, column=4)
            delete_button.grid(row=row_id, column=5)

            row_id += 1

        tk.Button(self, text="Add Task", command=self.add).grid(row=row_id, column=4, columnspan=2)

    def redraw_page(self) -> None:
        self.set_title()
        self.reset_page()
        self.draw_page()

    def set_title(self):
        self.gui.title("Student Task Scheduler")

    def add(self):
        self.controller.show_add_task_page()

    def edit(self, entity_id: int) -> None:
        self.controller.show_edit_task_page(entity_id)
        pass

    def delete(self, entity_id: int, row_id: int) -> None:
        entity = self.task_repository.get_by_id(entity_id)

        if isinstance(entity, Task) and self.task_repository.delete(entity):
            for child in self.grid_slaves(row=row_id):
                child.grid_forget()
                child.destroy()


class TaskPage(tk.Frame):
    gui: tk.Tk
    controller: App
    task_repository: TaskRepository
    task_validator: TaskValidator

    entity: Task

    name_entry: tk.Entry
    due_date_entry: tkc.DateEntry
    percent_ready_entry: tk.Scale
    file_path: str | None = None
    file_contents: bytes | None = None

    def __init__(
            self,
            gui: tk.Tk,
            parent: tk.Frame,
            controller: App,
            task_repository: TaskRepository,
            task_validator: TaskValidator,
            notifications: BaseNotification,
    ):
        tk.Frame.__init__(self, parent)
        self.gui = gui
        self.controller = controller
        self.task_repository = task_repository
        self.task_validator = task_validator
        self.notifications = notifications

    def reset_page(self) -> None:
        for child in self.grid_slaves():
            child.grid_forget()
            child.destroy()

    def draw_page(self, row_id: int | None) -> None:
        title: tk.StringVar = tk.StringVar()
        due: date = date.today()
        percent_ready = tk.IntVar()

        if row_id is not None:
            self.entity = self.task_repository.get_by_id(row_id)

            title.set(self.entity.title)
            due = self.entity.due_date
            percent_ready.set(self.entity.percent_ready)
        else:
            self.entity = Task()

        name_label = tk.Label(self, text='Title', font=('calibre', 10, 'bold'))
        self.name_entry = tk.Entry(self, textvariable=title, font=('calibre', 10, 'normal'))

        due_date_label = tk.Label(self, text='Due date', font=('calibre', 10, 'bold'))
        self.due_date_entry = tkc.DateEntry(self, year=due.year, month=due.month, day=due.day,
                                            date_pattern="dd-mm-yyyy", mindate=date.today())

        percent_ready_label = tk.Label(self, text='Percent Ready', font=('calibre', 10, 'bold'))
        self.percent_ready_entry = tk.Scale(self, from_=0, to=100, variable=percent_ready, orient='horizontal')

        file_label = tk.Label(self, text="Add file", font=('calibre', 10, 'bold'))
        self.file_entry = tk.Button(self, text="File", command=lambda: self.select_file())
        sub_btn = tk.Button(self, text='Submit', command=lambda: self.save(True if row_id is not None else False))
        cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.cancel())

        name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        due_date_label.grid(row=1, column=0)
        self.due_date_entry.grid(row=1, column=1)
        percent_ready_label.grid(row=2, column=0)
        self.percent_ready_entry.grid(row=2, column=1)
        file_label.grid(row=3, column=0)
        self.file_entry.grid(row=3, column=1)
        sub_btn.grid(row=4, column=0)
        cancel_btn.grid(row=4, column=1)

    def redraw_page(self, row_id: int | None) -> None:
        self.reset_page()
        self.set_title(row_id)
        self.draw_page(row_id)

    def set_title(self, row_id: int | None):
        if row_id is None:
            self.gui.title("Add Task | Student Task Scheduler")
        else:
            self.gui.title("Edit Task | Student Task Scheduler")

    def save(self, update: bool):
        try:
            self.entity.title = self.name_entry.get()
            self.entity.due_date = self.due_date_entry.get_date()
            self.entity.percent_ready = self.percent_ready_entry.get()

            if self.file_path is not None and len(self.file_path) > 0:
                self.entity.file_path = self.file_path

            if self.file_contents is not None and len(self.file_contents) > 0:
                self.entity.file_contents = self.file_contents

            if update:
                self.task_validator.validate_entity(self.entity, "update")
                self.task_repository.update(self.entity)
            else:
                self.task_validator.validate_entity(self.entity, "insert")
                self.task_repository.insert(self.entity)

                self.notifications.info(
                    "New task",
                    "A new task %s with due date on %s has been added" % (
                    self.entity.title, self.entity.due_date.strftime("%d/%m/%Y"))
                )

            self.controller.show_list_tasks_page()
        except ValidationException as e:
            messagebox.showerror("Error", e.message)
        except Exception as e:
            messagebox.showerror("Error", "Error occurred")
            print("Error: could not save " + repr(e), file=sys.stderr)

    def cancel(self):
        self.controller.show_list_tasks_page()

    def select_file(self):
        filetypes = (
            ('PDF files', '*.pdf'),
            ('XSLX files', '*.xslx'),
            ('ODT files', '*.odt'),
            ('All files', '*.*'),
        )

        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes,
        )

        if os.path.exists(filename):
            self.file_path = filename

            fd = open(filename, mode="rb")
            self.file_contents = fd.read()
