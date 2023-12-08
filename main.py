from events import Events
from notifypy import Notify
from sqlalchemy import create_engine

from src.app import App, TaskListFrame
from src.dialogs import Dialogs
from src.entities import Base
from src.frames.task_frame import TaskFrame
from src.gui import gui
from src.notifications import Notification
from src.repositories import TaskRepository
from src.validation import TaskValidator

if __name__ == '__main__':
    """
    This is the main file of the application. It initializes core components need for the application:
    1. database object
    2. task repository object
    3. task validation object
    4. notification object
    5. GUI related objects (Tkinter and the main frame)
    6. application frames
    7. event handler 
    """

    db = create_engine("sqlite:///foo.db", echo=True)
    task_repository = TaskRepository(db)
    task_validator = TaskValidator(task_repository)
    Base.metadata.create_all(db)
    notifications = Notification(Notify(enable_logging=True))
    dialogs = Dialogs()
    gui, master_frame = gui()
    events = Events()

    task_list_frame = TaskListFrame(gui, master_frame, events, dialogs, task_repository)
    task_frame = TaskFrame(gui, master_frame, events, dialogs, task_repository, task_validator, notifications)

    app = App(task_list_frame, task_frame)

    events.on_show_list_tasks_page += app.show_list_tasks_page
    events.on_show_add_task_page += app.show_add_task_page
    events.on_show_edit_task_page += app.show_edit_task_page

    gui.mainloop()

