import Block
import SpriteManager
import pygame as pg

CHUNK_WIDTH = 24
CHUNK_HEIGHT = 16

class Chunk():
    def __init__(self):
        self.blocks =[[0 for i in range(CHUNK_WIDTH)] for j in range(CHUNK_HEIGHT)]
        self.generate_chunks()


    def generate_chunks(self):
        for x in range(CHUNK_WIDTH):
            for y in range(CHUNK_HEIGHT):
                block_type = 0
                if y > 6:
                    block_type = 1
                if y > 7:
                    block_type = 2
                self.blocks[y][x] = Block.Block(CHUNK_WIDTH * Block.BLOCK_SIZE, CHUNK_HEIGHT * Block.BLOCK_SIZE, block_type)

    def render_chunk(self, screen):
        for y in range(CHUNK_HEIGHT):
            for x in range(CHUNK_WIDTH):
                block = self.blocks[y][x]
                if block:
                    screen.blit(
                        SpriteManager.load_sprite(block.block_type), (x * Block.BLOCK_SIZE, y * Block.BLOCK_SIZE))
