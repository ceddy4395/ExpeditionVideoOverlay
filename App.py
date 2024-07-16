from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *


from Components.EntryWithPlaceholder import EntryWithPlaceholder
from Screens.LogFileScreen import LogFileScreen
from Screens.VideoFileScreen import VideoFileScreen
from State import State


class App(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.state = State()
        self.state.register_callback(self.stated_updated)
        self.title("Main menu")
        self.resizable = (False, False)

        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        label = ttk.Label(master=container, text="Log file", width=10)
        label.pack(side=LEFT, padx=5)
        self.input_logscreen = EntryWithPlaceholder(master=container, placeholder=("Path to logile"))
        self.input_logscreen.pack(side=LEFT, padx=5, fill=X, expand=YES)
        button_logscreen = tb.Button(container, text='Import log file', command=self.open_logscreen)
        button_logscreen.pack(side=RIGHT, padx=5, expand=NO)


        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        label = ttk.Label(master=container, text="Video file", width=10)
        label.pack(side=LEFT, padx=5)
        input_video = EntryWithPlaceholder(container, placeholder="Path to video")
        input_video.pack(side=LEFT, padx=5, fill=X, expand=YES)
        button_video = ttk.Button(container, text='Import video', command=self.open_videoscreen)
        button_video.pack(side=RIGHT, padx=5, expand=NO)
        self.vars_label = ttk.Label(self, text=f"{self.state.vars}")

        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        label = ttk.Label(master=container, text="Video start time", width=10)
        label.pack(side=LEFT, padx=5)
        date = tb.DateEntry(master=container, firstweekday=0, dateformat="%x %X")
        date.pack(side=LEFT, padx=5)

        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15,10))
        sub_btn = tb.Button(
            master=container,
            text="Go!",
            bootstyle=SUCCESS,
            width=6,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        # self.vars_label.pack(expand=True)

    def stated_updated(self, _state: State):
        self.state = _state
        self.vars_label.config(text=f"{self.state.vars}")
        self.input_logscreen.placeholder = self.state.filename
        # if _state.filename:
        #     self.input_logscreen.destroy()
        #     self.input_logscreen = EntryWithPlaceholder(self, _state.filename)
        #     self.input_logscreen.grid(row=1, column=0)

    def open_logscreen(self):
        LogFileScreen(self.state)

    def open_videoscreen(self):
        VideoFileScreen(self.state)

