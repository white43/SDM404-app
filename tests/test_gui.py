import os.path
import tkinter as tk
import unittest

from events import Events
from sqlalchemy import create_engine

from src.app import App
from src.dialogs import Dialogs
from src.entities import Base
from src.frames.task_frame import TaskFrame
from src.frames.task_list_frame import TaskListFrame
from src.gui import gui
from src.notifications import BaseNotification
from src.repositories import TaskRepository
from src.validation import TaskValidator

TITLE_FIELD_1 = "!entry"
TITLE_FIELD_2 = "!entry2"


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
        dialogs = Dialogs()
        self.gui, main_frame = gui()
        self.events = Events()

        task_list_frame = TaskListFrame(self.gui, main_frame, self.events, dialogs, task_repository)
        task_frame = TaskFrame(self.gui, main_frame, self.events, dialogs, task_repository, task_validator, notifications)

        app = App(task_list_frame, task_frame)

        self.events.on_show_list_tasks_page += app.show_list_tasks_page
        self.events.on_show_add_task_page += app.show_add_task_page
        self.events.on_show_edit_task_page += app.show_edit_task_page

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

        self.assertIsInstance(pages['!tasklistframe'], TaskListFrame)
        self.assertIsInstance(pages['!taskframe'], TaskFrame)

        task_list_page = pages['!tasklistframe']
        task_page = pages['!taskframe']

        # The window contains 8 elements (table head + add task button)
        self.assertEqual(8, len(task_list_page.children))

        # Simulate a click on the Add Task Button
        task_list_page.children['add'].invoke()

        # The main window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Add Task | Student Task Scheduler'
        self.assertEqual(title, expected)

        # Empty task page should contain 11 elements
        self.assertEqual(11, len(task_page.children))

        # Insert text "Test" in to the title field
        task_page.children[TITLE_FIELD_1].delete(0, tk.END)
        task_page.children[TITLE_FIELD_1].insert(0, "Test")

        # Simulate a click on the Submit Button
        task_page.children['submit'].invoke()

        # The window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Student Task Scheduler'
        self.assertEqual(title, expected)

        # The window contains 15 elements (table head + one row + add task button)
        self.assertEqual(15, len(task_list_page.children))

        # Simulate a click on the Add Task Button
        task_list_page.children['add'].invoke()

        # Insert text "Test" in to the title field
        task_page.children[TITLE_FIELD_2].delete(0, tk.END)
        task_page.children[TITLE_FIELD_2].insert(0, "Test2")

        # Simulate a click on the Submit Button
        task_page.children['submit'].invoke()

        # The window should change its title
        title = self.gui.winfo_toplevel().title()
        expected = 'Student Task Scheduler'
        self.assertEqual(title, expected)

        # The window contains 22 elements (table head + two rows + add task button)
        self.assertEqual(22, len(task_list_page.children))

        # Simulate a click on the first Delete Button
        task_list_page.children['delete1'].invoke()

        # The window contains 15 elements (table head + one row + add task button)
        self.assertEqual(15, len(task_list_page.children))

        # Simulate a click on the second Delete Button
        task_list_page.children['delete2'].invoke()

        # The window contains 8 elements (table head + add task button)
        self.assertEqual(8, len(task_list_page.children))


if __name__ == '__main__':
    unittest.main()
