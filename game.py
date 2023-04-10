import pygame
from world import World
from cell import Cell
import random

def events():
  # make the game quit when control and q are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] and keys[pygame.K_LCTRL]:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        quit()


class Game:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("Game of Life")
    # make the screen fullscreen
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # get the screen dimentions
    self.screen_width = self.screen.get_width()
    self.screen_height = self.screen.get_height()

    self.clock = pygame.time.Clock()

    # create world
    self.blockSize = 16
    self.world = World(self.screen_width/self.blockSize, self.screen_height/self.blockSize)
    for i in range(random.randint(5, 15)):
      newCell = Cell(random.randint(5, self.screen_width/self.blockSize-5),random.randint(5, self.screen_height/self.blockSize-5), "C", self.world)
      self.world.addCell(newCell)
      self.world.addPart(newCell.parts[0])
  def run(self):
    running = True
    while running:
      # make it 60 fps
      self.clock.tick(5)

      Game.turn(self.world)

      self.drawBackground()
      self.drawAllCells()
      
      events()

      pygame.display.update()


  def turn(world):
    for cell in world.cells:
      cell.update()


  def drawAllCells(self):
    for cell in self.world.cells:
      self.drawCell(cell)


  def drawCell(self, cell):
    for part in cell.parts:
      if (part.posX < 0 or part.posX >= self.world.width-1 or part.posY < 0 or part.posY >= self.world.height-1):
        part.kill()
      else:
        color = part.cellColor
        pygame.draw.rect(self.screen, color, (self.blockSize*part.posX + 1, self.blockSize*part.posY + 1, self.blockSize - 1, self.blockSize - 1))


  def drawBackground(self):
    # make the background light grey
    self.screen.fill((200, 200, 200))
    # draw a grid using screen width and height
    self.blockSize = 16
    for x in range(self.blockSize, self.screen_width, self.blockSize):
      pygame.draw.line(self.screen, (0, 0, 0), (x, self.blockSize), (x, self.screen_height-self.blockSize))
      for y in range(self.blockSize, self.screen_height, self.blockSize):
        pygame.draw.line(self.screen, (0, 0, 0), (self.blockSize, y), (self.screen_width-self.blockSize, y))
