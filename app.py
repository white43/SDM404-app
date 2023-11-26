import tkinter as tk
import tkcalendar as tkc

from tkinter import font
from repositories import TaskRepository
from entities import Task


class App:
    pages: dict[str, tk.Frame] = {}

    list_tasks_page = None
    add_task_page = None
    edit_task_page = None

    def __init__(self, gui: tk.Tk, task_repository: TaskRepository):
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(gui)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.list_tasks_page = ListTasksPage(gui=gui, parent=container, controller=self, task_repository=task_repository)
        self.add_task_page = AddTaskPage(gui=gui, parent=container, controller=self, task_repository=task_repository)
        self.edit_task_page = EditTaskPage(gui=gui, parent=container, controller=self, task_repository=task_repository)

        for page in (self.list_tasks_page, self.add_task_page, self.edit_task_page):
            page.grid(row=0, column=0, sticky="nsew")

        self.show_list_tasks_page()

    def show_list_tasks_page(self):
        self.list_tasks_page.tkraise()

    def show_edit_task_page(self, row_id: int):
        self.edit_task_page.redraw_page(row_id)
        self.edit_task_page.tkraise()


class ListTasksPage(tk.Frame):
    task_repository: TaskRepository

    def __init__(self, gui: tk.Tk, parent: tk.Frame, controller: App, task_repository: TaskRepository):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.task_repository = task_repository

        entities = task_repository.get_all()

        self.grid_columnconfigure(1, weight=1)

        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, text="Title").grid(row=0, column=1)
        tk.Label(self, text="Due date").grid(row=0, column=2)
        tk.Label(self, text="Percent Ready").grid(row=0, column=3)
        tk.Label(self, text="Edit").grid(row=0, column=4)
        tk.Label(self, text="Delete").grid(row=0, column=5)

        for entity in entities:
            id = tk.Label(self, text=entity.id)
            title = tk.Label(self, text=entity.title)
            due_date = tk.Label(self, text=str(entity.due_date))
            percent_ready = tk.Label(self, text=str(entity.percent_ready))

            edit_button = tk.Button(self, text="Edit", command=lambda val=entity.id: self.edit(val))
            delete_button = tk.Button(self, text="Delete", command=lambda val=entity.id: self.delete(val))

            id.grid(row=entity.id, column=0)
            title.grid(row=entity.id, column=1)
            due_date.grid(row=entity.id, column=2)
            percent_ready.grid(row=entity.id, column=3)
            edit_button.grid(row=entity.id, column=4)
            delete_button.grid(row=entity.id, column=5)

    def edit(self, row_id: int) -> None:
        self.controller.show_edit_task_page(row_id)
        pass

    def delete(self, row_id: int) -> None:
        entity = self.task_repository.get_by_id(row_id)

        if isinstance(entity, Task) and self.task_repository.delete(entity):
            for child in self.grid_slaves(row=row_id):
                child.grid_forget()


class AddTaskPage(tk.Frame):
    def __init__(self, gui: tk.Tk, parent: tk.Frame, controller: App, task_repository: TaskRepository):
        tk.Frame.__init__(self, parent)
        # self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame(ListTasksPage.__name__))
        button.pack()


class EditTaskPage(tk.Frame):
    gui: tk.Tk
    controller: App
    task_repository: TaskRepository

    entity: Task

    name_entry: tk.Entry
    due_date_entry: tk.Entry
    percent_ready_entry: tk.Scale

    def __init__(self, gui: tk.Tk, parent: tk.Frame, controller: App, task_repository: TaskRepository):
        tk.Frame.__init__(self, parent)
        self.gui = gui
        self.controller = controller
        self.task_repository = task_repository

    def reset_page(self) -> None:
        for child in self.grid_slaves():
            child.grid_forget()

    def draw_page(self, row_id: int) -> None:
        self.entity = self.task_repository.get_by_id(row_id)

        title = tk.StringVar()
        title.set(self.entity.title)
        percent_ready = tk.IntVar()
        percent_ready.set(self.entity.percent_ready)

        name_label = tk.Label(self, text='Title', font=('calibre', 10, 'bold'))
        self.name_entry = tk.Entry(self, textvariable=title, font=('calibre', 10, 'normal'))

        due_date_label = tk.Label(self, text='Due date', font=('calibre', 10, 'bold'))
        self.due_date_entry = tkc.DateEntry(self, date_pattern="dd-mm-yyyy")

        percent_ready_label = tk.Label(self, text='Due date', font=('calibre', 10, 'bold'))
        self.percent_ready_entry = tk.Scale(self, from_=0, to=100, variable=percent_ready, orient='horizontal')

        sub_btn = tk.Button(self, text='Submit', command=lambda: self.save())

        name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        due_date_label.grid(row=1, column=0)
        self.due_date_entry.grid(row=1, column=1)
        percent_ready_label.grid(row=2, column=0)
        self.percent_ready_entry.grid(row=2, column=1)
        sub_btn.grid(row=3, column=1)

    def redraw_page(self, row_id: int) -> None:
        self.reset_page()
        self.draw_page(row_id=row_id)

    def save(self):
        self.entity.title = self.name_entry.get()
        self.entity.percent_ready = self.percent_ready_entry.get()
