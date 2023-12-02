from copy import deepcopy

from notifypy import Notify

from utils import resource_path


class BaseNotification:
    def info(self, title: str, message: str) -> None:
        pass


class Notification(BaseNotification):
    notifier: Notify

    def __init__(self, notifier: Notify):
        self.notifier = notifier

    def info(self, title: str, message: str) -> None:
        notifier = deepcopy(self.notifier)
        notifier.title = title
        notifier.message = message
        notifier.application_name = "Student Task Scheduler"
        notifier.icon = resource_path("assets", "information-icon.png")
        notifier.send(block=False)
