

class World:

    def __init__(self, height):
        self.world = []
        self.cells = []
        self.height = height
        self.width = height * 2

        for i in range(height):
            self.world.append([])

        for i in range(self.width):
            self.world[0].append("-")

        for i in range(1, height-1):
            self.world[i].append("|")
            for j in range(1, self.width - 1):
                self.world[i].append(" ")
            self.world[i].append("|")

        for i in range(self.width):
            self.world[height-1].append("-")

    def printWorld(self):
        str = "".join(self.world[0])
        for i in range(1, len(self.world)):
            str += "\n" + "".join(self.world[i])
        str += "\n"
        print(str, end="")
        
    def drawCell(self, cell):
        for part in cell.parts:
            if (part.posX < 0 or part.posX >= self.width-1 or part.posY < 0 or part.posY >= self.height-1):
                part.kill()
            else:
                self.world[part.posY][part.posX] = part.cellPartType
    
    def clearWorld(self):
        for cell in self.cells:
            for part in cell.parts:
                self.world[part.posY][part.posX] = " "     

    def addCell(self, cell):
        self.cells.append(cell)
