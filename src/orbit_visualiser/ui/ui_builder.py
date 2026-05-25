from tkinter import Frame
from ttkbootstrap import Window
from ttkbootstrap.scrolled import ScrolledFrame
from typing import Callable
from orbit_visualiser.ui.figure.orbit_figure_builder import OrbitFigureBuilder
from orbit_visualiser.ui.properties.properties_builder import PropertiesBuilder
from orbit_visualiser.ui.input.variables_builder import VariablesBuilder
from orbit_visualiser.ui.input.determ_builder import DetermBuilder
from orbit_visualiser.ui.data_access import OrbitDataAccess
from orbit_visualiser.ui.common.geometry import GeometryManager, FrameGeometry

class UIBuilder():

    def __init__(self, root: Window, oda: OrbitDataAccess, geo_manager: GeometryManager):
        self._root = root
        self._oda = oda
        self._geo_manager = geo_manager

        input_geom, determ_geom, figure_geom, props_geom = geo_manager.parent_frame
        self._input_frame = self._build_frame(input_geom)
        self._determ_frame = self._build_frame(determ_geom, determ_frame = True)
        self._figure_frame = self._build_frame(figure_geom, scrollable = False)
        self._properties_frame = self._build_frame(props_geom)

        self._input_builder = VariablesBuilder(self._input_frame, oda, geo_manager)
        self._determ_builder = DetermBuilder(self._determ_frame, oda, geo_manager)
        self._figure_builder = OrbitFigureBuilder(self._figure_frame, oda, geo_manager)
        self._properties_builder = PropertiesBuilder(self._properties_frame, oda)

    @property
    def input_builder(self) -> VariablesBuilder:
        return self._input_builder

    @property
    def figure_builder(self) -> OrbitFigureBuilder:
        return self._figure_builder

    @property
    def properties_builder(self) -> PropertiesBuilder:
        return self._properties_builder

    def build(
            self,
            reset: Callable,
            validate_input: Callable,
            slider_changed: Callable,
            format_value: Callable
    ) -> None:
        self._input_builder.build(reset, validate_input, slider_changed)
        self._determ_builder.build()
        self._figure_builder.build()
        self._properties_builder.build(format_value)

    def _build_frame(self, frame_geom: FrameGeometry, scrollable: bool = True, determ_frame: bool = False) -> Frame | ScrolledFrame:
        scroll_frame_geom = self._geo_manager.parent_scrollable(determ_frame)
        frame = (ScrolledFrame(self._root, width = scroll_frame_geom.width, autohide = True,
                               padding = scroll_frame_geom.padding)
                if scrollable else Frame(self._root, bd = 1))

        frame.pack(side = frame_geom.side, anchor = frame_geom.anchor, padx = frame_geom.padx,
                   pady = frame_geom.pady, fill = frame_geom.fill, expand = frame_geom.expand
                   )

        return frame


