from tkinter import Frame, StringVar, OptionMenu, LabelFrame, Entry, Label
from typing import Literal
from orbit_visualiser.ui.common.builder import InputBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager

# TODO: Write functions for building different algorithm frames but initialise Gibbs
class DetermBuilder(InputBuilder):

    ALGORITHMS = ("gibbs",)
    POS_COMPONENTS = ("x", "y", "z")

    def __init__(self, determ_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        self._determ_frame = determ_frame
        self._oda = oda
        self._geo_manager = geo_manager

    @property
    def first_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self._first_x_entry, self._first_y_entry, self._first_z_entry

    @property
    def second_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self._second_x_entry, self._second_y_entry, self._second_z_entry

    @property
    def third_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self._third_x_entry, self._third_y_entry, self._third_z_entry

    def build(self) -> None:
        det_frame = Frame(self._determ_frame)
        self._build_separator(det_frame, "Determination")

        alg_options = StringVar(value = self.ALGORITHMS[0].title())

        menu = OptionMenu(det_frame, alg_options, *tuple(map(str.title, self.ALGORITHMS)))
        menu.pack(side = "top", anchor = "nw", pady = (16, 0))

        self._build_state_frame(det_frame)
        self._build_gibbs_frame(det_frame)
        self._build_lambert_frame(det_frame)
        self._build_range_angle_frame(det_frame)
        self._build_angles_only_frame(det_frame)
        self._build_gauss_frame(det_frame)

        # The gibbs frame is rendered by default
        self._gibbs_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

        self._build_button(det_frame, "Determine orbit", None)

        det_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _build_state_frame(self, root: Frame) -> None:
        pass

    def _build_gibbs_frame(self, root: Frame) -> None:
        self._gibbs_frame = Frame(root)
        positions = ("first", "second", "third")
        for pos in positions:
            self._pos_frame(self._gibbs_frame, pos)

    def _build_lambert_frame(self, root: Frame) -> None:
        pass

    def _build_range_angle_frame(self, root: Frame) -> None:
        pass

    def _build_angles_only_frame(self, root: Frame) -> None:
        pass

    def _build_gauss_frame(self, root: Frame) -> None:
        pass

    def _pos_frame(self, root: Frame, pos: Literal["first", "second", "third"]) -> None:
        pos_frame = LabelFrame(
            root, bd = 2, relief = "sunken", text = f"{pos.title()} position", font = self._subtitle_font
        )
        for entry in self._pos_input(pos_frame):
            setattr(self, f"_{pos}_{entry[0]}_entry", entry[1])

        pos_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _pos_input(self, root: LabelFrame) -> list[tuple[str, Entry]]:
        entry_frame = Frame(root, width = 310, height = 35)

        entries: list[tuple[Entry, str]] = []
        pos_entries = self._geo_manager.pos_entries
        for i, (label_geo, entry_geo) in enumerate(pos_entries):
            label = Label(entry_frame, text = f"{self.POS_COMPONENTS[i]}:")
            label.place(x = label_geo.x, y = label_geo.y)
            entry = Entry(entry_frame, width = entry_geo.width)
            entry.insert(0, "")
            entry.place(x = entry_geo.x, y = entry_geo.y)
            entries.append((self.POS_COMPONENTS[i], entry))

        entry_frame.pack(side = "top", anchor = "nw")

        return entries