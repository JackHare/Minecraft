"""
Hitbox module for collision detection and physics.

This module provides the Hitbox class for handling collision detection
and physics interactions between entities and the game world.
"""
import math
from typing import List, Any, Optional, Tuple

from world.Block import BLOCK_SIZE, AIR, OAK_LOG, LEAVES
from world.Chunk import CHUNK_WIDTH, CHUNK_HEIGHT, calculate_player_position
from entity.Entity import Entity

# Physics constants
GRAVITY = 9.8  # m/s^2, adjust as needed for your game's scale


class Hitbox(Entity):
    """
    Represents a physical entity with collision detection.

    This class extends Entity to add physics properties and collision detection.
    It handles movement and interactions with the game world.

    Attributes:
        chunk_x (int): The x-coordinate within the current chunk.
        chunk_y (int): The y-coordinate within the current chunk.
        x_change (float): The target x-coordinate for movement.
        y_change (float): The target y-coordinate for movement.
        mass (float): The mass of the entity for physics calculations.
        friction_coefficient (float): The friction coefficient for physics calculations.
        grounded (bool): Whether the entity is on the ground.
    """

    def __init__(self, x: float, y: float, width: int, height: int, type: str, 
                 mass: float = 1.0, friction_coefficient: float = 0.5) -> None:
        """
        Initialize a new Hitbox entity.

        Args:
            x: The x-coordinate of the entity.
            y: The y-coordinate of the entity.
            width: The width of the entity in pixels.
            height: The height of the entity in pixels.
            type: The type of the entity.
            mass: The mass of the entity for physics calculations.
            friction_coefficient: The friction coefficient for physics calculations.
        """
        super().__init__(x, y, width, height, type)
        self.chunk_x: Optional[int] = None
        self.chunk_y: Optional[int] = None
        self.x_change = x  # Initialize to current position
        self.y_change = y  # Initialize to current position
        self.mass = mass
        self.friction_coefficient = friction_coefficient
        self.grounded = True

    def update_player_position(self, chunk_list: List[Any]) -> None:
        """
        Update the entity's position based on physics and collisions.

        This method calculates the entity's new position, checks for collisions
        with blocks in the world, and resolves those collisions.

        Args:
            chunk_list: The list of chunks to check for collisions.
        """
        # Calculate chunk coordinates
        absolute_x = self.x
        self.chunk_x = math.floor((absolute_x % (CHUNK_WIDTH * BLOCK_SIZE)) / BLOCK_SIZE)
        self.chunk_y = math.floor(self.y / BLOCK_SIZE)

        # Get the current chunk number
        chunk_number = calculate_player_position(self)

        # Determine which chunks to check based on position
        chunks_to_check = self._get_chunks_to_check(chunk_list)

        # Find colliding blocks
        block_list = self._find_colliding_blocks(chunks_to_check)

        # Resolve collisions
        self._resolve_collisions(block_list)

        # Update position
        self.x = self.x_change
        self.y = self.y_change

    def _get_chunks_to_check(self, chunk_list: List[Any]) -> Tuple[Any, Any, Any]:
        """
        Determine which chunks to check for collisions.

        Args:
            chunk_list: The list of chunks.

        Returns:
            A tuple containing the left, center, and right chunks to check.
        """
        # Calculate if we are on the left or right edge of a chunk
        on_left_edge = self.chunk_x % CHUNK_WIDTH == 0
        on_right_edge = self.chunk_x % CHUNK_WIDTH == CHUNK_WIDTH - 1

        # Default to center chunk for all positions
        left_chunk = center_chunk = right_chunk = chunk_list[1]

        # Adjust chunks if on edges
        if on_left_edge:
            left_chunk = chunk_list[0]

        if on_right_edge:
            right_chunk = chunk_list[2]

        return left_chunk, center_chunk, right_chunk

    def _find_colliding_blocks(self, chunks: Tuple[Any, Any, Any]) -> List[Any]:
        """
        Find blocks that the entity is colliding with.

        Args:
            chunks: A tuple containing the left, center, and right chunks to check.

        Returns:
            A list of blocks that the entity is colliding with.
        """
        left_chunk, center_chunk, right_chunk = chunks
        block_list = []

        # Check blocks in a 5x6 area around the player (optimized search area)
        for dy in range(-2, 4):
            for dx in range(-2, 3):
                check_x = self.chunk_x + dx
                check_y = self.chunk_y + dy

                # Determine which chunk to check based on position
                current_chunk = center_chunk
                if check_x < 0:
                    if left_chunk:
                        check_x = CHUNK_WIDTH + check_x
                        current_chunk = left_chunk
                elif check_x >= CHUNK_WIDTH:
                    if right_chunk:
                        check_x = check_x - CHUNK_WIDTH
                        current_chunk = right_chunk
                    else:
                        continue

                # Skip if out of bounds
                if not (0 <= check_x < CHUNK_WIDTH and 0 <= check_y < CHUNK_HEIGHT):
                    continue

                # Get the block and check if it's solid
                block = current_chunk.blocks[check_y][check_x]
                if block is None or block.block_type in (AIR, OAK_LOG, LEAVES):
                    continue

                # Adjust block's absolute position based on chunk
                block.x = (current_chunk.position * CHUNK_WIDTH * BLOCK_SIZE) + (check_x * BLOCK_SIZE)

                # Check for collision
                if self.check_collision(block, self.x_change, self.y_change):
                    block_list.append(block)

        return block_list

    def _resolve_collisions(self, block_list: List[Any]) -> None:
        """
        Resolve collisions with blocks.

        Args:
            block_list: A list of blocks that the entity is colliding with.
        """
        for block in block_list:
            # Calculate overlap in x and y axes
            x_overlap = min(self.x + self.width, block.x + block.width) - max(self.x, block.x)
            y_overlap = min(self.y + self.height, block.y + block.height) - max(self.y, block.y)

            # Determine collision side and adjust position
            if x_overlap < y_overlap:
                if self.x < block.x:  # Collision on the left
                    self.x_change = block.x - self.width
                else:  # Collision on the right
                    self.x_change = block.x + block.width
            else:
                if self.y < block.y:  # Collision from above
                    self.y_change = block.y - self.height
                    self.grounded = True
                else:  # Collision from below
                    self.y_change = block.y + block.height

    def check_collision(self, block: Any, x: float, y: float) -> bool:
        """
        Check if the entity collides with a block at the given position.

        Args:
            block: The block to check collision with.
            x: The x-coordinate to check collision at.
            y: The y-coordinate to check collision at.

        Returns:
            True if the entity collides with the block, False otherwise.
        """
        # Check if rectangles overlap in both x and y axes (AABB collision)
        return (x < block.x + block.width and
                x + self.width > block.x and
                y < block.y + block.height and
                y + self.height > block.y)
