import random
from typing import Optional, List, Tuple, Dict, Set, Any

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
BEDROCK = -1
OAK_PLANK = 10
COBBLE_STONE = 11
DIAMOND_BLOCK = 12
GOLD_BLOCK = 13
IRON_BLOCK = 14
COAL_BLOCK = 15

# Ore vein size ranges
COAL_VEIN_SIZE = (9, 20)
IRON_VEIN_SIZE = (3, 12)
GOLD_VEIN_SIZE = (3, 12)
DIAMOND_VEIN_SIZE = (1, 9)

# Ore generation probabilities (chance to start a vein)
ORE_GENERATION_CHANCE = 0.01
COAL_CHANCE = 0.4
IRON_CHANCE = 0.3
GOLD_CHANCE = 0.25
DIAMOND_CHANCE = 0.15

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


def get_block_type(height: int, y: int, chunk_height: int = 192) -> int:
    """
    Determine the block type based on height and depth.

    This function determines what type of block should be generated at a given
    height and depth in the world. It handles terrain generation including
    grass, dirt, and stone. Ores are generated separately in veins.

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
    elif y > height + 27:
        block_type = DIRT
    elif y == height + 27:
        block_type = GRASS

    if y == 191:
        block_type = BEDROCK

    return block_type


def generate_ore_vein(chunk: Any, ore_type: int, start_x: int, start_y: int, vein_size: Tuple[int, int], 
                      chunk_height: int) -> None:
    """
    Generate an ore vein starting from the given coordinates.

    This function uses a simple flood-fill algorithm to create a natural-looking
    vein of ore blocks. The vein size is determined by the ore type.

    Args:
        chunk: The chunk to place the ore vein in.
        ore_type: The type of ore to generate.
        start_x: The starting x-coordinate within the chunk.
        start_y: The starting y-coordinate within the chunk.
        vein_size: A tuple containing the min and max size of the vein.
        chunk_height: The height of the chunk for boundary checking.
    """
    from world.Block import Block, STONE  # Import here to avoid circular import
    # Determine vein size - larger veins are rarer
    min_size, max_size = vein_size
    size_range = max_size - min_size
    # Use a weighted random to make larger veins rarer
    size = min_size + int(random.random() ** 2 * size_range)

    # Keep track of blocks that are part of the vein
    vein_blocks = set()
    vein_blocks.add((start_x, start_y))

    # Keep track of potential expansion points
    frontier = [(start_x, start_y)]

    # Directions for expansion (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # Generate the vein
    while len(vein_blocks) < size and frontier:
        # Get a random point from the frontier
        x, y = frontier.pop(random.randint(0, len(frontier) - 1))

        # Place the ore block if it's stone
        if (0 <= x < len(chunk.blocks[0]) and 0 <= y < chunk_height and 
                isinstance(chunk.blocks[y][x], Block) and 
                chunk.blocks[y][x].block_type == STONE):
            # Replace stone with ore
            chunk.blocks[y][x].block_type = ore_type

            # Add neighboring blocks to the frontier
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in vein_blocks and (nx, ny) not in frontier:
                    # Higher chance to expand to adjacent blocks than diagonal ones
                    if dx == 0 or dy == 0:
                        if random.random() < 0.7:  # 70% chance for adjacent
                            frontier.append((nx, ny))
                            vein_blocks.add((nx, ny))
                    else:
                        if random.random() < 0.3:  # 30% chance for diagonal
                            frontier.append((nx, ny))
                            vein_blocks.add((nx, ny))


def place_ore_veins(chunk: Any, chunk_height: int) -> None:
    """
    Place ore veins throughout the chunk.

    This function attempts to place ore veins throughout the chunk based on
    depth and probability settings.

    Args:
        chunk: The chunk to place ore veins in.
        chunk_height: The height of the chunk.
    """
    from world.Block import Block, STONE  # Import here to avoid circular import
    # Try to place ore veins
    for x in range(len(chunk.blocks[0])):
        for y in range(chunk_height):
            # Only consider stone blocks
            if not isinstance(chunk.blocks[y][x], Block) or chunk.blocks[y][x].block_type != STONE:
                continue

            # Check if we should start an ore vein
            if random.random() < ORE_GENERATION_CHANCE:
                # Determine ore type based on depth
                depth = y / chunk_height  # Normalized depth between 0 and 1
                ore_type = None
                vein_size = None

                # Use weighted random selection based on depth
                r = random.random()

                if depth > DIAMOND_DEPTH and r < DIAMOND_CHANCE:
                    ore_type = DIAMOND
                    vein_size = DIAMOND_VEIN_SIZE
                elif depth > GOLD_DEPTH and r < DIAMOND_CHANCE + GOLD_CHANCE:
                    ore_type = GOLD
                    vein_size = GOLD_VEIN_SIZE
                elif depth > IRON_DEPTH and r < DIAMOND_CHANCE + GOLD_CHANCE + IRON_CHANCE:
                    ore_type = IRON
                    vein_size = IRON_VEIN_SIZE
                else:  # Coal layer (shallower)
                    ore_type = COAL
                    vein_size = COAL_VEIN_SIZE

                if ore_type and vein_size:
                    generate_ore_vein(chunk, ore_type, x, y, vein_size, chunk_height)
