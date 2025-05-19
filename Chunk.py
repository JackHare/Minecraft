import Block
import SpriteManager
import pygame as pg
import random
import math

# Number of blocks per chunk
CHUNK_WIDTH = 64
CHUNK_HEIGHT = 128

class Chunk():
    def __init__(self, position):
        self.blocks = [[0 for i in range(CHUNK_WIDTH)] for j in range(CHUNK_HEIGHT)]
        self.position = position
        self.offset = position * (CHUNK_WIDTH * Block.BLOCK_SIZE)
        self.generate_chunks()



    # Generates the terrain in a chunk
    def generate_chunks(self):
        for x in range(CHUNK_WIDTH):

            #height = int(8 + math.sin(x * 0.5) * 2 + random.randint(-1, 1))
            height = int(8 + math.sin(x * 0.3) * 1 + random.uniform(-0.5, 0.5))

            for y in range(CHUNK_HEIGHT):
                # Generate air block by default
                block_type = 0

                if y > height + 3:
                    block_type = 3
                elif y > height:
                    block_type = 2
                elif y == height:
                    block_type = 1

                self.blocks[y][x] = Block.Block(x * Block.BLOCK_SIZE + self.offset, y * Block.BLOCK_SIZE, block_type)

    # Render a chunk to screen
    def render_chunk(self, screen, camera):
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        for y in range(CHUNK_HEIGHT):
            block_y = y * Block.BLOCK_SIZE - camera.y
            if block_y < -Block.BLOCK_SIZE or block_y > screen_height:
                continue

            for x in range(CHUNK_WIDTH):
                block_x = x * Block.BLOCK_SIZE + self.offset - camera.x
                if block_x < -Block.BLOCK_SIZE or block_x > screen_width:
                    continue

                block_type = self.blocks[y][x].block_type
                if block_type != 0:  # Only render if it's not an air block (type 0)
                    screen.blit(
                        SpriteManager.get_block_sprite(block_type),
                        (block_x, block_y),
                    )

# Calculates what "position" the player is in, using the same system as chunk.position
def calculate_player_position(player):
    return int(math.floor(player.x / (CHUNK_WIDTH * Block.BLOCK_SIZE)))