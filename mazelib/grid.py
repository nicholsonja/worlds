import re
from .cell import Cell
from random import randrange
from math import pi


class Grid:
    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        self.end = []

    def prepare_grid(self):
        grid_array = []
        for row in range(self.rows):
            row_array = []
            for column in range(self.columns):
                row_array.append(Cell(row, column))
            grid_array.append(row_array)
        return grid_array

    def configure_cells(self):
        for row in self.grid:
            for cell in row:
                row, col = cell.row, cell.column
                cell.north = self.get_neighbor(row - 1, col)
                cell.south = self.get_neighbor(row + 1, col)
                cell.west = self.get_neighbor(row, col - 1)
                cell.east = self.get_neighbor(row, col + 1)

    def get_neighbor(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]
        return None

    def random_cell(self):
        return self.grid[randrange(self.rows)][randrange(self.columns)]

    def size(self):
        return self.rows * self.columns

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        cells = []
        for row in self.grid:
            for cell in row:
                cells.append(cell)
        return cells

    def contents_of(self, cell):
        return " "

    def background_color_for(self, cell):
        return None

    def to_string(self, cell_width=3, do_print=True, filename=None):
        if cell_width < 2:
            raise ValueError("cell_width < 2")

        result = ["#" + ("#"*cell_width) * self.columns]
        # print("LINE LENGTH = ", len(result[0]))

        for row_num, row in enumerate(self.grid):
            top = '#'
            bottom = '#'

            for col_num, cell in enumerate(row):
                if row_num == self.rows-1 and col_num == 0:
                    contents = "R" + " " * (cell_width-2)
                else:
                    contents = " " * (cell_width-1)

                body = contents

                # east_boundary = " " if cell.linked(cell.east) else "#"
                if cell.linked(cell.east):
                    east_boundary = " "
                elif row_num == 0 and col_num == self.columns-1:
                    east_boundary = "E"
                else:
                    east_boundary = "#"

                top = top + body + east_boundary
                # south_boundary = (" " if cell.linked(cell.south) else '#') * cell_width
                if cell.linked(cell.south):
                    south_boundary = " " * (cell_width - 1)
                else:
                    south_boundary = "#" * (cell_width - 1)
                corner = '#'
                bottom = bottom + south_boundary + corner

            for _ in range(cell_width-1):
                result.append(top)

            result.append(bottom)

        result = '\n'.join(result)

        # HACK TO GET RID OF EXTRA E's AND R's
        if cell_width > 2:
            result = re.sub("E", "#", result[::-1], count=cell_width-2)
            result = re.sub("R", " ", result[::-1], count=cell_width-2)

        if filename:
            with open(filename, "w") as f:
                f.write(result)

        if do_print:
            print(result)
        else:
            return result
