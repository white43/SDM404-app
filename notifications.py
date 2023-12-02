import os

from notifypy import Notify


class Notification:
    notifier: Notify

    def __init__(self, notifier: Notify):
        self.notifier = notifier

    def info(self, title: str, message: str):
        self.notifier.send_notification(
            supplied_title=title,
            supplied_message=message,
            supplied_application_name="Student Task Scheduler",
            supplied_urgency="normal",
            supplied_icon_path=os.path.join(os.getcwd(), "assets", "information-icon.png"),
            supplied_audio_path="",
        )
