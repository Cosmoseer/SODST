from tkinter import Frame, Label
from abc import ABC, abstractmethod

class Builder(ABC):

    _title_font = ("Orbitron", 16, "bold")
    _subtitle_font = ("Orbitron", 13, "normal")
    _label_font = ("Fira Mono", 9, "normal")

    @abstractmethod
    def build(self):
        pass

    def _build_separator(self, root: Frame, text: str) -> None:
        frame = Frame(root)
        frame.pack(side = "top", fill = "x", pady = 4)

        Label(frame, text = text, font = self._title_font).pack(side = "left", padx = (0, 6))
        Frame(frame, height = 2, bd = 1, relief = "sunken").pack(side = "left", fill = "x", expand = True)