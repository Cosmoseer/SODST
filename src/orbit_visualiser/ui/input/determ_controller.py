import numpy as np
from numpy.typing import NDArray
from typing import Literal, Callable
from tkinter import Entry
from orbit_visualiser.ui.input.determ_builder import DetermBuilder
from orbit_visualiser.ui.input.elements_builder import ElementsBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.controller import Controller
from orbit_visualiser.ui.figure.orbit_figure_controller import OrbitFigureController

class DetermController(Controller):

    def __init__(
            self,
            builder: DetermBuilder,
            oda: OrbitDataAccess,
            figure_cont: OrbitFigureController,
            elements_builder: ElementsBuilder
    ):
        super().__init__(builder, oda)
        self._orbit_fig_cont = figure_cont
        self._elms_builder = elements_builder

    def determine_orbit(
            self, algorithm: Literal["state", "gibbs", "lambert", "range_angle", "angles_only", "gauss"]
    ) -> None:
        determination_alg: Callable = self._oda.determination_algorithm(algorithm)
        try:
            mu = self._numerical_validation(new_val = self._builder.mu_entry.get())[0]
        except ValueError:
            self._warning_message()
            return

        match algorithm:
            case "gibbs":
                try:
                    first_pos = self._array_from_entries(self._builder.first_pos_entries)
                    second_pos = self._array_from_entries(self._builder.second_pos_entries)
                    third_pos = self._array_from_entries(self._builder.third_pos_entries)
                except ValueError:
                    self._warning_message()
                    return

                inputs = [first_pos, second_pos, third_pos, mu]

        try:
            orbit = determination_alg(*inputs)
        except ValueError:
            self._warning_message("State cannot be evaluated at infinity")
            return

        self._update_satellite_state(orbit)

        self._orbit_fig_cont.redraw_orbit()
        self._orbit_fig_cont.redraw_satellite()


    def _array_from_entries(self, entries: tuple[Entry]) -> NDArray[np.float64]:
        entry_value_list = []
        for entry in entries:
            value_str = entry.get()
            entry_value_list.append(self._numerical_validation(new_val = value_str)[0])

        return np.array(entry_value_list)

    def validate_determination_input(self, variable: str):
        try:
            self._numerical_validation(variable)
        except ValueError:
            self._warning_message()
            return