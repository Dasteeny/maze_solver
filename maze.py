import random
import time
from enum import Enum

from cell import Cell
from graphics import Window


class Directions(Enum):
    right = "right"
    left = "left"
    up = "up"
    down = "down"


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
        seed: int = None,
    ):
        self._cells: list[list[Cell]] = []
        self._x1: int = x1
        self._y1: int = y1
        self._num_rows: int = num_rows
        self._num_cols: int = num_cols
        self._cell_size_x: int = cell_size_x
        self._cell_size_y: int = cell_size_y
        self._win: Window = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        if self._win is None:
            return
        x1 = self._x1 + self._cell_size_x * i
        y1 = self._y1 + self._cell_size_y * j
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            if i - 1 >= 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j, Directions.left))
            if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j, Directions.right))
            if j - 1 >= 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1, Directions.up))
            if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1, Directions.down))

            if not to_visit:
                self._draw_cell(i, j)
                return

            to_i, to_j, direction = random.choice(to_visit)
            to_cell = self._cells[to_i][to_j]
            match direction:
                case Directions.right:
                    current_cell.has_right_wall = False
                    to_cell.has_left_wall = False
                case Directions.left:
                    current_cell.has_left_wall = False
                    to_cell.has_right_wall = False
                case Directions.up:
                    current_cell.has_top_wall = False
                    to_cell.has_bottom_wall = False
                case Directions.down:
                    current_cell.has_bottom_wall = False
                    to_cell.has_up_wall = False

            self._break_walls_r(to_i, to_j)

    def _reset_cells_visited(self):
        for cols in self._cells:
            for cell in cols:
                cell.visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i: int, j: int):
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True

        if current_cell == self._cells[-1][-1]:
            return True

        if (
            i - 1 >= 0
            and not current_cell.has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            current_cell.draw_move(self._cells[i - 1][j], True)
        if (
            i + 1 < self._num_cols
            and not current_cell.has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            current_cell.draw_move(self._cells[i + 1][j], True)
        if (
            j - 1 >= 0
            and not current_cell.has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            current_cell.draw_move(self._cells[i][j - 1], True)
        if (
            j + 1 < self._num_rows
            and not current_cell.has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            current_cell.draw_move(self._cells[i][j + 1], True)

        return False
