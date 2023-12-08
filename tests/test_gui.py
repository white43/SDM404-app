import os.path
import tkinter as tk
import unittest

from sqlalchemy import create_engine

from src.app import App, ListTasksPage, TaskPage
from src.entities import Base
from src.notifications import BaseNotification
from src.repositories import TaskRepository
from src.validation import TaskValidator

TITLE_FIELD_1 = "!entry"
TITLE_FIELD_2 = "!entry2"
ADD_TASK_BUTTON_1 = "!button"
SUBMIT_BUTTON_1 = "!button2"
SUBMIT_BUTTON_2 = "!button5"
DELETE_BUTTON_1 = "!button6"
DELETE_BUTTON_2 = "!button8"


class MyGui(unittest.TestCase):
    async def _start_app(self):
        self.gui.mainloop()

    def setUp(self) -> None:
        if os.path.exists("test.db"):
            os.remove("test.db")

        db = create_engine("sqlite:///test.db")
        task_repository = TaskRepository(db)
        task_validator = TaskValidator(task_repository)
        Base.metadata.create_all(db)
        notifications = BaseNotification()

        self.gui = tk.Tk()
        self.gui.geometry("640x480")

        App(self.gui, task_repository, task_validator, notifications)

        self._start_app()

    def tearDown(self) -> None:
        self.gui.destroy()

        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_main_user_path(self):
        title = self.gui.winfo_toplevel().title()
        expected = 'Student Task Scheduler'
        self.assertEqual(title, expected)

        top = self.gui.winfo_toplevel().children
        self.assertIsInstance(top['!frame'], tk.Frame)

        pages = top['!frame'].children

        self.assertIsInstance(pages['!listtaskspage'], ListTasksPage)
        self.assertIsInstance(pages['!taskpage'], TaskPage)

        list_tasks_page = pages['!listtaskspage']
        task_page = pages['!taskpage']

        # The window contains 7 elements (table head + add task button)
        self.assertEqual(7, len(list_tasks_page.children))

        # Simulate a click on the Add Task Button
        list_tasks_page.children[ADD_TASK_BUTTON_1].invoke()

        # The main window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Add Task | Student Task Scheduler'
        self.assertEqual(title, expected)

        # Empty task page should contain 8 elements
        self.assertEqual(10, len(task_page.children))

        # Insert text "Test" in to the title field
        task_page.children[TITLE_FIELD_1].delete(0, tk.END)
        task_page.children[TITLE_FIELD_1].insert(0, "Test")

        # Simulate a click on the Submit Button
        task_page.children[SUBMIT_BUTTON_1].invoke()

        # The window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Student Task Scheduler'
        self.assertEqual(title, expected)

        # The window contains 13 elements (table head + one row + add task button)
        self.assertEqual(13, len(list_tasks_page.children))

        # Simulate a click on the Add Task Button
        list_tasks_page.children['!button4'].invoke()

        # Insert text "Test" in to the title field
        task_page.children[TITLE_FIELD_2].delete(0, tk.END)
        task_page.children[TITLE_FIELD_2].insert(0, "Test2")

        # Simulate a click on the Submit Button
        task_page.children[SUBMIT_BUTTON_2].invoke()

        # The window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Student Task Scheduler'
        self.assertEqual(title, expected)

        # The window contains 19 elements (table head + two rows + add task button)
        self.assertEqual(19, len(list_tasks_page.children))

        # Simulate a click on the first Delete Button
        list_tasks_page.children[DELETE_BUTTON_1].invoke()

        # The window contains 13 elements (table head + one row + add task button)
        self.assertEqual(13, len(list_tasks_page.children))

        # Simulate a click on the second Delete Button
        list_tasks_page.children[DELETE_BUTTON_2].invoke()

        # The window contains 7 elements (table head + add task button)
        self.assertEqual(7, len(list_tasks_page.children))


if __name__ == '__main__':
    unittest.main()
