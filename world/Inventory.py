"""
Inventory management module for the game.

This module provides the Inventory class for managing the player's
block selection and inventory.
"""
from typing import Dict, List, Optional, Tuple

from world.Block import GRASS, STONE, OAK_LOG, IRON


class Inventory:
    """
    Manages the player's block selection and inventory.

    This class tracks which blocks the player has selected and
    provides methods for selecting and using blocks.

    Attributes:
        AVAILABLE_BLOCKS (List[int]): List of block types available in the inventory.
        selected_block (int): The currently selected block type.
        selected_index (int): The index of the currently selected block in AVAILABLE_BLOCKS.
    """

    # List of block types available in the inventory (grass, stone, log, iron)
    AVAILABLE_BLOCKS = [GRASS, STONE, OAK_LOG, IRON]

    def __init__(self) -> None:
        """Initialize a new Inventory with the first block selected."""
        self.selected_block = self.AVAILABLE_BLOCKS[0]
        self.selected_index = 0

    def select_block(self, index: int) -> None:
        """
        Select a block by index.

        Args:
            index: The index of the block to select (0-3).
        """
        if 0 <= index < len(self.AVAILABLE_BLOCKS):
            self.selected_index = index
            self.selected_block = self.AVAILABLE_BLOCKS[index]

    def select_next_block(self) -> None:
        """Select the next block in the inventory."""
        self.selected_index = (self.selected_index + 1) % len(self.AVAILABLE_BLOCKS)
        self.selected_block = self.AVAILABLE_BLOCKS[self.selected_index]

    def select_previous_block(self) -> None:
        """Select the previous block in the inventory."""
        self.selected_index = (self.selected_index - 1) % len(self.AVAILABLE_BLOCKS)
        self.selected_block = self.AVAILABLE_BLOCKS[self.selected_index]

    def get_selected_block(self) -> int:
        """
        Get the currently selected block type.

        Returns:
            The block type of the currently selected block.
        """
        return self.selected_block