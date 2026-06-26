from dataclasses import dataclass
from typing import Literal, LiteralString
from ttkbootstrap import Window

@dataclass
class DimensionsGeometry():
    width: int = 0
    height: int = 0

@dataclass
class PlaceableGeometry():
    x: int
    y: int

@dataclass
class FrameGeometry(DimensionsGeometry):
    side: Literal['left', 'right', 'top', 'bottom'] = "left"
    anchor: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se'] = "nw"
    padx: int | tuple[int, int] = 0
    pady: int | tuple[int, int] = 0
    fill: Literal['none', 'x', 'y', 'both'] = "none"
    expand: bool = False

@dataclass
class ScrolledFrameGeometry(DimensionsGeometry):
    padding: int = 2

@dataclass
class EntryGeometry(DimensionsGeometry, PlaceableGeometry):
    pass

@dataclass
class SliderGeometry(PlaceableGeometry):
    pass

class GeometryManager():
    """
    Class for managing tkinter widget geometry and OS differences.
    """

    def __init__(self, os: LiteralString, root: Window):
        self._os = os
        self._os_win: bool = os.startswith("win")

        if self._os_win:
            root.geometry("1500x800")
            root.resizable(False, False)

    @property
    def parent_frame(self) -> tuple[FrameGeometry, FrameGeometry, FrameGeometry, FrameGeometry]:
        """
        The tuple of frame geometry of the 4 top level frames, input, determination, figure and properties in that
        order.

        Returns
        -------
        tuple[FrameGeometry, FrameGeometry, FrameGeometry, FrameGeometry]
            Tuple of parent frame FrameGeometry
        """
        return (
            FrameGeometry(padx = 2, pady = (2, 0), fill = "y", expand = True),
            FrameGeometry(padx = 2, pady = (2, 0), fill = "y", expand = True),
            FrameGeometry(padx = 8, pady = 6),
            FrameGeometry(padx = 2, pady = (2, 0), fill = "y", expand = True),
        )

    def parent_scrollable(self, determ_frame: bool) -> ScrolledFrameGeometry:
        """
        The geometry for the scrolled parent frames (input and properties)

        Parameters
        ----------
        determ_frame : bool
            Boolean for whether the scrollable frame geometry being grabbed is for the determination
            frame

        Returns
        -------
        ScrolledFrameGeometry
            Geometry for the parent ScrolledFrame
        """
        if self._os_win:
            return ScrolledFrameGeometry(width = 375, padding = 10)

        return ScrolledFrameGeometry(width = 335) if determ_frame else ScrolledFrameGeometry(width = 315)

    @property
    def input_widgets(self) -> tuple[FrameGeometry, SliderGeometry, EntryGeometry]:
        """
        The geometry for the frame, slider and entry widgets for each individual input frame.

        Returns
        -------
        tuple[FrameGeometry, SliderGeometry, EntryGeometry]
            Geometry for the input frame
        """
        return (
            self._input_frame(),
            self._input_slider(),
            self._input_entry()
        )

    def _input_frame(self) -> FrameGeometry:
        if self._os_win:
            return FrameGeometry(side = "top", width = 375, height = 100, pady = 2)

        return FrameGeometry(side = "top", width = 290, height = 75, pady = 2)

    def _input_entry(self) -> EntryGeometry:
        if self._os_win:
            return EntryGeometry(x = 5, y = 30, width = 10)

        return EntryGeometry(x = 5, y = 20, width = 10)

    def _input_slider(self) -> SliderGeometry:
        if self._os_win:
            return SliderGeometry(x = 5, y = 70)

        return SliderGeometry(x = 5, y = 45)

    @property
    def figsize(self) -> tuple[int, int]:
        """
        The figure size of the orbit plot.

        Returns
        -------
        tuple[int, int]
            The tuple of ints representing the (x, y) figure size in inches
        """
        if self._os_win:
            return (5, 5)

        return (7, 7)

    @property
    def pos_entries(self) -> list[tuple[PlaceableGeometry, EntryGeometry]]:
        pos_entry_geometries: list[tuple[PlaceableGeometry, EntryGeometry]] = []
        if self._os_win:
            pass

        label_x, entry_x = 5, 22
        dist_to_next_entry = 100
        y = 2.5
        width = 8
        for _ in range(3):
            pos_entry_geometries.append((
                PlaceableGeometry(x = label_x, y = y),
                EntryGeometry(x = entry_x, y = y, width = width)
            ))
            label_x += dist_to_next_entry
            entry_x += dist_to_next_entry

        return pos_entry_geometries
