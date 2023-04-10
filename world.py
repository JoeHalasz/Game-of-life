

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

    def addPart(self, part):
        foundOne = False
        if (self.parts[part.posX][part.posY]) != None:
            foundOne = True

        self.parts[part.posX][part.posY] = part
        return foundOne
    
    # ONLY CHECK THIS IF WE ARE TRYING TO ADD SOMETHING TO THE TILE
    def hasAlivePartAtPos(self, posX, posY):
        # give the eater part energy if this is checked
        if (self.parts[posX][posY] != None and self.parts[posX][posY].alive and self.parts[posX][posY].cellPartType == "A"):
            self.parts[posX][posY].parent.energy += 5
        return self.parts[posX][posY] != None and self.parts[posX][posY].alive