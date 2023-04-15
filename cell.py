import random
from collections import deque
from cellPart import *


class Cell:
  def __init__(self, posX, posY, startingpartType, world, generation=0, oldGenetics=None):
    self.id = world.getNextCellId()
    self.parts = []
    for _ in cellNameChoices:
      self.parts.append(deque([]))
    self.alive = True
    self.energy = 10
    self.numTurnsAlive = 0
    self.lastPartPos = (posX, posY)
    self.generation = generation
    self.world = world
    self.setupGenetics(oldGenetics)

    # spawn part has to happen last
    spawnedPart = self.spawnNewPart(CellPart(posX, posY, startingpartType, self))
    if not spawnedPart:
      self.kill()

  def setupGenetics(self, oldGenetics):
    random.seed(self.id)
    self.genetics = {}
    if (oldGenetics == None): # if this the first generation
      self.partsTypePlace = 0
      self.genetics["PartEnergyRequired"] = random.randint(5, 15)
      self.genetics["PartListMax"] = random.randint(5, 15)
      self.genetics["PartTypeList"] = []
      self.genetics["GrowthDirection"] = []
      self.genetics["cellPartLifeSpan"] = random.randint(15, 45)
      self.genetics["MaxStoredEnergy"] = random.randint(30, 100)

      self.genetics["PartTypeList"].append("B")
      self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))
      for i in range(1, self.genetics["PartListMax"]):
        if (self.genetics["PartTypeList"][i-1] == "B"): # make sure that new parts are connected to B parts
          self.genetics["PartTypeList"].append(random.choice(cellNameChoicesWeighted))
        else:
          self.genetics["PartTypeList"].append("B")
        self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))
    else: # if this is not the first generation
      self.genetics = oldGenetics
      self.partsTypePlace = 0
      # for all the genetics, there is a .1% chance that it will mutate
      for key in self.genetics:
        if (random.randint(0, 1000) == 0):
          if (key == "PartEnergyRequired" or key == "PartListMax"or key == "cellPartLifeSpan"):
            self.genetics[key] += random.choice([-2, -1, 1, 2])
          if (self.genetics["PartListMax"] <= 0):
            self.genetics["PartListMax"] = 1
          if key == "PartListMax":
            if (self.genetics[key] < oldGenetics[key]):
              self.genetics["PartTypeList"] = self.genetics["PartTypeList"][:self.genetics["PartListMax"]]
              self.genetics["GrowthDirection"] = self.genetics["GrowthDirection"][:self.genetics["PartListMax"]]
            else:
              self.genetics["PartTypeList"] = []
              self.genetics["GrowthDirection"] = []
              for i in range(self.genetics["PartListMax"]):
                if (i < len(oldGenetics["PartTypeList"])):
                  self.genetics["PartTypeList"].append(oldGenetics["PartTypeList"][i])
                else:
                  self.genetics["PartTypeList"].append(random.choice(cellNameChoicesWeighted))
                if (i < len(oldGenetics["GrowthDirection"])):
                  self.genetics["GrowthDirection"].append(oldGenetics["GrowthDirection"][i])
                else:
                  self.genetics["GrowthDirection"].append(random.choice(["U", "D", "L", "R"]))

      for i in range(self.genetics["PartListMax"]):
        if (random.randint(0, 1000) == 0):
          self.genetics["PartTypeList"][i] = random.choice(cellNameChoicesWeighted)
      for i in range(0, self.genetics["PartListMax"]):
        if (random.randint(0, 1000) == 0):
          self.genetics["GrowthDirection"][i] = random.choice(["U", "D", "L", "R"])

  def getParts(self):
    return self.parts

  def kill(self):
    self.alive = False
    for partsList in self.parts:
      for part in partsList:
        part.kill()
    self.world.removeCell(self)
    
  def checkDead(self):
    if (self.getTotalParts() == 0):
      self.kill()
  
  def isSingleCell(self):
    return self.getTotalParts() == 1

  # return false if it cant spawn one there
  def spawnNewCell(self, cell):
    cellPart = None
    for i in range(len(cell.parts)): 
      if (len(cell.parts[i]) != 0):
        cellPart = cell.parts[i][0]
        break
    
    if (cellPart == None):
      return False
    spawnedPart = self.spawnNewPart(cellPart)
    if (spawnedPart):
      # add the new cell to the list of cells
      self.world.addCell(cell)
      return True
    return False

  def spawnNewPart(self, part):
    posX = part.posX
    posY = part.posY
    # check if a part can be added there
    if (posX > 0 and posX < self.world.width-1 and posY > 0 and posY < self.world.height-1):
      if self.world.getAlivePartAtPos(posX, posY) == None or self.world.getAlivePartAtPos(posX, posY) == part:
        if part.partType == "C":
          # if the any of the 4 squares around this are a C then return false
          if  ((self.world.getPartAtPos(posX+1, posY) != None and self.world.getPartAtPos(posX+1, posY).partType == "C") 
            or (self.world.getPartAtPos(posX-1, posY) != None and self.world.getPartAtPos(posX-1, posY).partType == "C")
            or (self.world.getPartAtPos(posX, posY+1) != None and self.world.getPartAtPos(posX, posY+1).partType == "C")
            or (self.world.getPartAtPos(posX, posY-1) != None and self.world.getPartAtPos(posX, posY-1).partType == "C")):
            return False, "Another C is too close"
        # add the part if there is no part there
        if (self.world.getPartAtPos(posX, posY) != None and self.world.getPartAtPos(posX, posY).partType == "C"):
          return False, "Another part is on that position"
        self.lastPartPos = (posX, posY)
        removedPart = self.world.addPart(part)
        # remove energy based on the part
        self.energy -= CellTypeEnergyCost.__dict__[part.partType]
        self.parts[CellTypeData.__dict__[part.partType]].append(part)
        part.whenToDie = self.numTurnsAlive + self.genetics["cellPartLifeSpan"]
        return True, ""
      elif (self.world.getAlivePartAtPos(posX, posY).partType == "A"):
          # act like the part was added but it gets eaten by the A part
          self.world.getAlivePartAtPos(posX, posY).parent.energy += CellTypeEnergyCost.__dict__[part.partType]
          # remove energy based on the part
          self.energy -= CellTypeEnergyCost.__dict__[part.partType]
          return True, "The new part was eaten by an A part"
      else:
        return False, "Something is in the way"
    else:
      return False, "Outside world bounds"
          
  def getTotalParts(self):
    total = 0
    for partList in self.parts:
      total += len(partList)
    return total
  
  def update(self):
    for i in range(len(self.parts)):
      partsList = self.parts[i]
      self.energy += CellTypeEnergyGain[i] * len(partsList)
      while len(partsList) > 0:
        # check first part, if it should be dead then kill it, if it shouldnt then break
        if partsList[0].whenToDie <= self.numTurnsAlive:
          partsList[0].kill()
          partsList.popleft()
        else:
          break
    if self.getTotalParts() == 0:
      self.kill()
        
    # check if cell should bud
    if (random.randint(0, 1) == 0 and self.energy > self.genetics["MaxStoredEnergy"]/2 and 
        self.energy > self.genetics["PartEnergyRequired"] and
        self.getTotalParts() >= self.genetics["PartListMax"]/2):
      spawnDirection = random.choice([(0,-1), (0,1), (-1,0), (1,0)])
      newPosX = self.lastPartPos[0] + spawnDirection[0]
      newPosY = self.lastPartPos[1] + spawnDirection[1]
      newCell = Cell(newPosX, newPosY, "C", self.world, self.generation + 1, self.genetics)
      spawned = self.spawnNewCell(newCell)

    # check if cell should grow
    else:
      numTries = 0
      self.partsTypePlace += 1
      while (self.energy > self.genetics["PartEnergyRequired"]):
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
        addedPart, failReason = self.spawnNewPart(newPart)
        if (addedPart or failReason != "Another C is too close" or numTries > 10): # try to spawn up to 10 new parts
          break
        self.partsTypePlace += 1
        numTries += 1
    
    # check if cell is should be dead
    if (self.getTotalParts == 0):
      self.kill()
    if (self.energy <= 0):
      self.kill()
    
    self.numTurnsAlive += 1
