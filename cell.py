

import random


# enum of the cell types
class CellTypeNames:
	C = "C"
	B = "B"

class CellTypeEnergyCost:
	C = 5
	B = 2

class CellTypeColor:
	C = (0, 255, 0)
	B = (0, 0, 255)

class CellPart:
	def __init__(self, posX, posY, cellPartType, parentCell):
		self.posX = posX
		self.posY = posY
		self.alive = True
		self.numTurnsAlive = 0
		self.parent = parentCell
		self.cellPartType = cellPartType
		self.cellColor = CellTypeColor.__dict__[cellPartType]

	def getPos(self):
		return self.posX, self.posY

	def setPos(self, posX, posY):
		self.posX = posX
		self.posY = posY

	def kill(self):
		self.alive = False
		if (self in self.parent.parts):
			self.parent.parts.remove(self)

	def update(self):
		if (self.cellPartType == "C"):
			self.parent.energy += 5
		elif (self.cellPartType == "B"):
			self.parent.energy -= 1
		
		self.numTurnsAlive += 1
		if (self.numTurnsAlive >= self.parent.cellPartLifeSpan):
			self.kill()


class Cell:
	def __init__(self, posX, posY, startingCellPartType):
		self.parts = []
		self.addPart(posX, posY, startingCellPartType)
		self.alive = True
		self.energy = 10
		self.numTurnsAlive = 0
		self.lastPartPos = (posX, posY)
		self.setupGenetics()

	def setupGenetics(self):
		self.genetics = {}
		self.genetics["PartEnergyRequired"] = random.randint(1, 10)
		self.genetics["PartListMax"] = random.randint(1, 6)
		self.partsTypePlace = 0
		self.genetics["PartTypeList"] = []
		self.genetics["GrothDirection"] = []
		self.cellPartLifeSpan = random.randint(5, 30)
		for i in range(0, self.genetics["PartListMax"]):
			self.genetics["PartTypeList"].append(random.choice([CellTypeNames.C, CellTypeNames.B]))
			self.genetics["GrothDirection"].append(random.choice(["U", "D", "L", "R"]))

	def addPart(self, posX, posY, cellPartType):
		self.parts.append(CellPart(posX, posY, cellPartType, self))
        
	def getParts(self):
		return self.parts

	def kill(self):
		self.alive = False
		for parts in self.parts:
			parts.kill()
  
	def isSingleCell(self):
		return len(self.parts) == 1

	def update(self):
		
		for part in self.parts:
			part.update()
			if not part.alive:
				self.parts.remove(part)
    
		# check if cell should grow
		if (self.energy > self.genetics["PartEnergyRequired"]):

			# choose next part type
			partType = self.genetics["PartTypeList"][self.partsTypePlace]
			self.partsTypePlace += 1

			# make sure we dont go outside the list of parts
			if (self.partsTypePlace >= self.genetics["PartListMax"]):
				self.partsTypePlace = 0

			# add the part
			newPosX = self.lastPartPos[0]
			newPosY = self.lastPartPos[1]
			if(self.genetics["GrothDirection"][self.partsTypePlace] == "U"):
				newPosY -= 1
			elif(self.genetics["GrothDirection"][self.partsTypePlace] == "D"):
				newPosY += 1
			elif(self.genetics["GrothDirection"][self.partsTypePlace] == "L"):
				newPosX -= 1
			elif(self.genetics["GrothDirection"][self.partsTypePlace] == "R"):
				newPosX += 1
			self.addPart(newPosX, newPosY, partType)
			self.lastPartPos = (newPosX, newPosY)

			# remove energy based on the part
			self.energy -= CellTypeEnergyCost.__dict__[partType]
			
  
		# check if cell should move
		if (self.isSingleCell()): # it can move if its a single cell
			posX = self.getParts()[0].getPos()[0]
			posY = self.getParts()[0].getPos()[1]
			self.getParts()[0].setPos(posX + random.randint(-2, 2), posY + random.randint(-1, 1))
		
		# check if cell is should be dead
		if (len(self.parts) == 0):
			self.kill()
		self.energy -= len(self.parts)
		if (self.energy <= 0):
			self.kill()
   
		self.numTurnsAlive += 1
