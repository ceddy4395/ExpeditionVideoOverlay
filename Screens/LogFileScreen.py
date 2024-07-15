import tkinter as tk
from tkinter import DISABLED, ttk, NORMAL, E
from tkinter.filedialog import askopenfilename
from typing import Optional

import pandas as pd

from State import State


class LogFileScreen(tk.Toplevel):
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
        self.l = tk.Label(self, text="No file selected")
        self.l.grid(column=2, row=1)
        self.ok_button = ttk.Button(self, text="Confirm", state=DISABLED)
        self.ok_button.grid(column=6, row=2, sticky=E)

    def select_logfile(self):
        self.filename = askopenfilename(parent=self, filetypes=[("cvs", "*.csv")])
        self.l.destroy()
        self.l = tk.Label(self, text=f"Selected: {self.filename}")
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
