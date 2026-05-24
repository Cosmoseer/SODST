from tkinter import Frame, StringVar, OptionMenu, LabelFrame, Entry, Label, Button
from typing import Literal
from orbit_visualiser.ui.common.builder import Builder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager

# TODO: Write functions for building different algorithm frames but initialise Gibbs
class DetermBuilder(Builder):

    ALGORITHMS = ("gibbs",)
    POS_COMPONENTS = ("x", "y", "z")

    def __init__(self, determ_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        self._determ_frame = determ_frame
        self._oda = oda
        self._geo_manager = geo_manager

    def build(self) -> None:
        det_frame = Frame(self._determ_frame)
        self._build_separator(det_frame, "Determination")

        alg_options = StringVar(value = self.ALGORITHMS[0].title())

        menu = OptionMenu(det_frame, alg_options, *tuple(map(str.title, self.ALGORITHMS)))
        menu.pack(side = "top", anchor = "nw", pady = (16, 0))

        self._pos_frame(det_frame, "first")
        self._pos_frame(det_frame, "second")
        self._pos_frame(det_frame, "third")

        determ_button = Button(det_frame, text = "Determine orbit", command = None)
        determ_button.pack(side = "top", anchor = "nw", pady = (4, 0))

        det_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _pos_frame(self, root: Frame, pos: Literal["first", "second", "third"]) -> None:
        pos_frame = LabelFrame(
            root, bd = 2, relief = "sunken", text = f"{pos.title()} position", font = self._subtitle_font
        )
        for entry in self._pos_input(pos_frame):
            setattr(self, f"_{pos}_{entry[1]}_entry", entry[0])

        pos_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _pos_input(self, root: Frame) -> list[tuple[Entry, str]]:
        entry_frame = Frame(root, width = 310, height = 35)
        entries: list[tuple[Entry, str]] = []
        label_x, entry_x = 5, 22

        for comp in self.POS_COMPONENTS:
            label = Label(entry_frame, text = f"{comp}:")
            label.place(x = label_x, y = 2.5)
            entry = Entry(entry_frame, width = 8)
            entry.insert(0, "")
            entry.place(x = entry_x, y = 2.5)
            entries.append((entry, comp))
            label_x += 100
            entry_x += 100

        entry_frame.pack(side = "top", anchor = "nw")

        return entries