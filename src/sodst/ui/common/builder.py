import numpy as np
from functools import partial
from typing import Callable, Any
from tkinter import Frame, Label, Scale, Entry, DoubleVar, LabelFrame, Button
from abc import ABC, abstractmethod
from sodst.ui.common.specs import VariableSpec
from sodst.ui.common.presets import initial_config
from sodst.ui.common.geometry import GeometryManager
from sodst.ui.common.fonts import title_font, subtitle_font, label_font
from sodst.ui.data_access import OrbitDataAccess

class Builder(ABC):

    _title_font = title_font
    _subtitle_font = subtitle_font
    _label_font = label_font

    def __init__(self, root: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        self._root = root
        self._oda = oda
        self._geo_manager = geo_manager

    @abstractmethod
    def build(self):
        pass

    @staticmethod
    def _build_button(root: Frame, button_txt: str, command: Callable[[Any], Any] | None) -> None:
        button = Button(root, text = button_txt, command = command)
        button.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _build_separator(self, root: Frame, text: str) -> None:
        frame = Frame(root)
        frame.pack(side = "top", fill = "x", pady = 4)

        Label(frame, text = text, font = self._title_font).pack(side = "left", padx = (0, 6))
        Frame(frame, height = 2, bd = 1, relief = "sunken").pack(side = "left", fill = "x", expand = True)


class InputBuilder(Builder):

    _e_specs: VariableSpec = VariableSpec(
            "Eccentricity",
            None,
            lambda sat: sat.orbit.eccentricity,
            initial_config.eccentricity,
            (0, 5),
            3,
            "normal"
        )
    _rp_specs: VariableSpec = VariableSpec(
            "Radius of periapsis",
            "km",
            lambda sat: sat.orbit.radius_of_periapsis,
            initial_config.radius_of_periapsis,
            (initial_config.radius + 1, 200_000),
            0,
            "normal"
        )
    _mu_specs: VariableSpec = VariableSpec(
            "Gravitational parameter",
            "km³/s²",
            lambda sat: sat.central_body.mu,
            initial_config.gravitational_parameter,
            (1, 1_000_000),
            0,
            "normal"
        )
    _nu_specs: VariableSpec = VariableSpec(
            "True anomaly",
            "°",
            lambda sat: np.degrees(sat.true_anomaly),
            np.degrees(initial_config.true_anomaly),
            (0, 360),
            2,
            "normal"
        )
    _raan_specs: VariableSpec = VariableSpec(
            "Right ascension of the ascending node",
            "°",
            lambda sat: np.degrees(sat.orbit.right_ascen_of_ascend_node),
            np.degrees(initial_config.right_ascension_of_the_ascending_node),
            (0, 360),
            2,
            "disabled"
        )
    _i_specs: VariableSpec = VariableSpec(
            "Inclination",
            "°",
            lambda sat: np.degrees(sat.orbit.inclination),
            np.degrees(initial_config.inclination),
            (0, 180),
            2,
            "normal"
        )
    _omega_specs: VariableSpec = VariableSpec(
            "Argument of periapsis",
            "°",
            lambda sat: np.degrees(sat.orbit.argument_of_periapsis),
            np.degrees(initial_config.argument_of_periapsis),
            (0, 360),
            2,
            "disabled"
        )

    _orbit_specs: dict[str, VariableSpec] = {
        "e" : _e_specs,
        "rp" : _rp_specs,
        "raan" : _raan_specs,
        "i" : _i_specs,
        "omega" : _omega_specs
    }

    _central_body_specs: dict[str, VariableSpec] = {
        "mu" : _mu_specs
    }

    _satellite_specs: dict[str, VariableSpec] = {
        "nu" : _nu_specs,
    }

    _variable_specs: dict[str, VariableSpec] = _orbit_specs | _central_body_specs | _satellite_specs

    def __init__(self, input_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        super().__init__(input_frame, oda, geo_manager)

        self._input_geometry = self._geo_manager.input_widgets

    @property
    def mu_slider(self) -> Scale:
        return self._mu_slider

    @property
    def mu_entry(self) -> Entry:
        return self._mu_entry

    @property
    def variable_specs(self) -> dict[str, VariableSpec]:
        return self._variable_specs

    def _build_input_label_frame(
            self,
            root: Frame,
            label: str,
            input_changed: Callable[[Any], Any],
            slider_changed: Callable[[Any], Any],
            specs: dict[str, VariableSpec]
    ) -> None:
        frame = LabelFrame(root, bd = 2, relief = "sunken", text = label, font = self._subtitle_font)
        self._build_input_frame(frame, input_changed, slider_changed, specs)
        frame.pack(side = "top", anchor = "nw", pady = (4, 0))

    def _build_input_frame(
            self,
            root: Frame,
            input_changed: Callable[[Any], Any],
            slider_changed: Callable[[Any], Any],
            specs: dict[str, VariableSpec]
    ) -> None:
        for variable, spec in specs.items():
            slider, entry = self._build_input_widgets(
                root, variable, spec, input_changed, slider_changed
            )
            setattr(self, f"_{variable}_slider", slider)
            setattr(self, f"_{variable}_entry", entry)

    def _build_input_widgets(self,
            root: Frame,
            variable: str,
            spec: VariableSpec,
            input_changed: Callable[[Any], Any],
            slider_changed: Callable[[Any], Any]
    ) -> tuple[Scale, Entry]:
        frame_geo = self._input_geometry[0]
        frame = Frame(root, width = frame_geo.width, height = frame_geo.height, relief = "groove", bd = 1)

        units = spec.units
        label = Label(frame, text = f"{spec.label}{"" if units is None else f" ({units})"}:")
        label.place(x = 5, y = 0)

        slider = self._build_slider(
            frame,
            variable,
            spec,
            slider_changed
        )

        entry_geom = self._input_geometry[2]
        entry = Entry(frame, width = entry_geom.width)
        entry.insert(0, f"{spec.getter(self._oda.satellite): 0.{spec.decimal_places}f}".strip())
        entry.configure(state = spec.init_state)
        entry.bind("<Return>", partial(input_changed, self, variable))
        entry.place(x = entry_geom.x, y = entry_geom.y)

        frame.pack(side = frame_geo.side, anchor = frame_geo.anchor, pady = frame_geo.pady)

        return slider, entry

    def _build_slider(
            self,
            root: Frame,
            variable: str,
            spec: VariableSpec,
            slider_changed: Callable[[Any], Any]
    ) -> Scale:
        slider_var: DoubleVar = DoubleVar()
        self.__setattr__(f"{variable}_var", slider_var)

        slider_name = f"_{variable}_slider"
        lims = spec.slider_lims
        self.__setattr__(
            slider_name,
            Scale(root, from_ = lims[0], to = lims[1], resolution = 1/10**spec.decimal_places, length = 275,
                  orient = "horizontal", variable = slider_var,
                  command = partial(slider_changed, self, variable),
                  tickinterval = 0, showvalue = 0,
                  state = spec.init_state
                  )
        )

        slider_var.set(spec.getter(self._oda.satellite))

        slider: Scale = self.__getattribute__(slider_name)
        geometry = self._input_geometry[1]
        slider.place(x = geometry.x, y = geometry.y, anchor = "nw")
        return slider

class DisplayBuilder(Builder):
    pass