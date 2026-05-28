from tkinter import Frame, Scale, Entry
from typing import Callable
from orbit_visualiser.ui.common.builder import InputBuilder
from orbit_visualiser.ui.common.specs import VariableSpec
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager


class VariablesBuilder(InputBuilder):

    def __init__(self, input_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        super().__init__(input_frame, oda, geo_manager)


    @property
    def variable_specs(self) -> dict[str, VariableSpec]:
        return self._variable_specs

    @property
    def e_slider(self) -> Scale:
        return self._e_slider

    @property
    def e_entry(self) -> Entry:
        return self._e_entry

    @property
    def rp_slider(self) -> Scale:
        return self._rp_slider

    @property
    def rp_entry(self) -> Entry:
        return self._rp_entry

    @property
    def mu_slider(self) -> Scale:
        return self._mu_slider

    @property
    def mu_entry(self) -> Entry:
        return self._mu_entry

    @property
    def nu_slider(self) -> Scale:
        return self._nu_slider

    @property
    def nu_entry(self) -> Entry:
        return self._nu_entry

    @property
    def raan_slider(self) -> Scale:
        return self._raan_slider

    @property
    def raan_entry(self) -> Entry:
        return self._raan_entry

    @property
    def i_slider(self) -> Scale:
        return self._i_slider

    @property
    def i_entry(self) -> Entry:
        return self._i_entry

    @property
    def omega_slider(self) -> Scale:
        return self._omega_slider

    @property
    def omega_entry(self) -> Entry:
        return self._omega_entry

    def build(
            self,
            reset: Callable,
            input_changed: Callable,
            slider_changed: Callable
    ) -> None:
        var_frame = Frame(self._root)
        self._variables_frame = var_frame

        self._build_separator(var_frame, "Variables")

        input_sections: dict[str, dict[str, VariableSpec]] = {
            "Orbital geometry": self._orbit_specs,
            "Central body": self._central_body_specs,
            "Satellite": self._satellite_specs
        }

        for section, specs in input_sections.items():
            frame = self._build_input_label_frame(var_frame, section)
            self._build_input_frame(frame, validate_input, slider_changed, specs)
            frame.pack(side = "top", anchor = "nw", pady = (4, 0))

        self._build_button(var_frame, "Reset", reset)

        var_frame.pack(side = "top", anchor = "nw", pady = (4, 0))