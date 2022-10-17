class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.links = {}

    def link(self, cell, bidi=True):
        self.links[cell] = True
        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True):
        if cell in self.links:
            del self.links[cell]
        if bidi:
            cell.unlink(self, False)

    def get_links(self):
        return self.links.keys()

    def linked(self, cell):
        if cell in self.links:
            return True
        return False

    def neighbors(self):
        lst = []
        if self.north:
            lst.append(self.north)
        if self.south:
            lst.append(self.south)
        if self.west:
            lst.append(self.west)
        if self.east:
            lst.append(self.east)
        return lst
