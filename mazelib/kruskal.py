from random import shuffle


class State:
    def __init__(self, grid):
        self.grid = grid
        self.neighbors = []
        self.set_for_cell = {}
        self.cells_in_set = {}

        for cell in grid.each_cell():
            set = len(self.set_for_cell)

            self.set_for_cell[cell] = set
            self.cells_in_set[set] = [cell]

            if cell.south:
                self.neighbors.append([cell, cell.south])
            if cell.east:
                self.neighbors.append([cell, cell.east])

    def can_merge(self, left, right):
        return self.set_for_cell[left] != self.set_for_cell[right]

    def merge(self, left, right):
        left.link(right)

        winner = self.set_for_cell[left]
        loser = self.set_for_cell[right]
        if loser in self.cells_in_set:
            losers = self.cells_in_set[loser]
        else:
            losers = self.cells_in_set[right]

        for cell in losers:
            self.cells_in_set[winner].append(cell)
            self.set_for_cell[cell] = winner

        del self.cells_in_set[loser]


class Kruskals:
    @staticmethod
    def on(grid, state=None):
        if state is None:
            state = State(grid)

        neighbors = state.neighbors[::]
        shuffle(neighbors)

        while len(neighbors) > 0:
            left, right = neighbors.pop()
            if state.can_merge(left, right):
                state.merge(left, right)
