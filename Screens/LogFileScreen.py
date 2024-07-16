import tkinter as tk
from tkinter import DISABLED, ttk, NORMAL, E
from tkinter.constants import W, X, YES, N, LEFT
from tkinter.filedialog import askopenfilename
from typing import Optional, Any
from ttkbootstrap.constants import *
import ttkbootstrap as tb


import pandas as pd

from State import State


class LogFileScreen(tk.Toplevel):
    check_vars: Optional[list[tuple[Any, tk.BooleanVar]]]

    def __init__(self, state: State):
        super().__init__()
        self.state = state
        self.check_vars = None
        self.filename = None
        self.title("Select log file")

        self.path_var = tk.StringVar(value="")

        option_text = "Complete the form to begin your search"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES, pady=5)
        path_lbl = ttk.Label(path_row, text="Path", width=8)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)

        self.checkbox_frame = tk.Frame(self)
        self.checkbox_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)

        browse_btn = ttk.Button(
            master=path_row,
            text="Browse",
            command=self.select_logfile,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15,10))
        self.ok_button = tb.Button(
            master=container,
            text="Go!",
            bootstyle=SUCCESS,
            width=6,
        )
        self.ok_button.pack(side=RIGHT, padx=5)

    def select_logfile(self):
        self.filename = askopenfilename(parent=self, filetypes=[("cvs", "*.csv")])
        if self.filename:
            self.path_var.set(self.filename)
        self.generate_checkbox(self.filename)

    def confirm_log_file(self):
        for var in self.check_vars:
            if var[1].get():
                self.state.add_var(var[0])
        self.destroy()

    def generate_checkbox(self, filename):
        df = pd.read_csv(filename, low_memory=False)
        all_variables = df.columns.tolist()
        # Create a dictionary to hold the Checkbutton variables
        self.check_vars = [(var, tk.BooleanVar()) for var in all_variables]
        # Create a check button for each variable
        for i in range(0, len(self.check_vars), 5):
            frame = tk.Frame(self)
            frame.pack(fill='x', pady=2)

            for j in range(5):
                index = i + j
                if index >= len(self.check_vars):
                    break
                var_info = self.check_vars[index]
                cb = tk.Checkbutton(frame, variable=var_info[1], text=var_info[0])
                cb.pack(side='left', padx=5)
                # self.checkbuttons.append(var)
