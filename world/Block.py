from world.Chunk import CHUNK_HEIGHT

BLOCK_SIZE = 64
import random


class Block():
    def __init__(self, x, y, block_type):
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.block_type = block_type



def get_block_type(height, y):
    block_type = 0

    if y > height + 3:
        block_type = 3
        # Generate ores based on depth and rarity
        if random.random() < 0.1:  # 10% chance for ore generation
            depth = y / CHUNK_HEIGHT  # Normalized depth between 0 and 1
            if depth > 0.8:  # Diamond layer (deeper)
                if random.random() < 0.02:
                    block_type = 7
            elif depth > 0.6:  # Gold layer
                if random.random() < 0.05:
                    block_type = 6
            elif depth > 0.4:  # Iron layer
                if random.random() < 0.08:
                    block_type = 5
            else:  # Coal layer (shallower)
                if random.random() < 0.1:
                    block_type = 4
    elif y > height:
        block_type = 2  # Dirt
    elif y == height:
        block_type = 1  # Grass

    return block_type


