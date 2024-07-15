from __future__ import annotations

from typing import Callable, List


class State:
    # filename: str
    # video: str
    # vars: list[str]

    def __init__(self):
        self._filename = ""
        self._video = ""
        self._vars = []
        self.callbacks = []

    @property
    def video(self):
        return self._video

    @video.setter
    def video(self, _video: str):
        self._video = _video
        self.notify_callbacks()

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = filename
        self.notify_callbacks()

    @property
    def vars(self) -> List[str]:
        return self._vars

    @vars.setter
    def vars(self, var_list: List[str]):
        self._vars = var_list
        self.notify_callbacks()

    def add_var(self, var: str):
        self._vars.append(var)
        self.notify_callbacks()

    def notify_callbacks(self):
        for callback in self.callbacks:
            callback(self)

    def register_callback(self, callback: Callable[[State], None]):
        self.callbacks.append(callback)
