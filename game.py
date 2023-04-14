import pygame
from world import World
from cell import Cell
import random
from pygame._sdl2 import Window

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
    
    monitor = "LEFT" # LEFT MIDDLE RIGHT
    COVER_TASKBAR = False
    
    buffer = 0
    if not COVER_TASKBAR:
      buffer += 40
    if monitor == "MIDDLE" or monitor == "RIGHT":
      self.screen_width = pygame.display.Info().current_w
      self.screen_height = pygame.display.Info().current_h-buffer
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
      pgwindow = Window.from_display_module() # call this after set_mode

    if monitor == "RIGHT":
      pgwindow.position = (1920,0)

    if monitor == "MIDDLE":
      pgwindow.position = (0,0)

    if monitor == "LEFT":
      self.screen_width = pygame.display.Info().current_h
      self.screen_height = pygame.display.Info().current_w-buffer
      self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
      pgwindow = Window.from_display_module() #call this after set_mode
      pgwindow.position = (-1080,-1*(1920-1080) + 104)
    
    print("Screen width:", self.screen_width, "Screen height:", self.screen_height)

    self.clock = pygame.time.Clock()

    self.setupWorld()


  def run(self):
    running = True
    self.currentTickRate = 5
    while running:
      # reset world when R is pressed
      if pygame.key.get_pressed()[pygame.K_r]:
        self.setupWorld()
      
      # fps change on pressing the up and down arrow keys
      if pygame.key.get_pressed()[pygame.K_UP]:
        self.currentTickRate += 1
        print("Tickrate:", self.currentTickRate)
      if pygame.key.get_pressed()[pygame.K_DOWN]:
        self.currentTickRate -= 1
        print("Tickrate:", self.currentTickRate)
      if self.currentTickRate < 1:
        self.currentTickRate = 1
        print("Tickrate:", self.currentTickRate)
      self.clock.tick(self.currentTickRate)

      Game.turn(self.world)

      self.drawBackground()
      self.drawAllCells()
      if (len(self.world.cells) == 0):
        self.setupWorld()
      
      events()

      pygame.display.update()


  def setupWorld(self):
    # create world
    self.blockSize = 10
    self.world = World(self.screen_width/self.blockSize, self.screen_height/self.blockSize)
    for i in range(random.randint(5, 15)):
      newCell = Cell(random.randint(5, self.screen_width/self.blockSize-5),random.randint(5, self.screen_height/self.blockSize-5), "C", self.world)
      self.world.addCell(newCell)

  def turn(world):
    for cell in world.cells:
      cell.update()


  def drawAllCells(self):
    PRINT_STUFF = False
    totalParts = 0
    totalEnergy = 0
    for cell in self.world.cells:
      self.drawCell(cell)
      totalParts += len(cell.parts)
      totalEnergy += cell.energy
    
    if PRINT_STUFF:
      print()
      print("Cells:", len(self.world.cells))
      if len(self.world.cells) != 0:
        print("Cell parts:", totalParts, "Average of", round(totalParts/len(self.world.cells),2), "parts per cell")
        print("Cell parts take up ", str(round(totalParts/(self.world.width*self.world.height)*100,2)) + "% of the", self.world.width*self.world.height, "blocks")
        print("Average of", round(totalEnergy/len(self.world.cells),2), "energy per cell")


  def drawCell(self, cell):
    for part in cell.parts:
      if (part.posX < 0 or part.posX >= self.world.width-1 or part.posY < 0 or part.posY >= self.world.height-1):
        part.kill()
      else:
        color = part.cellColor
        pygame.draw.rect(self.screen, color, (self.blockSize*part.posX + 1, self.blockSize*part.posY + 1, self.blockSize - 1, self.blockSize - 1))


  def drawBackground(self):
    self.screen.fill((50, 50, 50)) # background
    # draw a grid using screen width and height
    for x in range(self.blockSize, self.screen_width, self.blockSize):
      pygame.draw.line(self.screen, (100, 100, 100), (x, self.blockSize), (x, self.screen_height-self.blockSize))
      for y in range(self.blockSize, self.screen_height, self.blockSize):
        pygame.draw.line(self.screen, (100, 100, 100), (self.blockSize, y), (self.screen_width-self.blockSize, y))
