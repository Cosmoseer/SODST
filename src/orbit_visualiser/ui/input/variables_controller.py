from tkinter import Entry, DoubleVar
from decimal import Decimal
import numpy as np
from orbit_visualiser.ui.figure.orbit_figure_controller import OrbitFigureController
from orbit_visualiser.ui.input.variables_builder import  VariablesBuilder
from orbit_visualiser.core import Orbit, asymptote_anomaly
from orbit_visualiser.ui.common.utils import floor_float
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.controller import Controller

# TODO: Allow for temporary increase in slider scale when inputting manual values.
# TODO: Allow for fractional manual inputs.
# TODO: Remove any leading 0s from manual inputs.
# TODO: Refactor to a lazy/cached recalculation model. Currently everything is recalculated on every variable change.

class VariablesController(Controller):


    def __init__(
            self,
            builder: VariablesBuilder,
            oda: OrbitDataAccess,
            figure_cont: OrbitFigureController,
    ):
        super().__init__(builder, oda)
        self._orbit_fig_cont = figure_cont

    def reset_state(self) -> None:
        init_values = []
        var_props = self._builder.variable_specs
        for name, value in list(var_props.items()):
            init_value = value.init_value
            getattr(self._builder, f"{name}_slider").set(init_value)

            entry: Entry = getattr(self._builder, f"{name}_entry")
            entry.delete(0, 1000)
            entry.insert(0, f"{init_value: 0.{value.decimal_places}f}".strip())

            init_values.append(init_value)

        self._update_satellite_state(Orbit.from_orbital_elements(*init_values))

        self._orbit_fig_cont.redraw_orbit()
        self._orbit_fig_cont.redraw_satellite()
        self._orbit_fig_cont.reset_axes()

    def update_from_manual_input(self, variable: str) -> None:
        try:
            new_val_float, new_val_str = self._numerical_validation(variable)
        except ValueError:
            self._warning_message()
            return

        # When e < 1 then the orbit is periodic, and so the true anomaly is as well.
        if variable == "nu":
            if self._oda.satellite.orbit.eccentricity < 1 and (new_val_float < 0 or new_val_float > 360):
                # float(new_val) will kill off any decimal points when new_val has extremely large
                # absolute value (around 16 digits due to limitations of 64bit double precision
                # for python floats). The Decimal class retains that information. If the angle is
                # negative then Decimal(new_val)%360 reduces it to (-360, 0), then + 360 to the range we want.
                new_val_float = (Decimal(new_val_str)%360 + 360)%360
                self._set_entry(getattr(self._builder, f"{variable}_entry"),
                                f"{new_val_float: 0.{self._builder.variable_specs[variable].decimal_places}f}".strip()
                            )
            else:
                t_asymp = np.degrees(self._oda.satellite.orbit.asymptote_anomaly)
                if new_val_float < -t_asymp:
                    new_val_float = -t_asymp
                elif new_val_float > t_asymp:
                    new_val_float = t_asymp

        self.update_variable(variable, "entry", new_val_float)

    def update_variable(
            self,
            variable: str,
            input_type: str,
            new_val: str | float
    ) -> None:
        new_val = float(new_val)

        self.slider_entry_interaction(input_type, variable, new_val)

        if variable in ["nu", "raan", "i", "omega"]:
            new_val = np.deg2rad(float(new_val))

        new_values = {
            "e": self._builder.e_var.get(),
            "rp": self._builder.rp_var.get(),
            "raan": np.deg2rad(self._builder.raan_var.get()),
            "i": np.deg2rad(self._builder.i_var.get()),
            "omega": np.deg2rad(self._builder.omega_var.get()),
            "mu": self._builder.mu_var.get(),
            "nu": np.deg2rad(self._builder.nu_var.get())
        }
        new_values[variable] = new_val

        self._configure_input_widgets(new_values, variable)

        try:
            self._update_satellite_state(Orbit.from_orbital_elements(*new_values.values()))

        except ValueError:
            self._warning_message("State cannot be evaluated at infinity")
            return

        self._orbit_fig_cont.redraw_orbit()
        self._orbit_fig_cont.redraw_satellite()

    def _configure_input_widgets(self, new_values: dict[str, float], variable: str) -> None:
        new_val = new_values[variable]

        # The value of the eccentricity determines the range of possible true anomaly values, which
        # this if block checks for.
        if variable == "e":
            if new_val >= 1:
                # Slider should never allow for users to input the true anomaly of the asymptote
                t_asymp_offset = np.degrees(asymptote_anomaly(new_val)) - 0.01
                t_asymp_slider_lim = floor_float(t_asymp_offset, 2)
                self._builder.nu_slider.configure(from_ = -t_asymp_slider_lim, to = t_asymp_slider_lim)

                nu = new_values["nu"]
                if nu < -t_asymp_offset:
                    new_values["nu"] = -t_asymp_offset
                elif nu > t_asymp_offset:
                    new_values["nu"] = t_asymp_offset
            else:
                self._builder.nu_slider.configure(from_ = 0, to = 360)

        if np.isclose(new_values["e"], 0):
            new_values["omega"] = 0.0
            omega_var: DoubleVar = self._builder.omega_var
            omega_var.set(0.0)

            self._set_entry(self._builder.omega_entry, "0.00")

            self._builder.omega_entry.configure(state = "disabled")
            self._builder.omega_slider.configure(state = "disabled")
        else:
            self._builder.omega_entry.configure(state = "normal")
            self._builder.omega_slider.configure(state = "normal")

        if np.isclose(new_values["i"], 0):
            new_values["raan"] = 0.0
            raan_var: DoubleVar = self._builder.raan_var
            raan_var.set(0.0)

            self._set_entry(self._builder.raan_entry, "0.00")

            self._builder.raan_entry.configure(state = "disabled")
            self._builder.raan_slider.configure(state = "disabled")
        else:
            self._builder.raan_entry.configure(state = "normal")
            self._builder.raan_slider.configure(state = "normal")