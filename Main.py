import pygame as pg
import Block
import SpriteManager

background_colour = (100,200,255)
(width, height) = (1280, 720)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minecraft2d")
screen.fill(background_colour)
pygame.display.flip()


running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

