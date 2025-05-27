"""
Sprite management module for the game.

This module provides functions for loading, managing, and retrieving
sprites for blocks and entities in the game.
"""
import pygame as pg
from typing import Dict, Optional, Union

from world.Block import BLOCK_SIZE, AIR, GRASS, DIRT, STONE, COAL, IRON, GOLD, DIAMOND, OAK_LOG, LEAVES, BEDROCK, \
    OAK_PLANK, COBBLE_STONE, DIAMOND_BLOCK, GOLD_BLOCK, IRON_BLOCK, COAL_BLOCK, POPPY, PUMPKIN, ANDESITE, GRANITE, \
    DIORITE

# Dictionary to store loaded block sprites
block_sprites: Dict[int, pg.Surface] = {}

# Sprite file paths
SPRITE_PATHS = {
    AIR: './rendering/sprites/air.png',
    GRASS: './rendering/sprites/grass.webp',
    DIRT: './rendering/sprites/dirt.webp',
    STONE: './rendering/sprites/stone.webp',
    COAL: './rendering/sprites/coal.png',
    IRON: './rendering/sprites/iron.jpeg',
    GOLD: './rendering/sprites/gold.jpeg',
    DIAMOND: './rendering/sprites/diamond.jpeg',
    OAK_LOG: './rendering/sprites/oaklog.jpg',
    LEAVES: './rendering/sprites/leaves.webp',
    BEDROCK: './rendering/sprites/bedrock.png',
    OAK_PLANK: './rendering/sprites/oak_plank.jpg',
    COBBLE_STONE: './rendering/sprites/cobble_stone.png',
    DIAMOND_BLOCK: './rendering/sprites/diamond_block.png',
    GOLD_BLOCK: './rendering/sprites/gold_block.webp',
    IRON_BLOCK: './rendering/sprites/iron_block.jpg',
    COAL_BLOCK: './rendering/sprites/coal_block.png',
    POPPY: './rendering/sprites/poppy.png',
    PUMPKIN: './rendering/sprites/pumpkin.png',
    ANDESITE: './rendering/sprites/andesite.png',
    GRANITE: './rendering/sprites/granite.webp',
    DIORITE: './rendering/sprites/diorite.webp'
}

# Entity sprite paths
ENTITY_SPRITE_PATHS = {
    "Player": './rendering/sprites/steve.png'
}


def load_block_sprites() -> None:
    """
    Load all block sprites into memory.

    This function loads and scales all block sprites from their respective
    image files and stores them in the block_sprites dictionary.
    """
    for block_type, path in SPRITE_PATHS.items():
        try:
            image = pg.image.load(path)

            # Convert with alpha channel for transparency
            if block_type == POPPY:
                block_sprites[block_type] = pg.transform.scale(
                    image.convert_alpha(),  # Use convert_alpha() for poppy
                    (BLOCK_SIZE, BLOCK_SIZE)
                )
            else:
                # For other block types, convert() might be slightly faster if they don't have transparency
                block_sprites[block_type] = pg.transform.scale(
                    image.convert(),
                    (BLOCK_SIZE, BLOCK_SIZE)
                )

        except Exception as e:
            print(f"Error loading sprite for block type {block_type}: {e}")
            # Create a fallback sprite (purple square for missing textures)
            fallback = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
            fallback.fill((255, 0, 255))  # Purple color
            block_sprites[block_type] = fallback


def get_block_sprite(block_type: int) -> Optional[pg.Surface]:
    """
    Get the sprite for a specific block type.

    Args:
        block_type: The type of block to get the sprite for.

    Returns:
        The sprite surface for the specified block type, or None if not found.
    """
    return block_sprites.get(block_type)


def load_entity_sprite(entity_type: str) -> Optional[pg.Surface]:
    """
    Load and return the sprite for a specific entity type.

    Args:
        entity_type: The type of entity to load the sprite for.

    Returns:
        The sprite surface for the specified entity type, or None if not found.
    """
    if entity_type in ENTITY_SPRITE_PATHS:
        try:
            return pg.transform.scale(
                pg.image.load(ENTITY_SPRITE_PATHS[entity_type]).convert(),
                (BLOCK_SIZE, BLOCK_SIZE)
            )
        except Exception as e:
            print(f"Error loading sprite for entity type {entity_type}: {e}")
            # Create a fallback sprite (red square for missing textures)
            fallback = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
            fallback.fill((255, 0, 0))  # Red color
            return fallback

    return None
