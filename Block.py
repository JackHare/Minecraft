import pygame
import SpriteManager

BLOCK_SIZE = 64

class Block():
    def __init__(self, x, y, block_type):

        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.block_type = block_type

        self.image = SpriteManager.load_sprite(block_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.width
        self.height = self.height
        #self.rect = pygame.Rect(x, y, self.width, self.height)