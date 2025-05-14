import pygame as pg

import SpriteManager


class Entity:
    def __init__(self, x, y, width, height, type):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.type = type
        self.image = SpriteManager.load_entity_sprite(type)
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.rect.width = self.width
        self.rect.height = self.width

    def render(self, screen, camera):
        self.rect.x = self.x - camera.x
        self.rect.y = self.y - camera.y
        screen.blit(self.image, self.rect)
