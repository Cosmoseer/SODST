import numpy as np
from numpy.typing import NDArray
from typing import Literal, Callable
from tkinter import Entry
from orbit_visualiser.ui.input.determ_builder import DetermBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.controller import Controller

class DetermController(Controller):

    def __init__(self, builder: DetermBuilder, oda: OrbitDataAccess):
        self._builder = builder
        self._oda = oda

    def determine_orbit(self, algorithm: Literal["state", "gibbs", "lambert", "range_angle", "angles_only", "gauss"]):
        determination_alg: Callable = self._oda.determination_algorithm(algorithm)

        match algorithm:
            case "gibbs":
                first_pos = self._array_from_entries(self._builder.first_pos_entries)
                second_pos = self._array_from_entries(self._builder.second_pos_entries)
                third_pos = self._array_from_entries(self._builder.third_pos_entries)
                # also get gravitational parameter when built

    def _array_from_entries(entries: tuple[Entry]) -> NDArray[np.float64]:
        pass

    def validate_determination_input(self, variable: str):
        new_val = getattr(self._builder, f"{variable}_entry").get().strip()
        self._numerical_validation(new_val, variable)