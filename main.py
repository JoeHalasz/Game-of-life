from game import Game
from world import World
from cell import Cell
import time


if __name__ == "__main__":

    fps = 8
    lastTime = time.time()
    world = World(62)
    world.addCell(Cell(15,15, "C"))
    while True:
        deltaTime = time.time() - lastTime
        if (deltaTime < (1/fps)):
            continue

        Game.turn(world, deltaTime)
        lastTime = time.time()

        world.printWorld()
        world.clearWorld()
