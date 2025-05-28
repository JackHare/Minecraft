"""
Block interaction module for the game.

This module provides the BlockInteraction class for handling
block breaking and placing in the game world.
"""
import math
from typing import List, Any, Optional, Tuple

import pygame as pg

from world.Block import Block, AIR, BLOCK_SIZE, BEDROCK, STONE, COBBLE_STONE, WATER
from world.WaterSimulation import WaterSimulation
from world.Chunk import CHUNK_WIDTH, CHUNK_HEIGHT


class BlockInteraction:
    """
    Handles block breaking and placing in the game world.

    This class provides methods for breaking and placing blocks,
    including checking if a block is within reach of the player.

    Attributes:
        MAX_REACH (int): The maximum distance in blocks that the player can reach.
    """

    # Maximum distance in blocks that the player can reach
    MAX_REACH = 6

    @staticmethod
    def get_block_at_position(screen_x: int, screen_y: int, camera: Any, chunk_list: List[Any]) -> Tuple[Optional[Block], Optional[Any], int, int]:
        """
        Get the block at the specified screen position.

        Args:
            screen_x: The x-coordinate on the screen.
            screen_y: The y-coordinate on the screen.
            camera: The camera object that determines the view position.
            chunk_list: The list of chunks to check for blocks.

        Returns:
            A tuple containing:
            - The block at the specified position, or None if no block is found.
            - The chunk containing the block, or None if no block is found.
            - The x-coordinate of the block within the chunk.
            - The y-coordinate of the block within the chunk.
        """
        # Convert screen coordinates to world coordinates
        world_x = screen_x + camera.x
        world_y = screen_y + camera.y

        # Convert world coordinates to chunk coordinates
        chunk_x = math.floor(world_x / (CHUNK_WIDTH * BLOCK_SIZE))
        block_x = math.floor((world_x % (CHUNK_WIDTH * BLOCK_SIZE)) / BLOCK_SIZE)
        block_y = math.floor(world_y / BLOCK_SIZE)

        # Find the chunk that contains the block
        chunk = None
        for c in chunk_list:
            if c.position == chunk_x:
                chunk = c
                break

        # If no chunk is found or the block coordinates are out of bounds, return None
        if not chunk or block_x < 0 or block_x >= CHUNK_WIDTH or block_y < 0 or block_y >= CHUNK_HEIGHT:
            return None, None, block_x, block_y

        # Return the block, chunk, and block coordinates
        return chunk.blocks[block_y][block_x], chunk, block_x, block_y

    @staticmethod
    def is_within_reach(player: Any, block_x: int, block_y: int, chunk: Any) -> bool:
        """
        Check if a block is within reach of the player.

        Args:
            player: The player entity.
            block_x: The x-coordinate of the block within the chunk.
            block_y: The y-coordinate of the block within the chunk.
            chunk: The chunk containing the block.

        Returns:
            True if the block is within reach of the player, False otherwise.
        """
        # Calculate the absolute position of the block
        block_abs_x = chunk.position * CHUNK_WIDTH * BLOCK_SIZE + block_x * BLOCK_SIZE
        block_abs_y = block_y * BLOCK_SIZE

        # Calculate the center of the player
        player_center_x = player.x + player.width / 2
        player_center_y = player.y + player.height / 2

        # Calculate the center of the block
        block_center_x = block_abs_x + BLOCK_SIZE / 2
        block_center_y = block_abs_y + BLOCK_SIZE / 2

        # Calculate the distance between the player and the block
        distance = math.sqrt((player_center_x - block_center_x) ** 2 + (player_center_y - block_center_y) ** 2)

        # Convert distance from pixels to blocks
        distance_in_blocks = distance / BLOCK_SIZE

        # Check if the block is within reach
        return distance_in_blocks <= BlockInteraction.MAX_REACH

    @staticmethod
    def break_block(mouse_x: int, mouse_y: int, camera: Any, chunk_list: List[Any], player: Any) -> int:
        """
        Break the block at the specified screen position.

        Args:
            mouse_x: The x-coordinate of the mouse on the screen.
            mouse_y: The y-coordinate of the mouse on the screen.
            camera: The camera object that determines the view position.
            chunk_list: The list of chunks to check for blocks.
            player: The player entity.

        Returns:
            The block type that was broken, or 0 (AIR) if no block was broken.
        """
        # Get the block at the mouse position
        block, chunk, block_x, block_y = BlockInteraction.get_block_at_position(mouse_x, mouse_y, camera, chunk_list)

        # If no block is found or the block is air, return AIR
        if not block or not chunk or block.block_type == AIR or block.block_type == BEDROCK:
            return AIR

        # Check if the block is within reach of the player
        if not BlockInteraction.is_within_reach(player, block_x, block_y, chunk):
            return AIR

        # Store the block type before breaking it
        broken_block_type = block.block_type

        # Special handling for water blocks
        if broken_block_type == WATER:
            # Check if this is a source block
            is_source = block.water_distance == 0

            if is_source:
                # If it's a source block, remove all connected water blocks first
                WaterSimulation.remove_connected_water(chunk, block_x, block_y, chunk_list)
                # Then replace the source block with air
                chunk.blocks[block_y][block_x] = Block(
                    block_x * BLOCK_SIZE + chunk.offset,
                    block_y * BLOCK_SIZE,
                    AIR
                )
                # Return WATER to add to inventory
                return WATER
            else:
                # For non-source water blocks, just remove the single block
                chunk.blocks[block_y][block_x] = Block(
                    block_x * BLOCK_SIZE + chunk.offset,
                    block_y * BLOCK_SIZE,
                    AIR
                )
                # Non-source water blocks don't give water
                return AIR

        # If block was stone, give back cobble stone instead
        if broken_block_type == STONE:
            broken_block_type = COBBLE_STONE

        # Break the block by replacing it with air
        chunk.blocks[block_y][block_x] = Block(
            block_x * BLOCK_SIZE + chunk.offset,
            block_y * BLOCK_SIZE,
            AIR
        )

        # Return the type of block that was broken
        return broken_block_type

    @staticmethod
    def place_block(mouse_x: int, mouse_y: int, camera: Any, chunk_list: List[Any], player: Any, block_type: int) -> bool:
        """
        Place a block at the specified screen position.

        Args:
            mouse_x: The x-coordinate of the mouse on the screen.
            mouse_y: The y-coordinate of the mouse on the screen.
            camera: The camera object that determines the view position.
            chunk_list: The list of chunks to check for blocks.
            player: The player entity.
            block_type: The type of block to place.

        Returns:
            True if a block was placed, False otherwise.
        """
        # Get the block at the mouse position
        block, chunk, block_x, block_y = BlockInteraction.get_block_at_position(mouse_x, mouse_y, camera, chunk_list)

        # If no chunk is found, return False
        if not chunk:
            return False

        # If the block is not air, we can't place a block here
        if block and block.block_type != AIR:
            return False

        # Check if the block is within reach of the player
        if not BlockInteraction.is_within_reach(player, block_x, block_y, chunk):
            return False

        # Check if the player is trying to place a block on themselves
        player_chunk_x = math.floor(player.x / (CHUNK_WIDTH * BLOCK_SIZE))
        player_block_x = math.floor((player.x % (CHUNK_WIDTH * BLOCK_SIZE)) / BLOCK_SIZE)
        player_block_y = math.floor(player.y / BLOCK_SIZE)
        player_block_y_bottom = math.floor((player.y + player.height - 1) / BLOCK_SIZE)

        if (chunk.position == player_chunk_x and
            block_x == player_block_x and
            (block_y == player_block_y or block_y == player_block_y_bottom)):
            return False

        # Handle water blocks specially
        if block_type == WATER:
            WaterSimulation.place_water_source(chunk, block_x, block_y)
        else:
            # Place a regular block
            chunk.blocks[block_y][block_x] = Block(
                block_x * BLOCK_SIZE + chunk.offset,
                block_y * BLOCK_SIZE,
                block_type
            )

        return True
