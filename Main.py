import pygame as pg
import pygame.display

import Block
import Chunk
import SpriteManager

background_colour = (100,200,255)
(width, height) = (24 * Block.BLOCK_SIZE, 16 * Block.BLOCK_SIZE)
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Minecraft2d")
screen.fill(background_colour)

block = Block.Block(10, 0, 1)


c = Chunk.Chunk()

c.render_chunk(screen)

pg.display.flip()

running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

