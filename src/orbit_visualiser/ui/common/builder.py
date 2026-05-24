from tkinter import Frame, Label
from abc import ABC, abstractmethod

class Builder(ABC):

    _title_font = ("Orbitron", 16, "bold")
    _subtitle_font = ("Orbitron", 13, "normal")
    _label_font = ("Fira Mono", 9, "normal")

    @abstractmethod
    def build(self):
        pass

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

    _variable_specs: dict[str, VariableSpec] = {
            "e" : _e_specs,
            "rp" : _rp_specs,
            "nu" : _nu_specs,
            "raan" : _raan_specs,
            "i" : _i_specs,
            "omega" : _omega_specs,
            "mu" : _mu_specs
        }