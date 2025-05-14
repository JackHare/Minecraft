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

      #  self.image = SpriteManager.load_block_sprite(block_type).convert()
       # self.image = pygame.transform.scale(self.image, (self.width, self.height))

        #self.rect = self.image.get_rect()
       # self.rect.x = x
       # self.rect.y = y
        #self.rect.width = self.width;
        #self.rect.height = self.width;
