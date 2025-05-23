"""
Rendering module for the game.

This module provides classes for rendering the game world, entities,
and UI elements to the screen.
"""
import pygame as pg
import random
import math
from typing import List, Any, Tuple, Optional, Dict

from rendering import SpriteManager
from world.Block import BLOCK_SIZE


class Sky:
    """
    Manages the sky elements including sun and clouds.

    This class handles the rendering and movement of sky elements
    such as the sun and clouds, including parallax effects.

    Attributes:
        SUN_COLOR (Tuple[int, int, int]): The color of the sun (yellow).
        SUN_SIZE (int): The size of the sun in pixels.
        SUN_POSITION (Tuple[int, int]): The fixed position of the sun.
        CLOUD_COLOR (Tuple[int, int, int]): The color of clouds (white).
        CLOUD_COUNT (int): The number of clouds to generate.
        clouds (List[Dict]): List of cloud data (position, size, speed).
    """

    # Sun settings
    SUN_COLOR = (255, 255, 0)  # Yellow
    SUN_SIZE = 120  # Size in pixels
    SUN_POSITION = (200, 100)  # Fixed position (x, y)

    # Cloud settings
    CLOUD_COLOR = (255, 255, 255)  # White
    CLOUD_COUNT = 10  # Number of clouds

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the sky with sun and clouds.

        Args:
            screen_width: The width of the game window in pixels.
            screen_height: The height of the game window in pixels.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Generate random clouds
        self.clouds = []
        for _ in range(self.CLOUD_COUNT):
            # Random cloud properties
            width = random.randint(100, 300)
            height = random.randint(0, 80)
            x = random.randint(-width, screen_width)
            y = random.randint(0, 400)
            speed = random.uniform(10, 30)  # Pixels per second
            parallax_factor = random.uniform(0.1, 1.0)  # Different depths for parallax

            self.clouds.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'speed': speed,
                'parallax_factor': parallax_factor,
                'x_offset': x
            })

    def update(self, dt: float, camera_x: float) -> None:
        """
        Update cloud positions based on time and camera movement.

        Args:
            dt: Delta time in seconds since the last frame.
            camera_x: The x-coordinate of the camera.
        """
        for cloud in self.clouds:
            # Move clouds based on their speed
            cloud['x_offset'] += cloud['speed'] * dt

            # Apply parallax effect based on camera movement
            cloud['x'] = cloud['x_offset'] + camera_x * 0.01 * cloud['parallax_factor']

            # Wrap clouds around when they go off-screen
            if cloud['x'] > self.screen_width:
                cloud['x'] = -cloud['width']

    def draw(self, screen: pg.Surface) -> None:
        """
            screen: The pygame surface to render to.
        """
        # Draw the sun (a yellow circle)
      #  pg.draw.circle(screen, self.SUN_COLOR, self.SUN_POSITION, self.SUN_SIZE)
        pg.draw.rect(screen, self.SUN_COLOR, (self.SUN_POSITION[0], self.SUN_POSITION[1], self.SUN_SIZE, self.SUN_SIZE), 0)
        # Draw clouds (white rectangles)
        for cloud in self.clouds:
            pg.draw.rect(
                screen,
                self.CLOUD_COLOR,
                (
                    cloud['x'],
                    cloud['y'],
                    cloud['width'],
                    cloud['height']
                ),
                0,  # Filled rectangle
                border_radius=5  # Rounded corners for nicer clouds
            )


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
    INVENTORY_BLOCK_SIZE = 48  # Size of the block icon in the inventory
    INVENTORY_BACKGROUND_COLOR = (0, 0, 0, 180)  # Semi-transparent black
    INVENTORY_SELECTED_COLOR = (255, 255, 255)  # White for selected block
    INVENTORY_BORDER_COLOR = (100, 100, 100)  # Gray for unselected blocks
    INVENTORY_BORDER_WIDTH = 2  # Width of the border around blocks
    INVENTORY_SPACING = 10  # Spacing between blocks in the hotbar
    INVENTORY_TEXT_COLOR = (255, 255, 255)  # White text for block counts

    # Block highlight settings
    BLOCK_HIGHLIGHT_COLOR = (0, 0, 0)  # Black outline for highlighted block
    BLOCK_HIGHLIGHT_WIDTH = 2  # Width of the highlight outline

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

        # Initialize sky with sun and clouds
        self.sky = Sky(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Load sprites
        SpriteManager.load_block_sprites()

        # Set game font
        self.font = pg.font.Font(None, 36)

        # Track time for animations
        self.last_time = pg.time.get_ticks() / 1000.0

    def render_frame(self, player: Any, chunk_list: List[Any], fps: int, inventory: Optional[Any] = None, mouse_pos: Optional[Tuple[int, int]] = None, crafting_menu: Optional[Any] = None) -> None:
        """
        Draw a complete frame to the screen.

        This method clears the screen, draws the background, renders all chunks,
        draws the player, and updates the display.

        Args:
            player: The player entity to render.
            chunk_list: The list of chunks to render.
            fps: The current frames per second to display.
            inventory: The inventory object containing the selected block.
            mouse_pos: The current mouse position (x, y) for block highlighting.
            crafting_menu: The crafting menu to render, or None if the menu is closed.
        """
        # Calculate time delta for animations
        current_time = pg.time.get_ticks() / 1000.0
        dt = current_time - self.last_time
        self.last_time = current_time

        # Clear the screen and draw background
        self.screen.fill(self.BACKGROUND_COLOR)

        # Update and draw the sky
        self.sky.update(dt, self.camera.x)
        self.sky.draw(self.screen)

        # Loop over each chunk and render it
        for chunk in chunk_list:
            chunk.render_chunk(self.screen, self.camera)

        # Highlight the block under the mouse cursor if mouse position is provided
        if mouse_pos:
            self.highlight_block_at_mouse(mouse_pos, chunk_list)

        # Draw the player
        player.render(self.screen, self.camera)

        # Draw the inventory UI if provided
        if inventory:
            self.draw_inventory(inventory)

        # Draw the FPS counter if enabled
        if self.DRAW_FPS:
            self.draw_fps(fps)

        # Draw the crafting menu if provided
        if crafting_menu:
            crafting_menu.draw(self.screen)

        # Update the display
        pg.display.flip()

    def highlight_block_at_mouse(self, mouse_pos: Tuple[int, int], chunk_list: List[Any]) -> None:
        """
        Highlight the block that the mouse is hovering over.

        Args:
            mouse_pos: The current mouse position (x, y).
            chunk_list: The list of chunks to check for blocks.
        """
        # Import here to avoid circular import
        from world.BlockInteraction import BlockInteraction

        # Get the block at the mouse position
        mouse_x, mouse_y = mouse_pos
        block, chunk, block_x, block_y = BlockInteraction.get_block_at_position(
            mouse_x, mouse_y, self.camera, chunk_list
        )

        if block and chunk:
            # Calculate the screen position of the block
            screen_x = block.x - self.camera.x
            screen_y = block.y - self.camera.y

            # Draw a highlight rectangle around the block
            pg.draw.rect(
                self.screen,
                self.BLOCK_HIGHLIGHT_COLOR,
                (
                    screen_x,
                    screen_y,
                    block.width,
                    block.height
                ),
                self.BLOCK_HIGHLIGHT_WIDTH
            )

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
        Draw the inventory hotbar UI to the screen.

        This method draws a hotbar at the bottom center of the screen showing
        all blocks the player has collected, with the selected block highlighted.

        Args:
            inventory: The inventory object containing the collected blocks.
        """
        # Get the collected blocks and selected block
        collected_blocks = inventory.get_collected_blocks()
        selected_block = inventory.get_selected_block()

      #  if not collected_blocks:
       #     return  # No blocks to display

        # Calculate hotbar dimensions
        block_size_with_spacing = self.INVENTORY_BLOCK_SIZE + self.INVENTORY_SPACING
        hotbar_width = 9 * block_size_with_spacing + self.INVENTORY_SPACING
        hotbar_height = self.INVENTORY_BLOCK_SIZE + self.INVENTORY_SPACING * 2

        # Calculate hotbar position (centered at bottom of screen)
        hotbar_x = (self.SCREEN_WIDTH - hotbar_width) // 2
        hotbar_y = self.SCREEN_HEIGHT - hotbar_height - 20  # 20px margin from bottom

        # Create a surface for the background
        background = pg.Surface((hotbar_width, hotbar_height), pg.SRCALPHA)
        background.fill(self.INVENTORY_BACKGROUND_COLOR)

        # Draw the background
        self.screen.blit(background, (hotbar_x, hotbar_y))

        # Draw each block in the hotbar
        for i, block_type in enumerate(collected_blocks):
            # Calculate position for this block
            block_x = hotbar_x + self.INVENTORY_SPACING + i * block_size_with_spacing
            block_y = hotbar_y + self.INVENTORY_SPACING

            # Get the sprite for this block
            block_sprite = SpriteManager.get_block_sprite(block_type)

            if block_sprite:
                # Scale the block sprite to the inventory block size
                scaled_sprite = pg.transform.scale(block_sprite, 
                                                  (self.INVENTORY_BLOCK_SIZE, self.INVENTORY_BLOCK_SIZE))

                # Draw the block sprite
                self.screen.blit(scaled_sprite, (block_x, block_y))

                # Draw the block count
                block_count = inventory.get_block_count(block_type)
                count_text = self.font.render(str(block_count), True, self.INVENTORY_TEXT_COLOR)
                count_rect = count_text.get_rect(bottomright=(block_x + self.INVENTORY_BLOCK_SIZE - 2, 
                                                             block_y + self.INVENTORY_BLOCK_SIZE - 2))
                self.screen.blit(count_text, count_rect)

                # Determine border color based on whether this is the selected block
                border_color = self.INVENTORY_SELECTED_COLOR if block_type == selected_block else self.INVENTORY_BORDER_COLOR

                # Draw a border around the block
                pg.draw.rect(
                    self.screen,
                    border_color,
                    (
                        block_x,
                        block_y,
                        self.INVENTORY_BLOCK_SIZE,
                        self.INVENTORY_BLOCK_SIZE
                    ),
                    self.INVENTORY_BORDER_WIDTH
                )

        for i in range(len(collected_blocks), 9):
            border_color = self.INVENTORY_BORDER_COLOR

            pg.draw.rect(
                self.screen,
                border_color,
                (
                    i * block_size_with_spacing + hotbar_x + self.INVENTORY_SPACING,
                    hotbar_y + self.INVENTORY_SPACING,
                    self.INVENTORY_BLOCK_SIZE,
                    self.INVENTORY_BLOCK_SIZE
                ),
                self.INVENTORY_BORDER_WIDTH
            )
