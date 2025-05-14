import pygame as pg

from Game import Game

game = Game()

running = True
while running:
  game.update()

  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

    if event.type == pg.KEYDOWN:
      if event.key == pg.K_UP:
        game.keyboard.up = True
      if event.key == pg.K_DOWN:
        game.keyboard.down = True
      if event.key == pg.K_LEFT:
        game.keyboard.left = True
      if event.key == pg.K_RIGHT:
        game.keyboard.right = True
      if event.key == pg.K_w:
        game.keyboard.w = True
      if event.key == pg.K_a:
        game.keyboard.a = True
      if event.key == pg.K_s:
        game.keyboard.s = True
      if event.key == pg.K_d:
        game.keyboard.d = True

    if event.type == pg.KEYUP:
      if event.key == pg.K_UP:
        game.keyboard.up = False
      if event.key == pg.K_DOWN:
        game.keyboard.down = False
      if event.key == pg.K_LEFT:
        game.keyboard.left = False
      if event.key == pg.K_RIGHT:
        game.keyboard.right = False
      if event.key == pg.K_w:
        game.keyboard.w = False
      if event.key == pg.K_a:
        game.keyboard.a = False
      if event.key == pg.K_s:
        game.keyboard.s = False
      if event.key == pg.K_d:
        game.keyboard.d = False


