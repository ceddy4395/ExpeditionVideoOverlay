from tkinter import ttk
import ttkbootstrap as tb

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
        LogFileScreen(self.state)

    def open_videoscreen(self):
        VideoFileScreen(self.state)

