from tkinter import messagebox
from typing import TypeAlias
from orbit_visualiser.ui.input.determ_builder import DetermBuilder
from orbit_visualiser.ui.input.variables_builder import VariablesBuilder
from orbit_visualiser.ui.figure.orbit_figure_builder import OrbitFigureBuilder
from orbit_visualiser.ui.properties.properties_builder import PropertiesBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess

Builders: TypeAlias = DetermBuilder | VariablesBuilder | OrbitFigureBuilder | PropertiesBuilder

class Controller():

    def __init__(self, builder: Builders, oda: OrbitDataAccess):
        self._builder = builder
        self._oda = oda

    def _numerical_validation(self, variable: str | None = None) -> float:
        value = getattr(self._builder, f"{variable}_entry").get().strip()
        try:
            new_val_float = float(value)

            if new_val_float < 0 and variable != "nu":
                raise ValueError

            return new_val_float

    @staticmethod
    def _invalid_input_message() -> None:
        messagebox.showwarning("Warning", "Invalid input")