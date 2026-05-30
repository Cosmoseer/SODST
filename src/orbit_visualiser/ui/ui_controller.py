from tkinter import Event
from typing import Callable, Any
from orbit_visualiser.ui.input.variables_controller import VariablesController
from orbit_visualiser.ui.properties.properties_controller import PropertiesController
from orbit_visualiser.ui.figure.orbit_figure_controller import OrbitFigureController
from orbit_visualiser.ui.input.determ_controller import DetermController
from orbit_visualiser.ui.common.controller import Controller
#from orbit_visualiser.ui.config.display_panel.display_panel_controller import DisplayController
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.ui_builder import UIBuilder
from orbit_visualiser.ui.input.variables_builder import VariablesBuilder
from orbit_visualiser.ui.input.determ_builder import DetermBuilder

class UIController(Controller):

    def __init__(self, builder: UIBuilder, oda: OrbitDataAccess):
        super().__init__(builder, oda)

        self._figure_controller = OrbitFigureController(builder.figure_builder, oda)
        self._variables_controller = VariablesController(builder.input_builder, oda, self._figure_controller)
        self._determ_controller = DetermController(builder.determ_builder, oda)
        self._properties_controller = PropertiesController(builder.properties_builder, oda)

        self._callbacks: dict[str, Callable[[Any], Any]] = {
                "manual_input_changed": self.manual_input_changed,
                "reset_state": self.reset_state,
                "format_display_value": self.format_display_value,
                "slider_changed": self.slider_changed
            }

    @property
    def callbacks(self) -> dict[str, Callable[[Any], Any]]:
        return self._callbacks

    def manual_input_changed(
            self, cls: VariablesBuilder | DetermBuilder, variable: str, event: Event
    ) -> None:
        if isinstance(cls, VariablesBuilder):
            self._variables_controller.update_from_manual_input(variable)
            self._properties_controller.update_display()

        elif isinstance(cls, DetermBuilder):
            self._determ_controller.validate_determination_input(variable)

    def reset_state(self) -> None:
        return self._variables_controller.reset_state()

    def format_display_value(self, value: float | str, units: str | None) -> str:
        return self._properties_controller.format_display_value(value, units)

    def slider_changed(self, variable: str, input_type: str, new_val: str | float) -> None:
        self._variables_controller.update_variable(
            variable,
            input_type,
            new_val
        )
        self._properties_controller.update_display()