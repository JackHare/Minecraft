"""
World management module for handling chunk loading and unloading.

This module provides functions for managing the game world, including
loading and unloading chunks as the player moves through the world.
"""
from typing import List, Any

from world.Chunk import Chunk, calculate_player_position


def load_chunks(chunk_list: List[Chunk], player: Any) -> None:
    """
    Load and unload chunks based on player position.

    This function checks if chunks need to be loaded or unloaded as the player
    moves through the world. It maintains a list of three chunks centered around
    the player's current position.

    Precondition: chunk_list consists of exactly 3 chunks in the world in a
    sequence ordered left to right.

    Args:
        chunk_list: The list of chunks currently loaded in the world.
        player: The player entity whose position determines chunk loading.
    """
    # Get the player's current chunk position
    player_chunk_pos = calculate_player_position(player)

    # If player is at the left edge of the loaded chunks, load a new chunk to the left
    if chunk_list[0].position == player_chunk_pos:
        # Create a new chunk to the left of the leftmost chunk
        new_chunk = Chunk(chunk_list[0].position - 1)
        chunk_list.insert(0, new_chunk)

        # Remove the rightmost chunk to maintain exactly 3 chunks
        chunk_list.pop()

    # If player is at the right edge of the loaded chunks, load a new chunk to the right
    if chunk_list[2].position == player_chunk_pos:
        # Create a new chunk to the right of the rightmost chunk
        new_chunk = Chunk(chunk_list[-1].position + 1)
        chunk_list.append(new_chunk)

        # Remove the leftmost chunk to maintain exactly 3 chunks
        chunk_list.pop(0)
