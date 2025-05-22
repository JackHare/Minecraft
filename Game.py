import pygame as pg
from typing import List, Optional

from engine.Update import update_input
from input.Event import poll_events
from rendering import SpriteManager
from entity.Camera import Camera
from world.Chunk import Chunk, calculate_player_position
from rendering.Drawer import Drawer
from input.Keyboard import Keyboard
from input.Mouse import Mouse
from entity.Player import Player
from entity.Gravity import Gravity
from world.World import load_chunks
from world.Inventory import Inventory
from world.BlockInteraction import BlockInteraction


class Game:
    """
    Main game class that orchestrates all game components and the game loop.

    This class is responsible for initializing all game components, updating
    game state, handling input, and rendering the game world.

    Attributes:
        dt (float): Delta time between frames in seconds.
        camera (Camera): The camera that determines the view position.
        drawer (Drawer): The renderer for drawing the game world.
        keyboard (Keyboard): The keyboard input handler.
        chunk_list (List[Chunk]): List of chunks that make up the game world.
        player (Player): The player entity controlled by the user.
        clock (pg.time.Clock): The game clock for timing and FPS calculation.
        gravity (Gravity): The gravity physics component for the player.
        fps (int): Current frames per second.
    """

    def __init__(self) -> None:
        """Initialize the game and all its components."""
        # Initialize attributes that were previously class variables
        self.dt: float = 0

        # Init a camera object
        self.camera = Camera()

        # Init our renderer object
        self.drawer = Drawer(self.camera)

        # Init input handlers
        self.keyboard = Keyboard()
        self.mouse = Mouse()

        # Create our chunks
        self.chunk_list: List[Chunk] = [Chunk(-1), Chunk(0), Chunk(1)]

        # Create our player object
        self.player = Player()

        # Create our clock object
        self.clock = pg.time.Clock()

        # Create gravity physics for the player
        self.gravity = Gravity(self.player, self)

        # Create inventory for block selection
        self.inventory = Inventory()

        # Tracks game fps
        self.fps: int = 0

    def update(self) -> None:
        """
        Update the game state for one frame.

        This method handles input processing, physics updates, camera positioning,
        world loading, and rendering.
        """
        # Process input and update player movement
        self.control_updates()

        # Handle block breaking and placing
        self.handle_block_interaction()

        # Update player position based on physics and input
        self.player.update_player_position(self.chunk_list)

        # Center the camera on the player
        self.camera.center_on_player(self.player)

        # Load or unload chunks as needed based on player position
        load_chunks(self.chunk_list, self.player)

        # Get current mouse position for block highlighting
        mouse_pos = (self.mouse.x, self.mouse.y)

        # Render the current frame
        self.drawer.render_frame(self.player, self.chunk_list, self.fps, self.inventory, mouse_pos)

        # Update FPS counter
        self.fps = int(self.clock.get_fps())

    def control_updates(self) -> None:
        """
        Process input and update player movement and physics.

        This method calculates delta time for the current frame and
        delegates input handling to the update_input function.
        """
        # Calculate delta time for this frame
        self.dt = self.clock.tick() / 1000  # Convert milliseconds to seconds

        # Use the update_input function to handle player movement
        update_input(self.dt, self.keyboard, self.player, self.gravity)

        # Handle inventory selection with number keys
        if self.keyboard.key_1:
            self.inventory.select_block(0)
        elif self.keyboard.key_2:
            self.inventory.select_block(1)
        elif self.keyboard.key_3:
            self.inventory.select_block(2)
        elif self.keyboard.key_4:
            self.inventory.select_block(3)

    def handle_block_interaction(self) -> None:
        """
        Handle block breaking and placing based on mouse input.

        This method checks for mouse clicks and calls the appropriate
        BlockInteraction methods to break or place blocks. It also
        manages the inventory, adding blocks when they're broken and
        checking if the player has the block before placing it.
        """
        # Handle block breaking (right click)
        if self.mouse.right_click_event:
            # Try to break the block
            block_type = BlockInteraction.break_block(
                self.mouse.x, self.mouse.y,
                self.camera, self.chunk_list, self.player
            )

            # If a block was broken, add it to the inventory
            if block_type and block_type != 0:  # 0 is AIR
                self.inventory.add_block(block_type)

        # Handle block placing (left click)
        if self.mouse.left_click_event:
            selected_block = self.inventory.get_selected_block()

            # Only try to place the block if the player has it in their inventory
            if selected_block != 0 and self.inventory.has_block(selected_block):
                # Try to place the block
                placed = BlockInteraction.place_block(
                    self.mouse.x, self.mouse.y,
                    self.camera, self.chunk_list, self.player,
                    selected_block
                )

                # If the block was placed, remove it from the inventory
                if placed:
                    self.inventory.remove_block(selected_block)

    def main_loop(self) -> None:
        """
        Main game loop that runs continuously until the game is exited.

        This method handles the game's main loop, updating the game state
        and processing events each frame.
        """
        while True:
            # Poll events (keyboard, mouse, window events)
            poll_events(keyboard=self.keyboard, mouse=self.mouse)

            # Update the game
            self.update()
