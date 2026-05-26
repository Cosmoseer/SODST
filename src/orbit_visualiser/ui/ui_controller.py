from tkinter import Event
from typing import Callable, Any
from orbit_visualiser.ui.input.variables_controller import VariablesController
from orbit_visualiser.ui.properties.properties_controller import PropertiesController
from orbit_visualiser.ui.figure.orbit_figure_controller import OrbitFigureController
from orbit_visualiser.ui.common.controller import Controller
#from orbit_visualiser.ui.config.display_panel.display_panel_controller import DisplayController
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.ui_builder import UIBuilder

class UIController(Controller):

    def __init__(self, builder: UIBuilder, oda: OrbitDataAccess):
        self._builder = builder

        self._figure_controller = OrbitFigureController(builder.figure_builder, oda)
        self._variables_controller = VariablesController(self._figure_controller, builder.input_builder, oda)
        self._properties_controller = PropertiesController(builder.properties_builder, oda)

        self._callbacks: dict[str, Callable[[Any], Any]] = {
                "validate_manual_input": self.validate_manual_input,
                "reset_state": self.reset_state,
                "format_display_value": self.format_display_value,
                "slider_changed": self.slider_changed
            }

    @property
    def callbacks(self) -> dict[str, Callable[[Any], Any]]:
        return self._callbacks

    def validate_manual_input(
            self,
            variable: str,
            event: Event
    ) -> None:
        self._variables_controller.validate_manual_input(variable, event)
        self._properties_controller.update_display()

    def reset_state(self) -> Callable:
        return self._variables_controller.reset_state()

    def format_display_value(self, value: float | str, units: str | None) -> str:
        return self._properties_controller.format_display_value(value, units)

    def slider_changed(
            self,
            variable: str,
            input_type: str,
            new_val: str | float
    ) -> None:
        self._variables_controller.update_variable(
            variable,
            input_type,
            new_val
        )
        self._properties_controller.update_display()