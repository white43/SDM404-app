from tkinter import font

from src.frames.task_frame import TaskFrame
from src.frames.task_list_frame import TaskListFrame


class App:
    """
    This is a base class of the application. It is initialized in the main.app and hold all other classes needed for the
    application.
    """
    def __init__(self, task_list_frame: TaskListFrame, task_frame: TaskFrame):
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.task_list_frame: TaskListFrame = task_list_frame
        self.task_frame: TaskFrame = task_frame

        for frame in [self.task_list_frame, self.task_frame]:
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_list_tasks_page()

    def show_list_tasks_page(self):
        """
        A shorthand method to navigate to the task list page
        """
        self.task_list_frame.redraw_page()
        self.task_list_frame.tkraise()

    def show_add_task_page(self):
        """
        A shorthand method to navigate to the add task page
        """
        self.task_frame.redraw_page(None)
        self.task_frame.tkraise()

    def show_edit_task_page(self, row_id: int | None):
        """
        A shorthand method to navigate to the edit task page
        """
        self.task_frame.redraw_page(row_id)
        self.task_frame.tkraise()
