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

