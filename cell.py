

import random


# enum of the cell types
class CellTypeNames:
  C = "C" # chloroplast
  B = "B" # body or connection
  A = "A" # attack

cellNameChoices = [CellTypeNames.C, CellTypeNames.B,CellTypeNames.C, CellTypeNames.B,CellTypeNames.C, CellTypeNames.B, CellTypeNames.A]

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
      self.parent.parts.remove(self)
    try: # this will fail for parts that are off the grid
      self.parent.world.parts[self.posX][self.posY] = None
    except:
      pass
    self.parent.checkDead()

  def update(self):
    if (self.partType == "C"):
      self.parent.energy += 3
    elif (self.partType == "B"):
      self.parent.energy -= 1
    elif (self.partType == "A"):
      self.parent.energy -= 2
    
    self.numTurnsAlive += 1
    if (self.numTurnsAlive >= self.parent.genetics["cellPartLifeSpan"]):
      self.kill()
    # if its outside the playzone, kill it
    if self.posX < 2 or self.posX > self.parent.world.width or self.posY < 2 and self.posY > self.parent.world.height:
      self.kill()

class Cell:
  def __init__(self, posX, posY, startingpartType, world, generation=0, oldGenetics=None):
    self.parts = []
    self.alive = True
    self.energy = 10
    self.numTurnsAlive = 0
    self.lastPartPos = (posX, posY)
    self.generation = generation
    self.world = world
    self.setupGenetics(oldGenetics)

    # spawn part has to happen last
    self.spawnNewPart(CellPart(posX, posY, startingpartType, self), True)


  def setupGenetics(self, oldGenetics):
    self.genetics = {}
    if (oldGenetics == None): # if this the first generation
      self.partsTypePlace = 0
      self.genetics["PartEnergyRequired"] = random.randint(1, 10)
      self.genetics["PartListMax"] = random.randint(5, 15)
      self.genetics["PartTypeList"] = []
      self.genetics["GrowthDirection"] = []
      self.genetics["cellPartLifeSpan"] = random.randint(5, 30)
      self.genetics["MaxStoredEnergy"] = random.randint(30, 100)

      self.genetics["PartTypeList"].append("B")
      self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))
      for i in range(1, self.genetics["PartListMax"]):
        if (self.genetics["PartTypeList"][i-1] == "B"): # make sure that new parts are connected to B parts
          self.genetics["PartTypeList"].append(random.choice(cellNameChoices))
        else:
          self.genetics["PartTypeList"].append("B")
        self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))
    else: # if this is not the first generation
      self.genetics = oldGenetics
      self.partsTypePlace = 0
      # for all the genetics, there is a 1% chance that it will mutate
      for key in self.genetics:
        if (random.randint(0, 100) == 0):
          if (key == "PartEnergyRequired" or key == "PartListMax"or key == "cellPartLifeSpan"):
            self.genetics[key] += random.choice([-2, -1, 1, 2])
          if (self.genetics["PartListMax"] <= 0):
            self.genetics["PartListMax"] = 1
          if key == "PartListMax":
            if (self.genetics[key] < oldGenetics[key]):
              self.genetics["PartTypeList"] = self.genetics["PartTypeList"][0:self.genetics["PartListMax"]]
              self.genetics["GrowthDirection"] = self.genetics["GrowthDirection"][0:self.genetics["PartListMax"]]
            else:
              self.genetics["PartTypeList"] = []
              self.genetics["GrowthDirection"] = []
              for i in range(0, self.genetics["PartListMax"]):
                if (i < len(oldGenetics["PartTypeList"])):
                  self.genetics["PartTypeList"].append(oldGenetics["PartTypeList"][i])
                else:
                  self.genetics["PartTypeList"].append(random.choice(cellNameChoices))
                if (i < len(oldGenetics["GrowthDirection"])):
                  self.genetics["GrowthDirection"].append(oldGenetics["GrowthDirection"][i])
                else:
                  self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))

      for i in range(0, self.genetics["PartListMax"]):
        if (random.randint(0, 100) == 0):
          self.genetics["PartTypeList"][i] = random.choice(cellNameChoices)
      for i in range(0, self.genetics["PartListMax"]):
        if (random.randint(0, 100) == 0):
          self.genetics["GrowthDirection"][i] = random.choice(["U", "D", "L", "R"])

  def getParts(self):
    return self.parts

  def kill(self):
    self.alive = False
    for parts in self.parts:
      parts.kill()
    self.world.removeCell(self)
    
  def checkDead(self):
    if (len(self.parts) == 0):
      self.kill()
  
  def isSingleCell(self):
    return len(self.parts) == 1

  # return false if it cant spawn one there
  def spawnNewCell(self, cell):
    spawnedPart = self.spawnNewPart(cell.parts[0])
    if (spawnedPart):
      # add the new cell to the list of cells
      self.world.addCell(cell)
      return True
    return False

  def spawnNewPart(self, part, force=False):
    posX = part.posX
    posY = part.posY
    # check if a part can be added there
    if (force or (posX > 1 and posX < self.world.width and posY > 1 and posY < self.world.height)):
      if force or (self.world.getAlivePartAtPos(posX, posY) == None or self.world.getAlivePartAtPos(posX, posY) == part or part.partType == "A"):
        if (not force) and (part.partType == "C"):
          # if the any of the 4 squares around this are a C then return false
          if ((self.world.getPartAtPos(posX+1, posY) != None and self.world.getPartAtPos(posX+1, posY) == "C") 
            or (self.world.getPartAtPos(posX-1, posY) != None and self.world.getPartAtPos(posX-1, posY) == "C")
            or (self.world.getPartAtPos(posX, posY+1) != None and self.world.getPartAtPos(posX, posY+1) == "C")
            or (self.world.getPartAtPos(posX, posY-1) != None and self.world.getPartAtPos(posX, posY-1) == "C")):
            return False
        # add the part
        self.partsTypePlace += 1
        self.lastPartPos = (posX, posX)
        removedPart = self.world.addPart(part)
        # if we are adding an A part and there was a part then give energy based on the part
        if (removedPart != None and part.partType == "A"):
          self.energy += CellTypeEnergyCost.__dict__[removedPart.partType]
        # remove energy based on the part
        self.energy -= CellTypeEnergyCost.__dict__[part.partType]
        self.parts.append(part)
        return True
    return False
          

  def update(self):
    for part in self.parts:
      part.update()
      try:
        if not part.alive:
          self.parts.remove(part)
      except:
        pass
      
    # check if cell should bud
    if (random.randint(0, 1) == 0 and self.energy > self.genetics["MaxStoredEnergy"]/2 and 
        self.energy > self.genetics["PartEnergyRequired"] and
        len(self.parts) >= self.genetics["PartListMax"]/2):
      spawnDirection = random.choice([(0,-1), (0,1), (-1,0), (1,0)])
      newPosX = self.lastPartPos[0] + spawnDirection[0]
      newPosY = self.lastPartPos[1] + spawnDirection[1]
      newCell = Cell(newPosX, newPosY, "C", self.world, self.generation + 1, self.genetics)
      spawned = self.spawnNewCell(newCell)

    # check if cell should grow
    elif (self.energy > self.genetics["PartEnergyRequired"]):
      # make sure we dont go outside the list of parts
      if (self.partsTypePlace >= self.genetics["PartListMax"]):
        self.partsTypePlace = 0

      # choose next part type
      partType = self.genetics["PartTypeList"][self.partsTypePlace]			

      # get the next pos
      newPosX = self.lastPartPos[0]
      newPosY = self.lastPartPos[1]
      if(self.genetics["GrowthDirection"][self.partsTypePlace] == "U"):
        newPosY -= 1
      elif(self.genetics["GrowthDirection"][self.partsTypePlace] == "D"):
        newPosY += 1
      elif(self.genetics["GrowthDirection"][self.partsTypePlace] == "L"):
        newPosX -= 1
      elif(self.genetics["GrowthDirection"][self.partsTypePlace] == "R"):
        newPosX += 1

      newPart = CellPart(newPosX, newPosY, partType, self)
      addedPart = self.spawnNewPart(newPart)

    # check if cell should move
    if (self.isSingleCell()): # it can move if its a single cell
      posX = self.getParts()[0].getPos()[0]
      posY = self.getParts()[0].getPos()[1]
      self.getParts()[0].setPos(posX + random.randint(-1, 1), posY + random.randint(-1, 1))
      # if its outside the world, kill it
      if (self.getParts()[0].posX < 1 or self.getParts()[0].posY < 1 or self.getParts()[0].posX > self.world.width or self.getParts()[0].posY > self.world.height):
        self.kill()
      self.energy -= 1
    
    # check if cell is should be dead
    if (len(self.parts) == 0):
      self.kill()
    self.energy -= len(self.parts)
    if (self.energy <= 0):
      self.kill()
    
    self.numTurnsAlive += 1
