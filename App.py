import tkinter as tk
from tkinter import ttk, Label, DISABLED, NORMAL, W, E
from tkinter.filedialog import askopenfilename
from typing import Optional
import ttkbootstrap as tb

import pandas as pd

from Components.EntryWithPlaceholder import EntryWithPlaceholder
from State import State

# state: State = State()


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.state = State()
        self.state.register_callback(self.stated_updated)
        self.title("Main menu")
        self.geometry('600x400')
        ttk.Label(self, text='Main Menu').grid(row=0)
        self.input_logscreen = EntryWithPlaceholder(self, "Path to log file")
        self.input_logscreen.grid(row=1, column=0)
        button_logscreen = ttk.Button(self, text='Import log file', command=self.open_logscreen)
        button_logscreen.grid(row=1, column=1)
        # button_logscreen.pack(expand=True)
        input_video = EntryWithPlaceholder(self, placeholder="Path to video")
        input_video.grid(row=2, column=0)
        button2 = ttk.Button(self, text='Import video', command=self.open_videoscreen)
        button2.grid(row=2, column=1)
        self.vars_label = ttk.Label(self, text=f"{self.state.vars}")
        # self.vars_label.pack(expand=True)

    def stated_updated(self, _state: State):
        self.state = _state
        self.vars_label.config(text=f"{self.state.vars}")
        if _state.filename:
            self.input_logscreen.destroy()
            self.input_logscreen = EntryWithPlaceholder(self, _state.filename)
            self.input_logscreen.grid(row=1, column=0)

    def open_logscreen(self):
        self.LogScreen(self.state)

    def open_videoscreen(self):
        self.VideoSelectScreen(self.state)


    class LogScreen(tk.Toplevel):

        check_vars: Optional[dict[str, tk.BooleanVar]]

        def __init__(self, state: State):
            super().__init__()
            self.state = state
            self.check_vars = None
            self.filename = None
            self.title("Select log file")
            self.geometry('600x400')
            button = ttk.Button(self, text="Select expedition log file",
                                command=self.select_logfile)
            button.grid(column=2, row=0)
            self.l = Label(self, text="No file selected")
            self.l.grid(column=2, row=1)
            self.ok_button = ttk.Button(self, text="Confirm", state=DISABLED)
            self.ok_button.grid(column=6, row=2, sticky=E)

        def select_logfile(self):
            self.filename = askopenfilename(parent=self, filetypes=[("cvs", "*.csv")])
            self.l.destroy()
            self.l = Label(self, text=f"Selected: {self.filename}")
            self.l.grid(column=1, row=1)
            self.state.filename = self.filename
            self.generate_checkbox(self.filename)

        def confirm_log_file(self):
            for var in self.check_vars.keys():
                if self.check_vars[var].get():
                    self.state.add_var(var)
            self.destroy()

        def generate_checkbox(self, filename):
            df = pd.read_csv(filename, low_memory=False)
            all_variables = df.columns.tolist()
            # Create a dictionary to hold the Checkbutton variables
            self.check_vars = {var: tk.BooleanVar() for var in all_variables}

            # Create a check button for each variable
            checkbuttons: list[tuple[str, tk.Checkbutton]] = (
                list(map(lambda var: (
                var, tk.Checkbutton(self, text=var, variable=self.check_vars[var])),
                         all_variables)))
            col = 0
            row = 2
            for (_, btn) in checkbuttons:
                btn.grid(row=row, column=col, sticky=W, pady=2)
                col = col + 1
                if col > 5:
                    col = 0
                    row = row + 1
            self.ok_button.destroy()
            self.ok_button = ttk.Button(self, text="Confirm", state=NORMAL,
                                        command=self.confirm_log_file)
            self.ok_button.grid(row=row, column=col + 1, sticky=E)

    class VideoSelectScreen(tk.Toplevel):
        def __init__(self, state: State):
            super().__init__()
            self.state = state
            self.geometry('600x400')
            self.title("Select video file")
            button = ttk.Button(self, text="Select expedition log file",
                                command=self.select_video)
            button.grid(column=2, row=0)
            self.l = Label(self, text="No file selected")
            self.l.grid(column=2, row=1)
            self.ok_button = ttk.Button(self, text="Confirm", state=DISABLED)
            self.ok_button.grid(column=6, row=2, sticky=E)


        def select_video(self):
            self.filename = askopenfilename(parent=self, filetypes=[("mp4", "*.mp4")])
            self.l.destroy()
            self.l = Label(self, text=f"Selected: {self.filename}")
            self.l.grid(column=1, row=1)
            self.state.video = self.filename
            self.ok_button['state'] = NORMAL
