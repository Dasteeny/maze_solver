from graphics import Line, Point, Window


class Cell:
    def __init__(self, win: Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_left_wall:
            self._win.draw_line(
                Line(
                    Point(self._x1, self._y1),
                    Point(self._x1, self._y2),
                )
            )
        if self.has_top_wall:
            self._win.draw_line(
                Line(
                    Point(self._x1, self._y1),
                    Point(self._x2, self._y1),
                )
            )
        if self.has_right_wall:
            self._win.draw_line(
                Line(
                    Point(self._x2, self._y1),
                    Point(self._x2, self._y2),
                )
            )
        if self.has_bottom_wall:
            self._win.draw_line(
                Line(
                    Point(self._x1, self._y2),
                    Point(self._x2, self._y2),
                )
            )

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        current_half_length_x = abs(self._x2 - self._x1) // 2
        current_half_length_y = abs(self._y2 - self._y1) // 2

        current_x_center = self._x1 + current_half_length_x
        current_y_center = self._y1 + current_half_length_y

        to_cell_half_length_x = abs(to_cell._x2 - to_cell._x1) // 2
        to_cell_half_length_y = abs(to_cell._y2 - to_cell._y1) // 2

        to_cell_x_center = to_cell._x1 + to_cell_half_length_x
        to_cell_y_center = to_cell._y1 + to_cell_half_length_y

        fill_color = "grey" if undo else "red"

        self._win.draw_line(
            line=Line(
                Point(current_x_center, current_y_center),
                Point(to_cell_x_center, to_cell_y_center),
            ),
            fill_color=fill_color,
        )
