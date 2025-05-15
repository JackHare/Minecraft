import Block
import SpriteManager
from Entity import Entity
import pygame as pg

from Hitbox import Hitbox


class Player(Hitbox):
    def __init__(self):
        super().__init__(0, 0, Block.BLOCK_SIZE * .6, Block.BLOCK_SIZE *1.8, "Player")
        self.image_copy = self.image.copy()
        self.facingLeft = True

    def render(self, screen, camera):
        self.rect.x = self.x - camera.x
        self.rect.y = self.y - camera.y
        if self.facingLeft:
            self.image = pg.transform.flip(self.image_copy, True, False)
            self.image.set_colorkey((0, 0, 0))

        screen.blit(self.image, self.rect)

