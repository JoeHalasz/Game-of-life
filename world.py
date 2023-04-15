

class World:

    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.cells = []
        self.parts = []
        self.nextCellId = 0
        for i in range(self.width):
            self.parts.append([])
            for j in range(self.height):
                self.parts[i].append(None)

    def getNextCellId(self):
        self.nextCellId += 1
        return self.nextCellId
    
    def addCell(self, cell):
        self.cells.append(cell)

    def removeCell(self, cell):
        for partsList in cell.parts:
            for part in partsList:
                cell.world.parts[part.posX][part.posY] = None

        if cell in self.cells:
            self.cells.remove(cell)

    def addPart(self, part):
        oldPart = None
        if (part.posX < 0 or part.posX >= self.width or part.posY < 0 or part.posY >= self.height):
            return None
        if self.parts[part.posX][part.posY] != None and self.parts[part.posX][part.posY] != part:
            oldPart = self.parts[part.posX][part.posY]
            oldPart.kill()

        self.parts[part.posX][part.posY] = part
        return oldPart
    
    def getAlivePartAtPos(self, posX, posY):
        if self.parts[posX][posY] != None and self.parts[posX][posY].alive:
            return self.parts[posX][posY]
        return None

    def getPartAtPos(self, posX, posY):
        if (posX < 0 or posX >= self.width or posY < 0 or posY >= self.height):
            return None
        return self.parts[posX][posY]