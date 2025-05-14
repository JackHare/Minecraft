import Block
import SpriteManager
import pygame as pg
import random
import math

# Number of blocks per chunk
CHUNK_WIDTH = 24
CHUNK_HEIGHT = 16

class Chunk():
    def __init__(self):
        self.blocks =[[0 for i in range(CHUNK_WIDTH)] for j in range(CHUNK_HEIGHT)]
        self.generate_chunks()


    # Generates the terrain in a chunk
    def generate_chunks(self):
        for x in range(CHUNK_WIDTH):

            height = int(8 + math.sin(x * 0.5) * 2 + random.randint(-1, 1))

            for y in range(CHUNK_HEIGHT):
                # Generate air block by default
                block_type = 0

                if y > height + 3:
                    block_type = 3
                elif y > height:
                    block_type = 2
                elif y == height:
                    block_type = 1

                self.blocks[y][x] = Block.Block(CHUNK_WIDTH * Block.BLOCK_SIZE, CHUNK_HEIGHT * Block.BLOCK_SIZE, block_type)

    # Render a chunk to screen
    def render_chunk(self, screen, camera):
        for y in range(CHUNK_HEIGHT):
            for x in range(CHUNK_WIDTH):
                block = self.blocks[y][x]
                if block:
                   # screen.blit(
                       # SpriteManager.load_sprite(block.block_type), (x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))
                    screen.blit(SpriteManager.load_block_sprite(block.block_type), (x * Block.BLOCK_SIZE - camera.x, y * Block.BLOCK_SIZE - camera.y))