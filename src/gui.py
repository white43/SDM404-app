import tkinter as tk


def gui():
    gui = tk.Tk()
    gui.geometry("640x480")

    master_frame = tk.Frame(gui)
    master_frame.pack(side="top", fill="both", expand=True)
    master_frame.grid_rowconfigure(0, weight=1)
    master_frame.grid_columnconfigure(0, weight=1)

    return gui, master_frame
