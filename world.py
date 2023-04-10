

class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []

    def addCell(self, cell):
        self.cells.append(cell)
