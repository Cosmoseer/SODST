from tkinter import Frame, StringVar, OptionMenu, LabelFrame, Entry, Label
from orbit_visualiser.ui.common.fonts import subtitle_font

class VectorInputFrame(LabelFrame):

    def __init__(self, master, components: list[str] | None = None, cnf = ..., *, background = ..., bg = ..., class_ = "Labelframe", colormap = "", container = False, cursor = "", fg = ..., foreground = ..., height = 0, highlightbackground = ..., highlightcolor = ..., highlightthickness = 0, labelanchor = "nw", labelwidget = ..., name = ..., padx = 0, pady = 0, takefocus = 0, text = "", visual = "", width = 0):
        super().__init__(master, cnf, background=background, bd=2, border=2, borderwidth=2, bg=bg, class_=class_, colormap=colormap, container=container, cursor=cursor, fg=fg, font=subtitle_font, foreground=foreground, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, labelanchor=labelanchor, labelwidget=labelwidget, name=name, padx=padx, pady=pady, relief="sunken", takefocus=takefocus, text=text, visual=visual, width=width)
        self._root = master
        self._comps = components if components else ["x", "y", "z"]


class ScalarInputFrame(LabelFrame):

    def __init__(self, master = None, cnf = ..., *, background = ..., bd = 2, bg = ..., border = 2, borderwidth = 2, class_ = "Labelframe", colormap = "", container = False, cursor = "", fg = ..., font = "TkDefaultFont", foreground = ..., height = 0, highlightbackground = ..., highlightcolor = ..., highlightthickness = 0, labelanchor = "nw", labelwidget = ..., name = ..., padx = 0, pady = 0, relief = "groove", takefocus = 0, text = "", visual = "", width = 0):
        super().__init__(master, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, fg=fg, font=font, foreground=foreground, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, labelanchor=labelanchor, labelwidget=labelwidget, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, text=text, visual=visual, width=width)