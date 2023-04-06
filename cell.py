

import random


class CellPart:
	def __init__(self, posX, posY, cellPartType, parentCell):
		self.posX = posX
		self.posY = posY
		self.cellPartType = cellPartType
		self.alive = True
		self.numTurnsAlive = 0
		self.parent = parentCell

	def getPos(self):
		return self.posX, self.posY

	def setPos(self, posX, posY):
		self.posX = posX
		self.posY = posY

	def kill(self):
		self.alive = False

	def update(self):
		if (self.cellPartType == "c"):
			self.par
		self.numTurnsAlive += 1


class Cell:
	def __init__(self, posX, posY, startingCellPartType):
		self.parts = []
		self.addPart(posX, posY, startingCellPartType)
		self.alive = True
		self.energy = 10
		self.numTurnsAlive = 0

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
		if (self.energy == 5):
			self.addPart(self.posX, self.posY)
			self.energy = 10
  
		# check if cell should move
		if (self.isSingleCell()): # it can move if its a single cell
			self.posX += random.randint(-2, 2)
			self.posY += random.randint(-1, 1)
		
		# check if cell is should be dead
		if (len(self.parts) == 0):
			self.kill()
		self.energy -= len(self.parts)
		if (self.energy <= 0):
			self.kill()
   
		self.numTurnsAlive += 1
