import pygame as pg
import Block
import SpriteManager

background_colour = (100,200,255)
(width, height) = (1280, 720)
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Minecraft2d")
screen.fill(background_colour)

block = Block.Block(0, 0, 1)

screen.blit(SpriteManager.load_sprite(block.block_type), block.rect)
pg.display.flip()



running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

