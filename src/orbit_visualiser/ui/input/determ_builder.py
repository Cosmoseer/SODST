from tkinter import Frame, StringVar, OptionMenu
from orbit_visualiser.ui.common.builder import Builder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager

class DetermBuilder(Builder):

    def __init__(self, determ_frame: Frame, oda: OrbitDataAccess, geo_manager: GeometryManager):
        self._determ_frame = determ_frame
        self._oda = oda
        self._geo_manager = geo_manager

    def build(self):
        det_frame = Frame(self._determ_frame, bd = 1, relief = "solid")
        self._build_separator(det_frame, "Determination")

        algorithms: list[str] = ["Gibbs"]

        alg_options = StringVar(value = "Gibbs")

        menu = OptionMenu(det_frame, alg_options, *algorithms)
        menu.pack(side = "top", anchor = "nw")

        det_frame.pack(side = "top", anchor = "nw", pady = (4, 0))