

class World:

    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.cells = []
        self.parts = []
        for i in range(self.width):
            self.parts.append([])
            for j in range(self.height):
                self.parts[i].append(None)

    def addCell(self, cell):
        self.cells.append(cell)

    def removeCell(self, cell):
        for cellPart in cell.parts:
            cell.world.parts[cellPart.posX][cellPart.posY] = None
        if cell in self.cells:
            self.cells.remove(cell)

    def addPart(self, part):
        oldPart = None
        if (part.posX < 0 or part.posX >= self.width or part.posY < 0 or part.posY >= self.height):
            return None
        if (self.parts[part.posX][part.posY]) != None:
            oldPart = self.parts[part.posX][part.posY]
            oldPart.kill()

        self.parts[part.posX][part.posY] = part
        return oldPart
    
    # ONLY CHECK THIS IF WE ARE TRYING TO ADD SOMETHING TO THE TILE
    def getAlivePartAtPos(self, posX, posY):
        if self.parts[posX][posY] != None and self.parts[posX][posY].alive:
            return self.parts[posX][posY]
        return None

    def getPartAtPos(self, posX, posY):
        if (posX < 0 or posX >= self.width or posY < 0 or posY >= self.height):
            return None
        return self.parts[posX][posY]