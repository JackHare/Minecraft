import random
from typing import Optional

# Block size in pixels
BLOCK_SIZE = 64

# Block type constants
AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
COAL = 4
IRON = 5
GOLD = 6
DIAMOND = 7
OAK_LOG = 8
LEAVES = 9

# Ore generation probabilities
ORE_GENERATION_CHANCE = 0.1
COAL_CHANCE = 0.1
IRON_CHANCE = 0.08
GOLD_CHANCE = 0.05
DIAMOND_CHANCE = 0.02

# Depth thresholds for ore generation
COAL_DEPTH = 0.0  # Any depth
IRON_DEPTH = 0.4
GOLD_DEPTH = 0.6
DIAMOND_DEPTH = 0.8


class Block:
    """
    Represents a block in the game world.

    A block is a basic unit in the game world that can be of different types
    (air, grass, dirt, stone, ores, etc.) and has a position in the world.

    Attributes:
        x (float): The x-coordinate of the block in the game world.
        y (float): The y-coordinate of the block in the game world.
        width (int): The width of the block in pixels.
        height (int): The height of the block in pixels.
        block_type (int): The type of the block, determining its appearance and behavior.
    """

    def __init__(self, x: float, y: float, block_type: int) -> None:
        """
        Initialize a new Block.

        Args:
            x: The x-coordinate of the block in the game world.
            y: The y-coordinate of the block in the game world.
            block_type: The type of the block (use block type constants).
        """
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE
        self.height = BLOCK_SIZE
        self.block_type = block_type


def get_block_type(height: int, y: int, chunk_height: int = 256) -> int:
    """
    Determine the block type based on height and depth.

    This function determines what type of block should be generated at a given
    height and depth in the world. It handles terrain generation including
    grass, dirt, stone, and various ores.

    Args:
        height: The surface height at this position.
        y: The y-coordinate to determine the block type for.
        chunk_height: The total height of the chunk (for depth calculation).

    Returns:
        The block type as an integer constant.
    """
    block_type = AIR

    if y > height + 30:
        block_type = STONE
        # Generate ores based on depth and rarity
        if random.random() < ORE_GENERATION_CHANCE:
            depth = y / chunk_height  # Normalized depth between 0 and 1
            if depth > DIAMOND_DEPTH:
                if random.random() < DIAMOND_CHANCE:
                    block_type = DIAMOND
            elif depth > GOLD_DEPTH:
                if random.random() < GOLD_CHANCE:
                    block_type = GOLD
            elif depth > IRON_DEPTH:
                if random.random() < IRON_CHANCE:
                    block_type = IRON
            else:  # Coal layer (shallower)
                if random.random() < COAL_CHANCE:
                    block_type = COAL
    elif y > height + 27:
        block_type = DIRT
    elif y == height + 27:
        block_type = GRASS

    return block_type
