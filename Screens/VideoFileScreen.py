import tkinter as tk
from tkinter import DISABLED, ttk, NORMAL, E
from tkinter.filedialog import askopenfilename

from State import State


class VideoFileScreen(tk.Toplevel):
    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.geometry('600x400')
        self.title("Select video file")
        button = ttk.Button(self, text="Select expedition log file",
                            command=self.select_video)
        button.grid(column=2, row=0)
        self.l = tk.Label(self, text="No file selected")
        self.l.grid(column=2, row=1)
        self.ok_button = ttk.Button(self, text="Confirm", state=DISABLED)
        self.ok_button.grid(column=6, row=2, sticky=E)

    def select_video(self):
        self.filename = askopenfilename(parent=self, filetypes=[("mp4", "*.mp4")])
        self.l.destroy()
        self.l = tk.Label(self, text=f"Selected: {self.filename}")
        self.l.grid(column=1, row=1)
        self.state.video = self.filename
        self.ok_button['state'] = NORMAL
