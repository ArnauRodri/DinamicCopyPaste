import tkinter as tk

from logic import WindowLogic


STORED_FRAME_PADDING = 5

STORED_LABEL_PADDING = 5

STORED_LABEL_DIM_X = 20
STORED_LABEL_DIM_Y = 10

STORED_FRAME_DIM_X = 184

WIN_DIM_X = 738
WIN_DIM_Y = 205
WIN_TITTLE = "DCP"

CANVAS_DIM_X = WIN_DIM_X - 2
CANVAS_DIM_Y = 193


class StoredSlot:
    _padding_frame: tk.Frame
    _main_frame: tk.Frame
    _parent = tk.Widget

    def __init__(self, parent: tk.Widget) -> None:
        self._parent = parent

        self._padding_frame = tk.Frame(self._parent)

        self._main_frame = tk.Frame(self._padding_frame)
        self._main_frame.pack(padx=STORED_FRAME_PADDING, pady=STORED_FRAME_PADDING)

        self._str_var_stored = tk.StringVar()

        self._stored_label = tk.Label(self._main_frame, textvariable=self._str_var_stored,
                                      width=STORED_LABEL_DIM_X, height=STORED_LABEL_DIM_Y, bg='white')

        self._stored_label.pack(padx=STORED_LABEL_PADDING, pady=STORED_LABEL_PADDING)

        self.un_hover()

    def get_ui(self) -> tk.Frame:
        return self._padding_frame

    def hover(self) -> None:
        self._padding_frame.config(bg='light green')

    def un_hover(self) -> None:
        self._padding_frame.config(bg='light blue')


class StoredFrame(StoredSlot):

    def __init__(self, parent: tk.Widget, text: str) -> None:
        super().__init__(parent)
        self.update_text(text)

    def update_text(self, text: str) -> None:
        self._str_var_stored.set(text)


class AddFrame(StoredSlot):

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self._str_var_stored.set("[NEW]")


class DCPWindow:
    _win: tk.Tk
    _on_close_function: ()

    _array_stored_frames: list[StoredFrame]
    _add_frame: AddFrame

    _scroll: tk.Scrollbar

    _canvas_in_frame: tk.Frame

    _win_logic: WindowLogic

    def __init__(self, on_close_function: (), win_logic: WindowLogic) -> None:
        self._win = tk.Tk()
        self._on_close_function = on_close_function
        self._array_stored_frames = []
        self._canvas = tk.Canvas(self._win)
        self._win_logic = win_logic

        self._win.protocol("WM_DELETE_WINDOW", self._on_closing)

        self._init_gui()

        self._bindings()

        self._win.mainloop()

    def _bindings(self) -> None:
        self._win.bind('c', lambda event: self._c())
        self._win.bind('v', lambda event: self._v())
        self._win.bind('x', lambda event: self._x())

        self._win.bind('<Tab>', lambda event: self._forward())
        self._win.bind('<Shift-KeyPress-\t>', lambda event: self._backward())
        self._win.bind('<Right>', lambda event: self._forward())
        self._win.bind('<Left>', lambda event: self._backward())

        self._win.bind('<Return>', lambda event: self._enter())

    def _init_gui(self) -> None:
        self._win.minsize(WIN_DIM_X, WIN_DIM_Y)
        self._win.maxsize(WIN_DIM_X, WIN_DIM_Y)
        self._win.title(WIN_TITTLE)

        self._canvas.grid(row=0, column=0)

        self._scroll = tk.Scrollbar(self._win, orient=tk.HORIZONTAL, command=self._canvas.xview)
        self._scroll.grid(row=1, column=0, sticky=tk.EW)

        self._canvas.config(xscrollcommand=self._scroll.set)

        self._canvas_in_frame = tk.Frame(self._canvas)
        self._canvas_in_frame.pack()

        self._canvas.create_window(0, 0, window=self._canvas_in_frame, anchor=tk.NW)

        self._canvas.config(width=CANVAS_DIM_X, height=CANVAS_DIM_Y)

        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

        self._add_frame = AddFrame(self._canvas_in_frame)
        self._add_frame.get_ui().pack(side=tk.LEFT)
        self._add_frame.hover()

        self._canvas_in_frame.config(
            width=max(STORED_FRAME_DIM_X * (len(self._win_logic.stored_array) + 1), CANVAS_DIM_X))
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

        self._set_center_view()

    def _text_update(self) -> None:
        self._array_stored_frames[self._win_logic.get_index()].update_text(self._win_logic.get_stored().text)

    def _add_update(self) -> None:
        self._add_frame.get_ui().destroy()

        self._array_stored_frames.append(StoredFrame(self._canvas_in_frame, '[EMPTY]'))
        self._array_stored_frames[-1].get_ui().pack(side=tk.LEFT)
        self._array_stored_frames[-1].hover()

        self._add_frame = AddFrame(self._canvas_in_frame)
        self._add_frame.get_ui().pack(side=tk.LEFT)

    def _remove_update(self) -> None:
        self._array_stored_frames[self._win_logic.get_index()].get_ui().destroy()
        self._array_stored_frames.pop(self._win_logic.get_index())

        if len(self._array_stored_frames) <= self._win_logic.get_index():
            self._add_frame.hover()
        else:
            self._array_stored_frames[self._win_logic.get_index()].hover()

    def _move_update(self) -> None:
        for stored_frame in self._array_stored_frames:
            stored_frame.un_hover()

        if self._win_logic.get_index() == len(self._win_logic.stored_array):
            self._add_frame.hover()
        else:
            self._add_frame.un_hover()

        if 0 <= self._win_logic.get_index() < len(self._array_stored_frames):
            self._array_stored_frames[self._win_logic.get_index()].hover()

        self._update_scroll_size()
        self._set_center_view()

    def _reset_canvas_in_frame(self) -> None:
        for item in self._canvas_in_frame.winfo_children():
            item.destroy()

    def _on_closing(self) -> None:
        self._on_close_function()
        self._win.destroy()

    def _c(self) -> None:
        if not self._win_logic.is_on_add():
            self._win_logic.get_stored().load()

    def _v(self) -> None:
        if not self._win_logic.is_on_add():
            self._win_logic.get_stored().unload()
            self._text_update()

    def _x(self) -> None:
        if not self._win_logic.is_on_add():
            self._win_logic.remove()
            self._remove_update()

    def _forward(self) -> None:
        self._win_logic.next_stored()
        self._move_update()

    def _backward(self) -> None:
        self._win_logic.previous_stored()
        self._move_update()

    def _enter(self) -> None:
        if self._win_logic.is_on_add():
            self._win_logic.add_stored()
            self._win_logic.get_stored().update('[EMPTY]')
            self._add_update()

    def _update_scroll_size(self) -> None:
        self._canvas_in_frame.config(
            width=max(STORED_FRAME_DIM_X * (len(self._win_logic.stored_array) + 1), CANVAS_DIM_X))
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

    def _set_center_view(self) -> None:
        self._canvas.xview_moveto(
            ((self._win_logic.get_index() - 1.5) / (len(self._win_logic.stored_array) + 1)))
