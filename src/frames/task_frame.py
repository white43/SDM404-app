import os
import sys
import tkinter as tk
from datetime import date
from tkinter import messagebox, filedialog

import tkcalendar as tkc
from events import Events

from src.entities import Task
from src.notifications import BaseNotification, Notification
from src.repositories import TaskRepository
from src.validation import TaskValidator, ValidationException


class TaskFrame(tk.Frame):
    """
    This class is responsible for logic of the add and edit page
    """
    entity: Task

    name_entry: tk.Entry
    due_date_entry: tkc.DateEntry
    percent_ready_entry: tk.Scale
    file_path: str | None = None
    file_contents: bytes | None = None

    def __init__(
            self,
            gui: tk.Tk,
            master: tk.Frame,
            events: Events,
            task_repository: TaskRepository,
            task_validator: TaskValidator,
            notifications: BaseNotification,
    ):
        """
        The constructor of the add or edit task page
        """
        tk.Frame.__init__(self, master)
        self.gui: tk.Tk = gui
        self.events: Events = events
        self.task_repository: TaskRepository = task_repository
        self.task_validator: TaskValidator = task_validator
        self.notifications: BaseNotification = notifications

    def reset_page(self) -> None:
        """
        A shorthand method to call all necessary underlying methods to draw the page from scratch
        """
        for child in self.grid_slaves():
            child.grid_forget()
            child.destroy()

    def draw_page(self, row_id: int | None) -> None:
        """
        This class creates the add or edit page from scratch depending on which page was requested
        """
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
        self.due_date_entry = tkc.DateEntry(self, year=due.year, month=due.month, day=due.day, date_pattern="dd-mm-yyyy", mindate=date.today())

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
        """
        Destroys all elements on the page to recreate them after saving or editing tasks
        """
        self.reset_page()
        self.set_title(row_id)
        self.draw_page(row_id)

    def set_title(self, row_id: int | None):
        """
        This method changes the title of the page to Add Task or Edit Task depending on which the user is navigating
        """
        if row_id is None:
            self.gui.title("Add Task | Student Task Scheduler")
        else:
            self.gui.title("Edit Task | Student Task Scheduler")

    def save(self, update: bool):
        """
        This method creates a new record or updates a record depending on which page the user is using
        """
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

            self.events.on_show_list_tasks_page()
        except ValidationException as e:
            messagebox.showerror("Error", e.message)
        except Exception as e:
            messagebox.showerror("Error", "Error occurred")
            print("Error: could not save " + repr(e), file=sys.stderr)

    def cancel(self):
        """
        This method sends users back to the task list page
        """
        self.events.on_show_list_tasks_page()

    def select_file(self):
        """
        This method the file chosen by the user and writes its content for further saving to the database
        """
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
