from world import Block
from rendering import SpriteManager
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
                block_type = Block.get_block_type(height, y)

                self.blocks[y][x] = Block.Block(x * Block.BLOCK_SIZE + self.offset, y * Block.BLOCK_SIZE, block_type)

            # Generate trees after terrain generation
            if x > 2 and x < CHUNK_WIDTH - 3 and random.random() < 0.2:
                self.place_tree(x, height)

    def place_tree(self, x, y):
        # Check boundaries
        if y - 7 < 0 or x < 2 or x > CHUNK_WIDTH - 3:
            return

        # Place trunk
        trunk_height = random.randint(4, 6)
        for i in range(1, trunk_height + 1):
            if y - i >= 0:
                self.blocks[y - i][x] = Block.Block(
                    x * Block.BLOCK_SIZE + self.offset,
                    (y - i) * Block.BLOCK_SIZE,
                    8  # Trunk block type
                )

        # Place leaves
        leaf_start = y - trunk_height - 2
        for leaf_y in range(leaf_start - 2, leaf_start + 2):
            width = min(2, 3 - abs(leaf_y - leaf_start))
            for leaf_x in range(x - width, x + width + 1):
                # Check boundaries
                if not (0 <= leaf_y < CHUNK_HEIGHT and 0 <= leaf_x < CHUNK_WIDTH):
                    continue

                # Check if we can place a leaf here
                current_block = self.blocks[leaf_y][leaf_x]
                can_place_leaf = (current_block == 0 or
                                  (isinstance(current_block, Block.Block) and
                                   current_block.block_type in [0, 9]))

                # Place leaf if valid position and within desired shape
                if can_place_leaf and abs(leaf_x - x) + abs(leaf_y - leaf_start) < 4:
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