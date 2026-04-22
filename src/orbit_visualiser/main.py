import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QFrame, QWidget, QPushButton
from orbit_visualiser.core import Orbit, Satellite, CentralBody
from orbit_visualiser.ui import OrbitFigure, OrbitConfigBuilder, OrbitConfigController
from orbit_visualiser.ui.common.presets import initial_config

class MainWindow(QMainWindow):
    FIGURE_GEOMETRY = ("left", "nw")
    CONFIG_GEOMETRY = ("right", "ne")

    def __init__(self):
        super().__init__()

        self.setWindowTitle("2D Orbit Visualiser")

        if sys.platform.startswith("win"):
            self.showMaximized()
        else:
            self.showNormal()

        orbit: Orbit = Orbit.from_orbital_elements(
            initial_config.eccentricity,
            initial_config.radius_of_periapsis,
            initial_config.gravitational_parameter,
            initial_config.true_anomaly
        )

        central_body: CentralBody = CentralBody(
            initial_config.gravitational_parameter,
            initial_config.radius
        )
        satellite: Satellite = Satellite(orbit.position, orbit.velocity, central_body)

        main_layout: QHBoxLayout = QHBoxLayout()

        vars_frame = QFrame(parent = self)
        main_layout.addWidget(QPushButton())
        main_layout.addWidget(QPushButton())
        main_layout.addWidget(QPushButton())

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        """ orbit_figure: OrbitFigure = OrbitFigure(
            root, OrbitVisualiser.FIGURE_GEOMETRY, satellite
        )
        orbit_figure.build()

        orbit_builder: OrbitConfigBuilder = OrbitConfigBuilder(
            root, OrbitVisualiser.CONFIG_GEOMETRY, orbit, central_body, satellite
        )
        orbit_controller: OrbitConfigController = OrbitConfigController(
            orbit_figure, orbit_builder, orbit, satellite, central_body
        )
        orbit_builder.build(
            orbit_controller.reset_state,
            orbit_controller.validate_manual_input,
            orbit_controller.slider_changed,
            orbit_controller.format_display_value
        ) """



# TODO: Write tests as I go.
# TODO: Add variable presets (Earth - ISS, Earth - Geostationary, Mars - Phobos etc).
# TODO: Write proper docstrings
if __name__ == "__main__":
    app: QApplication = QApplication([])
    main = MainWindow()
    main.show()
    app.exec()