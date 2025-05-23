"""
Inventory management module for the game.

This module provides the Inventory class for managing the player's
block selection and inventory.
"""
from typing import Dict, List, Optional, Tuple

from world.Block import GRASS, STONE, OAK_LOG, IRON, AIR, LEAVES, DIAMOND, GOLD, COAL, DIRT, OAK_PLANK, COBBLE_STONE


class Inventory:
    """
    Manages the player's block selection and inventory.

    This class tracks which blocks the player has collected and selected,
    and provides methods for selecting and using blocks.

    Attributes:
        AVAILABLE_BLOCKS (List[int]): List of block types that can be collected.
        collected_blocks (Dict[int, int]): Dictionary mapping block types to quantities.
        selected_block (int): The currently selected block type.
        selected_index (int): The index of the currently selected block in the hotbar.
    """

    # List of block types that can be collected (grass, stone, log, iron)
    AVAILABLE_BLOCKS = [GRASS, DIRT, STONE, OAK_LOG, IRON, LEAVES, COAL, GOLD, DIAMOND, OAK_PLANK, COBBLE_STONE]

    def __init__(self) -> None:
        """Initialize a new Inventory with no blocks collected."""
        # Dictionary to track collected blocks and their quantities
        self.collected_blocks: Dict[int, int] = {}

        # Start with some blocks for testing (remove in production)

        # Initialize selection
        self.selected_block = AIR
        self.selected_index = 0

        # Update selected block if we have any
        self._update_selected_block()

    def add_block(self, block_type: int, quantity: int = 1) -> None:
        """
        Add blocks to the inventory.

        Args:
            block_type: The type of block to add.
            quantity: The number of blocks to add.
        """
        if block_type in self.AVAILABLE_BLOCKS:
            if block_type in self.collected_blocks:
                self.collected_blocks[block_type] += quantity
            else:
                self.collected_blocks[block_type] = quantity

            # If this is our first block, select it
            if self.select_block == AIR:
                self._update_selected_block()

    def remove_block(self, block_type: int, quantity: int = 1) -> bool:
        """
        Remove blocks from the inventory.

        Args:
            block_type: The type of block to remove.
            quantity: The number of blocks to remove.

        Returns:
            True if blocks were successfully removed, False otherwise.
        """
        if block_type in self.collected_blocks and self.collected_blocks[block_type] >= quantity:
            self.collected_blocks[block_type] -= quantity

            # If we run out of this block, remove it from inventory and update selection
            if self.collected_blocks[block_type] <= 0:
                del self.collected_blocks[block_type]
                if block_type == self.selected_block:
                    self._update_selected_block()

            return True
        return False

    def has_block(self, block_type: int) -> bool:
        """
        Check if the inventory has at least one of the specified block type.

        Args:
            block_type: The type of block to check.

        Returns:
            True if the inventory has at least one of the block, False otherwise.
        """
        return block_type in self.collected_blocks and self.collected_blocks[block_type] > 0

    def get_block_count(self, block_type: int) -> int:
        """
        Get the number of blocks of the specified type in the inventory.

        Args:
            block_type: The type of block to count.

        Returns:
            The number of blocks of the specified type.
        """
        return self.collected_blocks.get(block_type, 0)

    def select_block(self, index: int) -> None:
        """
        Select a block by index.

        Args:
            index: The index of the block to select.
        """
        # Get a list of collected blocks
        collected_block_types = list(self.collected_blocks.keys())

        if 0 <= index < len(collected_block_types):
            self.selected_index = index
            self.selected_block = collected_block_types[index]

    def select_next_block(self) -> None:
        """Select the next block in the inventory."""
        collected_block_types = list(self.collected_blocks.keys())

        if collected_block_types:
            self.selected_index = (self.selected_index + 1) % len(collected_block_types)
            self.selected_block = collected_block_types[self.selected_index]

    def select_previous_block(self) -> None:
        """Select the previous block in the inventory."""
        collected_block_types = list(self.collected_blocks.keys())

        if collected_block_types:
            self.selected_index = (self.selected_index - 1) % len(collected_block_types)
            self.selected_block = collected_block_types[self.selected_index]

    def get_selected_block(self) -> int:
        """
        Get the currently selected block type.

        Returns:
            The block type of the currently selected block.
        """
        return self.selected_block

    def get_collected_blocks(self) -> List[int]:
        """
        Get a list of all collected block types.

        Returns:
            A list of block types that have been collected.
        """
        return list(self.collected_blocks.keys())

    def _update_selected_block(self) -> None:
        """Update the selected block based on available blocks."""
        collected_block_types = list(self.collected_blocks.keys())

        if collected_block_types:
            # If we have blocks, select the first one
            self.selected_index = 0
            self.selected_block = collected_block_types[0]
        else:
            # If we have no blocks, select AIR
            self.selected_index = 0
            self.selected_block = AIR
