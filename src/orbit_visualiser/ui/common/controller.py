from tkinter import messagebox, DoubleVar, Entry
from typing import TypeAlias
from orbit_visualiser.ui.input.determ_builder import DetermBuilder
from orbit_visualiser.ui.input.variables_builder import VariablesBuilder
from orbit_visualiser.ui.figure.orbit_figure_builder import OrbitFigureBuilder
from orbit_visualiser.ui.properties.properties_builder import PropertiesBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.core import Orbit, Satellite

Builders: TypeAlias = DetermBuilder | VariablesBuilder | OrbitFigureBuilder | PropertiesBuilder

class Controller():

    def __init__(self, builder: Builders, oda: OrbitDataAccess):
        self._builder = builder
        self._oda = oda

    def _numerical_validation(
            self, variable: str | None = None, new_val: str | None = None
    ) -> tuple[float, str]:
        if variable is None and new_val is None:
            raise ValueError("Both variable and new_val arguments can't be None")

        new_val_str = (getattr(self._builder, f"{variable}_entry").get().strip() if new_val is None
                       else new_val)

        new_val_float = float(new_val_str)

        if new_val_float < 0 and variable is not None and variable != "nu":
            raise ValueError

        return new_val_float, new_val_str

    @staticmethod
    def _warning_message(warning_msg: str = "Invalid inputs") -> None:
        messagebox.showwarning("Warning", warning_msg)

    def slider_entry_interaction(
            self, input_type: str, variable: str, new_val: float | None
    ) -> None:
        if new_val is None:
            new_val = float(getattr(self._builder, f"{variable}_{input_type}").get())

        match input_type:
            case "slider":
                self._set_entry(
                    getattr(self._builder, f"{variable}_entry"),
                    f"{new_val: 0.{self._builder.variable_specs[variable].decimal_places}f}".strip()
                )

            case "entry":
                slider_var: DoubleVar = getattr(self._builder, f"{variable}_var")
                slider_var.set(new_val)

    def _set_entry(self, entry: Entry, new_entry_str: str) -> None:
        entry.delete(0, 1000)
        entry.insert(
                0,
                new_entry_str
        )

    def _update_satellite_state(self, orbit: Orbit) -> None:
        sat: Satellite = self._oda.satellite
        sat.position = orbit.position
        sat.velocity = orbit.velocity
        sat.central_body.mu = orbit.mu