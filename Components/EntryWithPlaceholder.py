import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self._placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        #
        # self.bind("<FocusIn>", self.foc_in)
        # self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, placeholder):
        self._placeholder = placeholder
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
