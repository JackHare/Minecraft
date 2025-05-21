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
            # Generate terrain height using smoother noise
            height = int(8 + math.sin((x + self.position * CHUNK_WIDTH) * 0.3) * 2 + random.uniform(-0.5, 0.5))

            for y in range(CHUNK_HEIGHT):
                # Generate air block by default
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

                self.blocks[y][x] = Block.Block(x * Block.BLOCK_SIZE + self.offset, y * Block.BLOCK_SIZE, block_type)

            # Generate trees after terrain generation
            if x > 2 and x < CHUNK_WIDTH - 3 and random.random() < 0.1:
                self.place_tree(x, height)

    def place_tree(self, x, y):

        if y - 7 < 0 or x < 2 or x > CHUNK_WIDTH - 3:
            return

        # Tree trunk
        trunk_height = random.randint(4, 6)
        for i in range(1, trunk_height + 1):
            if y - i >= 0:  # y-i is the y-coordinate of the trunk block
                self.blocks[y - i][x] = Block.Block(x * Block.BLOCK_SIZE + self.offset, (y - i) * Block.BLOCK_SIZE,
                                                    8)  # 8 is trunk

        leaf_start = y - trunk_height - 2

        for leaf_y in range(leaf_start - 2, leaf_start + 2):
            width = min(2, 3 - abs(leaf_y - (leaf_start)))
            for leaf_x in range(x - width, x + width + 1):
                if not (0 <= leaf_y < CHUNK_HEIGHT and 0 <= leaf_x < CHUNK_WIDTH):
                    continue


                current_block_val = self.blocks[leaf_y][leaf_x]
                can_place_leaf = False
                if current_block_val == 0:
                    can_place_leaf = True
                elif isinstance(current_block_val, Block.Block):
                    if current_block_val.block_type == 0 or current_block_val.block_type == 9:
                        can_place_leaf = True

                if can_place_leaf:
                    if abs(leaf_x - x) + abs(leaf_y - leaf_start) < 4:  # Your shape refinement
                        self.blocks[leaf_y][leaf_x] = Block.Block(
                            leaf_x * Block.BLOCK_SIZE + self.offset,
                            leaf_y * Block.BLOCK_SIZE,
                            9  # Leaf block type
                        )
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