

class Game:
	def turn(world, deltaTime):
		for cell in world.cells:
			cell.update()
			world.drawCell(cell)
