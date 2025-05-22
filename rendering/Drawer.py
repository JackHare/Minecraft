"""
Rendering module for the game.

This module provides classes for rendering the game world, entities,
and UI elements to the screen.
"""
import pygame as pg
from typing import List, Any, Tuple, Optional

from rendering import SpriteManager
from world.Block import BLOCK_SIZE


class Drawer:
    """
    Handles rendering of the game world and UI elements.

    This class is responsible for drawing the game world, entities,
    and UI elements to the screen each frame.

    Attributes:
        BACKGROUND_COLOR (Tuple[int, int, int]): The sky color (RGB).
        SCREEN_WIDTH (int): The width of the game window in pixels.
        SCREEN_HEIGHT (int): The height of the game window in pixels.
        WINDOW_TITLE (str): The title of the game window.
        DRAW_FPS (bool): Whether to display the FPS counter.
        camera (Any): The camera object that determines the view position.
        screen (pg.Surface): The pygame surface representing the game window.
        font (pg.font.Font): The font used for text rendering.
    """

    # Display settings
    BACKGROUND_COLOR = (100, 200, 255)  # Sky blue
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    WINDOW_TITLE = "Minecraft2d"

    # UI settings
    DRAW_FPS = True
    FPS_TEXT_COLOR = (255, 255, 255)  # White
    FPS_POSITION = (SCREEN_WIDTH - 10, 10)  # Top right

    # Inventory UI settings
    INVENTORY_POSITION = (10, 10)  # Top left
    INVENTORY_BLOCK_SIZE = 48  # Size of the block icon in the inventory
    INVENTORY_BACKGROUND_COLOR = (0, 0, 0, 128)  # Semi-transparent black
    INVENTORY_BORDER_COLOR = (255, 255, 255)  # White
    INVENTORY_BORDER_WIDTH = 2  # Width of the border around the selected block

    def __init__(self, camera: Any) -> None:
        """
        Initialize the renderer.

        Args:
            camera: The camera object that determines the view position.
        """
        # Initialize all fonts for text rendering
        pg.font.init()

        # Set our camera object
        self.camera = camera

        # Create the window
        self.screen = pg.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
            vsync=1
        )
        pg.display.set_caption(self.WINDOW_TITLE)

        # Set sky color
        self.screen.fill(self.BACKGROUND_COLOR)

        # Load sprites
        SpriteManager.load_block_sprites()

        # Set game font
        self.font = pg.font.Font(None, 36)

    def render_frame(self, player: Any, chunk_list: List[Any], fps: int, inventory: Optional[Any] = None) -> None:
        """
        Draw a complete frame to the screen.

        This method clears the screen, draws the background, renders all chunks,
        draws the player, and updates the display.

        Args:
            player: The player entity to render.
            chunk_list: The list of chunks to render.
            fps: The current frames per second to display.
            inventory: The inventory object containing the selected block.
        """
        # Clear the screen and draw background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Loop over each chunk and render it
        for chunk in chunk_list:
            chunk.render_chunk(self.screen, self.camera)

        # Draw the player
        player.render(self.screen, self.camera)

        # Draw the inventory UI if provided
        if inventory:
            self.draw_inventory(inventory)

        # Draw the FPS counter if enabled
        if self.DRAW_FPS:
            self.draw_fps(fps)

        # Update the display
        pg.display.flip()

    def draw_fps(self, fps: int) -> None:
        """
        Draw the FPS counter to the screen.

        Args:
            fps: The current frames per second to display.
        """
        # Render the FPS text
        fps_text = self.font.render(f'FPS: {fps}', True, self.FPS_TEXT_COLOR)

        # Position the text in the top right corner
        fps_rect = fps_text.get_rect(topright=self.FPS_POSITION)

        # Draw the text to the screen
        self.screen.blit(fps_text, fps_rect)

    def draw_inventory(self, inventory: Any) -> None:
        """
        Draw the inventory UI to the screen.

        This method draws the selected block in the top left corner of the screen.

        Args:
            inventory: The inventory object containing the selected block.
        """
        # Get the selected block type
        selected_block = inventory.get_selected_block()

        # Get the sprite for the selected block
        block_sprite = SpriteManager.get_block_sprite(selected_block)

        if block_sprite:
            # Create a surface for the background
            background = pg.Surface((self.INVENTORY_BLOCK_SIZE + 10, self.INVENTORY_BLOCK_SIZE + 10), pg.SRCALPHA)
            background.fill(self.INVENTORY_BACKGROUND_COLOR)

            # Draw the background
            self.screen.blit(background, self.INVENTORY_POSITION)

            # Scale the block sprite to the inventory block size
            scaled_sprite = pg.transform.scale(block_sprite, (self.INVENTORY_BLOCK_SIZE, self.INVENTORY_BLOCK_SIZE))

            # Draw the block sprite
            self.screen.blit(scaled_sprite, (self.INVENTORY_POSITION[0] + 5, self.INVENTORY_POSITION[1] + 5))

            # Draw a border around the selected block
            pg.draw.rect(
                self.screen,
                self.INVENTORY_BORDER_COLOR,
                (
                    self.INVENTORY_POSITION[0],
                    self.INVENTORY_POSITION[1],
                    self.INVENTORY_BLOCK_SIZE + 10,
                    self.INVENTORY_BLOCK_SIZE + 10
                ),
                self.INVENTORY_BORDER_WIDTH
            )
