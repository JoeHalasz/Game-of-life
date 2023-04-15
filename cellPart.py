
CellTypeEnergyGain = [3, -1, -2]

class CellTypeData:
  C = 0
  B = 1
  A = 2

# enum of the cell types
class CellTypeNames:
  C = "C" # chloroplast
  B = "B" # body or connection
  A = "A" # attack

cellNameChoices = [CellTypeNames.C, CellTypeNames.B, CellTypeNames.A]
cellNameChoicesWeighted = [CellTypeNames.C, CellTypeNames.B,CellTypeNames.C, CellTypeNames.B,CellTypeNames.C, CellTypeNames.B, CellTypeNames.A]

class CellTypeEnergyCost:
  C = 5
  B = 2
  A = 5

class CellTypeColor:
  C = (0, 255, 0)
  B = (0, 0, 255)
  A = (255, 0, 0)
  

class CellPart:
  def __init__(self, posX, posY, partType, parentCell):
    self.posX = posX
    self.posY = posY
    self.alive = True
    self.numTurnsAlive = 0
    self.parent = parentCell
    self.partType = partType
    self.cellColor = CellTypeColor.__dict__[partType]

  def getPos(self):
    return self.posX, self.posY

  def setPos(self, posX, posY):
    self.posX = posX
    self.posY = posY

  def kill(self):
    self.alive = False
    if (self in self.parent.parts):
      self.parent.parts[CellTypeData.__dict__[self.partType]].remove(self)
    
    self.parent.checkDead()
    
    try: # this will fail for parts that are off the grid
      if (self.parent.world.parts[self.posX][self.posY] == self):
        self.parent.world.parts[self.posX][self.posY] = None
    except:
      pass