from functools import partial
from tkinter import Frame, StringVar, OptionMenu, LabelFrame, Entry, Label
from typing import Literal, Callable, Any
from orbit_visualiser.ui.common.builder import InputBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager

# TODO: Write functions for building different algorithm frames but initialise Gibbs
class DetermBuilder(InputBuilder):

    ALGORITHMS = ("gibbs",)
    POS_COMPONENTS = ("x", "y", "z")
    POSITIONS = ("first", "second", "third")

    def __init__(self, determ_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        super().__init__(determ_frame, oda, geo_manager)

    @property
    def first_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self.first_x_entry, self.first_y_entry, self.first_z_entry

    @property
    def second_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self.second_x_entry, self.second_y_entry, self.second_z_entry

    @property
    def third_pos_entries(self) -> tuple[Entry, Entry, Entry]:
        return self.third_x_entry, self.third_y_entry, self.third_z_entry

    def build(
            self,
            input_changed: Callable[[Any], Any],
            slider_changed: Callable[[Any], Any],
            determine_orbit: Callable[[Any], Any]
    ) -> None:
        det_frame = Frame(self._root)
        self._build_separator(det_frame, "Determination")

        alg_options = StringVar(value = self.ALGORITHMS[0].title())

        self._alg_menu = OptionMenu(det_frame, alg_options, *tuple(map(str.title, self.ALGORITHMS)))
        self._alg_menu.pack(side = "top", anchor = "nw", pady = (16, 0))

        self._build_state_frame(det_frame)
        self._build_gibbs_frame(det_frame, input_changed)
        self._build_lambert_frame(det_frame)
        self._build_range_angle_frame(det_frame)
        self._build_angles_only_frame(det_frame)
        self._build_gauss_frame(det_frame)

        # The gibbs frame is rendered by default
        self._gibbs_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

        # TODO: Have the input_sections dictionary as an attribute in InputBuilder parent class (see VariablesBuilder)
        self._build_input_label_frame(det_frame, "Central body", input_changed, slider_changed, {"mu": self._mu_specs})

        self._build_button(det_frame, "Determine orbit", partial(determine_orbit, alg_options.get().lower()))

        det_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _build_state_frame(self, root: Frame) -> None:
        pass

    def _build_gibbs_frame(self, root: Frame, input_changed: Callable[[Any], Any]) -> None:
        self._gibbs_frame = Frame(root)

        for pos in self.POSITIONS:
            self._pos_frame(self._gibbs_frame, pos, input_changed)

    def _build_lambert_frame(self, root: Frame) -> None:
        pass

    def _build_range_angle_frame(self, root: Frame) -> None:
        pass

    def _build_angles_only_frame(self, root: Frame) -> None:
        pass

    def _build_gauss_frame(self, root: Frame) -> None:
        pass

    def _pos_frame(
            self,
            root: Frame,
            pos: Literal["first", "second", "third"],
            input_changed: Callable[[Any], Any]
    ) -> None:
        pos_frame = LabelFrame(
            root, bd = 2, relief = "sunken", text = f"{pos.title()} position", font = self._subtitle_font
        )
        for entry in self._pos_input(pos_frame, pos, input_changed):
            setattr(self, f"{pos}_{entry[0]}_entry", entry[1])

        pos_frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    # TODO: Give validation callback to entries
    def _pos_input(
            self,
            root: LabelFrame,
            pos: Literal["first", "second", "third"],
            input_changed: Callable[[Any], Any]
    ) -> list[tuple[str, Entry]]:
        entry_frame = Frame(root, width = 310, height = 35)

        entries: list[tuple[Entry, str]] = []
        pos_entries = self._geo_manager.pos_entries
        for i, (label_geo, entry_geo) in enumerate(pos_entries):
            comp = self.POS_COMPONENTS[i]
            label = Label(entry_frame, text = f"{comp}:")
            label.place(x = label_geo.x, y = label_geo.y)
            entry = Entry(entry_frame, width = entry_geo.width)
            entry.insert(0, "")
            entry.bind("<Return>", partial(input_changed, self, f"{pos}_{comp}"))
            entry.place(x = entry_geo.x, y = entry_geo.y)
            entries.append((comp, entry))

        entry_frame.pack(side = "top", anchor = "nw")

        return entries