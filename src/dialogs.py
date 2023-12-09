import os
from io import BufferedWriter
from tkinter import filedialog, messagebox

from src.entities import Task


class Dialogs:
    filetypes = (
        ('PDF files', '*.pdf'),
        ('XSLX files', '*.xslx'),
        ('ODT files', '*.odt'),
        ('All files', '*.*'),
    )

    def save_backup(self) -> (str | None, int | None, bytes | None):
        """
        This method collects information about a file for further saving it in the database as a backup
        """
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir=os.path.expanduser("~"),
            filetypes=self.filetypes,
        )

        if isinstance(filename, str) and os.path.exists(filename):
            file_mtime = int(os.path.getmtime(filename))

            fd = open(filename, mode="rb")
            file_contents = fd.read()
            fd.close()

            return filename, file_mtime, file_contents

        return None, None, None

    def restore_backup(self, entity: Task) -> None:
        """
        This method takes a record from the database and saves its file contents to a location specified by the user
        """
        if isinstance(entity, Task) and entity.file_path is not None:
            file = None

            try:
                file = filedialog.asksaveasfile(
                    mode='wb',
                    title='Save as',
                    initialdir=os.path.expanduser("~"),
                    filetypes=self.filetypes,
                )
            except Exception as e:
                messagebox.showerror("Error", "Error occurred: " + str(e))

            if isinstance(file, BufferedWriter):
                written = file.write(entity.file_contents)
                file.close()

                if written > 0:
                    messagebox.showinfo("Success", "The file has been downloaded")
                else:
                    messagebox.showerror("Error", "Error occurred during writing file on disk")
