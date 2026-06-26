import numpy as np
from tkinter import messagebox, DoubleVar, Entry
from typing import TypeAlias
from sodst.ui.input.determ_builder import DetermBuilder
from sodst.ui.input.elements_builder import ElementsBuilder
from sodst.ui.figure.orbit_figure_builder import OrbitFigureBuilder
from sodst.ui.properties.properties_builder import PropertiesBuilder
from sodst.ui.data_access import OrbitDataAccess
from sodst.core import Orbit, Satellite, asymptote_anomaly
from sodst.ui.common.utils import floor_float

Builders: TypeAlias = DetermBuilder | ElementsBuilder | OrbitFigureBuilder | PropertiesBuilder

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

    def _configure_elements_widgets(self, builder: ElementsBuilder, new_values: dict[str, float], variable: str | None = None) -> None:
        # The value of the eccentricity determines the range of possible true anomaly values, which
        # this if block checks for.
        if variable == "e" or variable is None:
            new_val = new_values["e"]
            if new_val >= 1:
                # Slider should never allow for users to input the true anomaly of the asymptote
                t_asymp_offset = np.degrees(asymptote_anomaly(new_val)) - 0.01
                t_asymp_slider_lim = floor_float(t_asymp_offset, 2)
                builder.nu_slider.configure(from_ = -t_asymp_slider_lim, to = t_asymp_slider_lim)

                nu = new_values["nu"]
                if nu < -t_asymp_offset:
                    new_values["nu"] = -t_asymp_offset
                elif nu > t_asymp_offset:
                    new_values["nu"] = t_asymp_offset
            else:
                builder.nu_slider.configure(from_ = 0, to = 360)

        if np.isclose(new_values["e"], 0):
            new_values["omega"] = 0.0
            omega_var: DoubleVar = builder.omega_var
            omega_var.set(0.0)

            self._set_entry(builder.omega_entry, "0.00")

            builder.omega_entry.configure(state = "disabled")
            builder.omega_slider.configure(state = "disabled")
        else:
            builder.omega_entry.configure(state = "normal")
            builder.omega_slider.configure(state = "normal")

        if np.isclose(new_values["i"], 0):
            new_values["raan"] = 0.0
            raan_var: DoubleVar = builder.raan_var
            raan_var.set(0.0)

            self._set_entry(builder.raan_entry, "0.00")

            builder.raan_entry.configure(state = "disabled")
            builder.raan_slider.configure(state = "disabled")
        else:
            builder.raan_entry.configure(state = "normal")
            builder.raan_slider.configure(state = "normal")