"""
Water simulation module for the game.

This module provides the WaterSimulation class for handling
water flow behavior in the game world.
"""
import random
from typing import List, Any, Optional, Tuple, Set

from world.Block import Block, AIR, WATER, BLOCK_SIZE, OAK_LOG, POPPY
from world.Chunk import CHUNK_WIDTH, CHUNK_HEIGHT

class WaterSimulation:
    """
    Handles water flow behavior in the game world.

    This class provides methods for simulating water flow, including
    downward and sideways movement, settling, and optional evaporation.

    Attributes:
        MAX_WATER_LEVEL (int): The maximum level of water (for partial blocks).
        FLOW_RATE (int): The rate at which water flows (blocks per update).
        EVAPORATION_CHANCE (float): The chance of water evaporating when isolated.
        ENABLE_EVAPORATION (bool): Whether water can evaporate.
        MAX_SPREAD_DISTANCE (int): The maximum distance water can spread from its source.
    """

    # Water simulation constants
    MAX_WATER_LEVEL = 8  # Water levels from 1 (minimal) to 8 (full block)
    FLOW_RATE = 1  # How many blocks water can flow per update
    EVAPORATION_CHANCE = 0.05  # 5% chance of evaporation when isolated
    ENABLE_EVAPORATION = True  # Whether water can evaporate
    MAX_SPREAD_DISTANCE = 7  # Maximum distance water can spread from source


    @staticmethod
    def update_water(chunk_list: List[Any]) -> None:
        """
        Update all water blocks in the chunks.

        This method iterates through all chunks and updates water blocks
        according to the water flow rules.

        Args:
            chunk_list: The list of chunks to update.
        """
        # Keep track of blocks that have been updated this frame
        updated_blocks = set()

        # Process each chunk
        for chunk in chunk_list:
            WaterSimulation._update_chunk_water(chunk, chunk_list, updated_blocks)

    @staticmethod
    def _update_chunk_water(chunk: Any, chunk_list: List[Any], updated_blocks: Set[Tuple[int, int, int]]) -> None:
        """
        Update water blocks in a single chunk.

        Args:
            chunk: The chunk to update.
            chunk_list: The list of all chunks (for cross-chunk flow).
            updated_blocks: Set of blocks that have been updated this frame.
        """
        # Process water blocks from bottom to top, left to right
        # This ensures water flows downward first
        for y in range(CHUNK_HEIGHT - 1, -1, -1):
            for x in range(CHUNK_WIDTH):
                block = chunk.blocks[y][x]

                # Skip if not a water block or already updated
                if not isinstance(block, Block) or block.block_type != WATER:
                    continue

                # Create a unique identifier for this block
                block_id = (chunk.position, x, y)
                if block_id in updated_blocks:
                    continue

                # Mark this block as updated
                updated_blocks.add(block_id)

                # Try to flow downward first
                if WaterSimulation._flow_downward(chunk, x, y, chunk_list, updated_blocks):
                    continue

                # If can't flow downward, try to flow sideways
                WaterSimulation._flow_sideways(chunk, x, y, chunk_list, updated_blocks)



    @staticmethod
    def _flow_downward(chunk: Any, x: int, y: int, chunk_list: List[Any], 
                       updated_blocks: Set[Tuple[int, int, int]]) -> bool:
        """
        Try to flow water downward.

        Args:
            chunk: The chunk containing the water block.
            x: The x-coordinate of the water block within the chunk.
            y: The y-coordinate of the water block within the chunk.
            chunk_list: The list of all chunks.
            updated_blocks: Set of blocks that have been updated this frame.

        Returns:
            True if water flowed downward, False otherwise.
        """
        # Check if we're at the bottom of the chunk
        if y >= CHUNK_HEIGHT - 1:
            return False

        # Get the current water block and its distance from source
        current_block = chunk.blocks[y][x]
        current_distance = current_block.water_distance

        # Check if we've reached the maximum spread distance



        # Get the block below
        block_below = chunk.blocks[y + 1][x]

        # If the block below is air, replace it with water
        if isinstance(block_below, Block) and (block_below.block_type == AIR or block_below.block_type == POPPY):
            # Create a new water block with increased distance
            chunk.blocks[y + 1][x] = Block(
                x * BLOCK_SIZE + chunk.offset,
                (y + 1) * BLOCK_SIZE,
                WATER,
                current_distance + 1  # Increment distance from source
            )

            # Mark the new water block as updated
            updated_blocks.add((chunk.position, x, y + 1))
            return True

        return False

    @staticmethod
    def _flow_sideways(chunk: Any, x: int, y: int, chunk_list: List[Any], 
                       updated_blocks: Set[Tuple[int, int, int]]) -> None:
        """
        Try to flow water sideways.

        Args:
            chunk: The chunk containing the water block.
            x: The x-coordinate of the water block within the chunk.
            y: The y-coordinate of the water block within the chunk.
            chunk_list: The list of all chunks.
            updated_blocks: Set of blocks that have been updated this frame.
        """
        # Get the current water block and its distance from source
        current_block = chunk.blocks[y][x]
        current_distance = current_block.water_distance

        # Check if there's space below for water to flow down
        has_space_below = False
        if y < CHUNK_HEIGHT - 1:
            block_below = chunk.blocks[y + 1][x]
            if isinstance(block_below, Block) and block_below.block_type == AIR:
                has_space_below = True

        # Only apply the MAX_SPREAD_DISTANCE limit if there's no space below
        if has_space_below and current_distance >= WaterSimulation.MAX_SPREAD_DISTANCE:
            WaterSimulation._flow_downward(chunk, x, y, chunk_list, updated_blocks)
        elif not has_space_below and current_distance >= WaterSimulation.MAX_SPREAD_DISTANCE:
            return


        # Check left and right blocks
        can_flow_left = False
        can_flow_right = False

        # Check left block
        left_chunk = chunk
        left_x = x - 1

        # If we're at the left edge of the chunk, get the adjacent chunk
        if left_x < 0:
            for c in chunk_list:
                if c.position == chunk.position - 1:
                    left_chunk = c
                    left_x = CHUNK_WIDTH - 1
                    break
            else:
                # No chunk to the left
                left_chunk = None

        # Check if we can flow left
        if left_chunk and 0 <= left_x < CHUNK_WIDTH:
            left_block = left_chunk.blocks[y][left_x]
            if isinstance(left_block, Block) and left_block.block_type == POPPY:
                # Remove poppy and allow water to flow there
                can_flow_left = True

            elif isinstance(left_block, Block) and (left_block.block_type == AIR or left_block.block_type == OAK_LOG):
                can_flow_left = True

        # Check right block
        right_chunk = chunk
        right_x = x + 1

        # If we're at the right edge of the chunk, get the adjacent chunk
        if right_x >= CHUNK_WIDTH:
            for c in chunk_list:
                if c.position == chunk.position + 1:
                    right_chunk = c
                    right_x = 0
                    break
            else:
                # No chunk to the right
                right_chunk = None

        # Check if we can flow right
        if right_chunk and 0 <= right_x < CHUNK_WIDTH:
            right_block = right_chunk.blocks[y][right_x]
            if isinstance(right_block, Block) and right_block.block_type == POPPY:
                # Remove poppy and allow water to flow there
                can_flow_right = True

            elif isinstance(right_block, Block) and (
                    right_block.block_type == AIR or right_block.block_type == OAK_LOG):
                can_flow_right = True

        # Flow in available directions
        if can_flow_left and can_flow_right:
            # Flow in both directions
            # Left
            left_chunk.blocks[y][left_x] = Block(
                left_x * BLOCK_SIZE + left_chunk.offset,
                y * BLOCK_SIZE,
                WATER,
                current_distance + 1  # Increment distance from source
            )
            updated_blocks.add((left_chunk.position, left_x, y))

            # Right
            right_chunk.blocks[y][right_x] = Block(
                right_x * BLOCK_SIZE + right_chunk.offset,
                y * BLOCK_SIZE,
                WATER,
                current_distance + 1  # Increment distance from source
            )
            updated_blocks.add((right_chunk.position, right_x, y))
        elif can_flow_left:
            # Flow left only
            left_chunk.blocks[y][left_x] = Block(
                left_x * BLOCK_SIZE + left_chunk.offset,
                y * BLOCK_SIZE,
                WATER,
                current_distance + 1  # Increment distance from source
            )
            updated_blocks.add((left_chunk.position, left_x, y))
        elif can_flow_right:
            # Flow right only
            right_chunk.blocks[y][right_x] = Block(
                right_x * BLOCK_SIZE + right_chunk.offset,
                y * BLOCK_SIZE,
                WATER,
                current_distance + 1  # Increment distance from source
            )
            updated_blocks.add((right_chunk.position, right_x, y))



    @staticmethod
    def place_water_source(chunk: Any, x: int, y: int) -> None:
        """
        Place a water source block at the specified coordinates.

        Args:
            chunk: The chunk to place the water in.
            x: The x-coordinate within the chunk.
            y: The y-coordinate within the chunk.
        """
        # Check boundaries
        if not (0 <= x < CHUNK_WIDTH and 0 <= y < CHUNK_HEIGHT):
            return

        # Place water block with distance 0 (source block)
        chunk.blocks[y][x] = Block(
            x * BLOCK_SIZE + chunk.offset,
            y * BLOCK_SIZE,
            WATER,
            0  # This is a source block, so distance is 0
        )

    @staticmethod
    def remove_connected_water(chunk: Any, x: int, y: int, chunk_list: List[Any]) -> None:
        """
        Remove all water blocks connected to the specified water block.
        This is used when a water source block is broken to remove all flowing water.

        Args:
            chunk: The chunk containing the water block.
            x: The x-coordinate of the water block within the chunk.
            y: The y-coordinate of the water block within the chunk.
            chunk_list: The list of all chunks.
        """
        # Use a breadth-first search to find all connected water blocks
        visited = set()  # Set of (chunk_position, x, y) tuples
        queue = [(chunk, x, y)]  # Queue of (chunk, x, y) tuples

        while queue:
            current_chunk, current_x, current_y = queue.pop(0)

            # Skip if already visited
            block_id = (current_chunk.position, current_x, current_y)
            if block_id in visited:
                continue

            # Mark as visited
            visited.add(block_id)

            # Skip if not a water block
            if (not (0 <= current_x < CHUNK_WIDTH and 0 <= current_y < CHUNK_HEIGHT) or
                not isinstance(current_chunk.blocks[current_y][current_x], Block) or
                current_chunk.blocks[current_y][current_x].block_type != WATER):
                continue

            # Skip source blocks (only remove flowing water)
            if current_chunk.blocks[current_y][current_x].water_distance == 0:
                continue

            # Remove this water block
            current_chunk.blocks[current_y][current_x] = Block(
                current_x * BLOCK_SIZE + current_chunk.offset,
                current_y * BLOCK_SIZE,
                AIR
            )

            # Check adjacent blocks
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                next_x, next_y = current_x + dx, current_y + dy
                next_chunk = current_chunk

                # Handle chunk boundaries
                if next_x < 0:
                    for c in chunk_list:
                        if c.position == current_chunk.position - 1:
                            next_chunk = c
                            next_x = CHUNK_WIDTH - 1
                            break
                    else:
                        continue  # No chunk to the left
                elif next_x >= CHUNK_WIDTH:
                    for c in chunk_list:
                        if c.position == current_chunk.position + 1:
                            next_chunk = c
                            next_x = 0
                            break
                    else:
                        continue  # No chunk to the right

                # Add to queue if it's a water block
                if (0 <= next_x < CHUNK_WIDTH and 0 <= next_y < CHUNK_HEIGHT and
                    isinstance(next_chunk.blocks[next_y][next_x], Block) and
                    next_chunk.blocks[next_y][next_x].block_type == WATER):
                    queue.append((next_chunk, next_x, next_y))
