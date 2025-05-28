import random
import math
from typing import List, Union, Any, Optional
import pygame as pg

from world.Block import Block, BLOCK_SIZE, AIR, OAK_LOG, LEAVES, POPPY, PUMPKIN, WATER, GRASS, DIRT, STONE
from rendering import SpriteManager

# Number of blocks per chunk
CHUNK_WIDTH = 64
CHUNK_HEIGHT = 192

# Tree generation constants
TREE_CHANCE = 0.2
POPPY_CHANCE = 0.03
PUMPKIN_CHANCE = 0.03
MIN_TREE_TRUNK_HEIGHT = 4
MAX_TREE_TRUNK_HEIGHT = 6

# Pond generation constants
POND_CHANCE = 0.05  # 5% chance to generate a pond
POND_MIN_SIZE = 3
POND_MAX_SIZE = 8


class Chunk:
    """
    Represents a chunk of the game world.

    A chunk is a section of the game world that contains a grid of blocks.
    The world is divided into chunks to make rendering and memory management more efficient.

    Attributes:
        blocks (List[List[Block]]): 2D grid of blocks in the chunk.
        position (int): The horizontal position of the chunk in the world.
        offset (int): The pixel offset of the chunk from the world origin.
    """

    def __init__(self, position: int) -> None:
        """
        Initialize a new Chunk.

        Args:
            position: The horizontal position of the chunk in the world.
        """
        self.blocks: List[List[Block]] = [[0 for i in range(CHUNK_WIDTH)] for j in range(CHUNK_HEIGHT)]
        self.position = position
        self.offset = position * (CHUNK_WIDTH * BLOCK_SIZE)
        self.generate_chunks()

    def generate_chunks(self) -> None:
        """
        Generate the terrain in the chunk.

        This method creates the terrain by setting block types based on height
        and adds features like ore veins and trees.
        """
        # First pass: Generate basic terrain (stone, dirt, grass, bedrock)
        for x in range(CHUNK_WIDTH):
            # Generate terrain height using smoother noise
            height = int(8 + math.sin((x + self.position * CHUNK_WIDTH) * 0.3) * 2 + random.uniform(-0.5, 0.5))

            for y in range(CHUNK_HEIGHT):
                # Import here to avoid circular import
                from world.Block import get_block_type
                block_type = get_block_type(height, y, CHUNK_HEIGHT)

                self.blocks[y][x] = Block(x * BLOCK_SIZE + self.offset, y * BLOCK_SIZE, block_type)

        # Second pass: Generate ore veins
        from world.Block import place_ore_veins
        place_ore_veins(self, CHUNK_HEIGHT)

        # Third pass: Generate trees
        for x in range(CHUNK_WIDTH):
            # Get the height at this x-coordinate
            height = int(8 + math.sin((x + self.position * CHUNK_WIDTH) * 0.3) * 2 + random.uniform(-0.5, 0.5))

            # Generate trees after terrain generation
            if x > 2 and x < CHUNK_WIDTH - 3 and random.random() < TREE_CHANCE:
                self.place_tree(x, height + 27)
                continue

            if random.random() < POPPY_CHANCE:
                self.place_poppy(x, height + 27)
                continue

            if random.random() < PUMPKIN_CHANCE:
                self.place_pumpkin(x, height + 27)
                continue

            # Generate ponds occasionally
            if random.random() < POND_CHANCE and x > POND_MAX_SIZE and x < CHUNK_WIDTH - POND_MAX_SIZE:
                # Place pond at grass level
                self.generate_pond(x, height + 26)
                continue

    def place_tree(self, x: int, y: int) -> None:
        """
        Place a tree at the specified coordinates.

        Args:
            x: The x-coordinate within the chunk.
            y: The y-coordinate (height) at which to place the tree.
        """
        # Check boundaries
        if y - 7 < 0 or x < 2 or x > CHUNK_WIDTH - 3:
            return

        # Place trunk
        trunk_height = random.randint(MIN_TREE_TRUNK_HEIGHT, MAX_TREE_TRUNK_HEIGHT)
        for i in range(1, trunk_height + 1):
            if y - i >= 0:
                self.blocks[y - i][x] = Block(
                    x * BLOCK_SIZE + self.offset,
                    (y - i) * BLOCK_SIZE,
                    OAK_LOG
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
                                  (isinstance(current_block, Block) and
                                   current_block.block_type in [AIR, LEAVES]))

                # Place leaf if valid position and within desired shape
                if can_place_leaf and abs(leaf_x - x) + abs(leaf_y - leaf_start) < 4 :
                    self.blocks[leaf_y][leaf_x] = Block(
                        leaf_x * BLOCK_SIZE + self.offset,
                        leaf_y * BLOCK_SIZE,
                        LEAVES
                    )

    def render_chunk(self, screen: pg.Surface, camera: Any) -> None:
        """
        Render the chunk to the screen.

        This method draws all visible blocks in the chunk to the screen,
        taking into account the camera position for scrolling.

        Args:
            screen: The pygame surface to render to.
            camera: The camera object that determines the view position.
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Only render blocks that are visible on screen
        for y in range(CHUNK_HEIGHT):
            block_y = y * BLOCK_SIZE - camera.y
            if block_y < -BLOCK_SIZE or block_y > screen_height:
                continue

            for x in range(CHUNK_WIDTH):
                block_x = x * BLOCK_SIZE + self.offset - camera.x
                if block_x < -BLOCK_SIZE or block_x > screen_width:
                    continue

                block_type = self.blocks[y][x].block_type
                if block_type != AIR:  # Only render if it's not an air block
                    screen.blit(
                        SpriteManager.get_block_sprite(block_type),
                        (block_x, block_y),
                    )

    def place_poppy(self, x: int, y: int):
        self.blocks[y][x] = Block(x * BLOCK_SIZE + self.offset, y * BLOCK_SIZE, POPPY)

    def place_pumpkin(self, x, y):
        self.blocks[y][x] = Block(x * BLOCK_SIZE + self.offset, y * BLOCK_SIZE, PUMPKIN)

    def generate_pond(self, center_x: int, center_y: int) -> None:
        """
        Generate a small pond of water at the specified coordinates.

        Args:
            center_x: The x-coordinate of the center of the pond.
            center_y: The y-coordinate of the center of the pond.
        """
        # Determine pond size
        pond_size = random.randint(POND_MIN_SIZE, POND_MAX_SIZE)

        # Keep track of blocks that are part of the pond
        pond_blocks = set()

        # Start with the center block
        pond_blocks.add((center_x, center_y))

        # Keep track of potential expansion points
        frontier = [(center_x, center_y)]

        # Directions for expansion (including diagonals)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        # Generate the pond
        while len(pond_blocks) < pond_size and frontier:
            # Get a random point from the frontier
            x, y = frontier.pop(random.randint(0, len(frontier) - 1))

            # Check if we can place water here (must be above stone level)
            if (0 <= x < CHUNK_WIDTH and 0 <= y < CHUNK_HEIGHT and 
                    isinstance(self.blocks[y][x], Block) and 
                    self.blocks[y][x].block_type in [GRASS, DIRT]):
                # Replace block with water
                self.blocks[y][x] = Block(
                    x * BLOCK_SIZE + self.offset,
                    y * BLOCK_SIZE,
                    WATER
                )

                # Add neighboring blocks to the frontier
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in pond_blocks and (nx, ny) not in frontier:
                        # Higher chance to expand to adjacent blocks than diagonal ones
                        if dx == 0 or dy == 0:
                            if random.random() < 0.7:  # 70% chance for adjacent
                                frontier.append((nx, ny))
                                pond_blocks.add((nx, ny))
                        else:
                            if random.random() < 0.3:  # 30% chance for diagonal
                                frontier.append((nx, ny))
                                pond_blocks.add((nx, ny))


def calculate_player_position(player: Any) -> int:
    """
    Calculate the chunk position that the player is in.

    Args:
        player: The player object with x-coordinate attribute.

    Returns:
        The horizontal chunk position of the player.
    """
    return int(math.floor(player.x / (CHUNK_WIDTH * BLOCK_SIZE)))
