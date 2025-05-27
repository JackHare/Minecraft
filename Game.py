import pygame as pg
from typing import List, Optional, Dict

from engine.Update import update_input
from input.Event import poll_events
from rendering import SpriteManager
from entity.Camera import Camera
from world.Chunk import Chunk, calculate_player_position
from rendering.Drawer import Drawer
from rendering.CraftingMenu import CraftingMenu
from input.Keyboard import Keyboard
from input.Mouse import Mouse
from entity.Player import Player
from entity.Gravity import Gravity
from world.World import load_chunks
from world.Inventory import Inventory
from world.BlockInteraction import BlockInteraction
from world import CraftingRecipes



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

        # Initialize crafting menu
        self.crafting_menu = CraftingMenu(self.drawer.SCREEN_WIDTH, self.drawer.SCREEN_HEIGHT)
        self.crafting_menu_open = False

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

        # No need to handle crafting menu events here, they will be handled in main_loop

        # Update player position based on physics and input
        self.player.update_player_position(self.chunk_list)

        # Center the camera on the player
        self.camera.center_on_player(self.player)

        # Load or unload chunks as needed based on player position
        load_chunks(self.chunk_list, self.player)

        # Get current mouse position for block highlighting
        mouse_pos = (self.mouse.x, self.mouse.y)

        # Render the current frame
        self.drawer.render_frame(
            self.player, 
            self.chunk_list, 
            self.fps, 
            self.inventory, 
            mouse_pos,
            self.crafting_menu if self.crafting_menu_open else None
        )

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

        # Update keyboard state
        self.keyboard.update()

        # Toggle crafting menu when E is pressed
        print(self.keyboard.e_pressed)
        if self.keyboard.e_pressed:
            self.crafting_menu_open = not self.crafting_menu_open
            # Update crafting menu when opened
            if self.crafting_menu_open:
                self.crafting_menu.update(self.inventory)

        # Only process movement and inventory selection if crafting menu is closed
        if not self.crafting_menu_open:
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
            elif self.keyboard.key_5:
                self.inventory.select_block(4)
            elif self.keyboard.key_6:
                self.inventory.select_block(5)
            elif self.keyboard.key_7:
                self.inventory.select_block(6)
            elif self.keyboard.key_8:
                self.inventory.select_block(7)
            elif self.keyboard.key_9:
                self.inventory.select_block(8)

            if self.keyboard.a or self.keyboard.left:
                self.player.facingLeft = True

            if self.keyboard.d or self.keyboard.right:
                self.player.facingLeft = False

    def handle_block_interaction(self) -> None:
        """
        Handle block breaking and placing based on mouse input.

        This method checks for mouse clicks and calls the appropriate
        BlockInteraction methods to break or place blocks. It also
        manages the inventory, adding blocks when they're broken and
        checking if the player has the block before placing it.
        """
        # Skip block interaction if crafting menu is open
        if self.crafting_menu_open:
            return

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
            # Reset mouse click events at the beginning of each frame
            if self.mouse:
                self.mouse.reset_click_events()

            # Update mouse position
            if self.mouse:
                self.mouse.x, self.mouse.y = pg.mouse.get_pos()

            # Process all events
            for event in pg.event.get():
                # Handle window close event
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                # Handle keyboard events
                if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                    self.keyboard.handle_events(event)

                # Handle mouse events
                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    self.mouse.handle_events(event)

                # Handle crafting menu events when the menu is open
                if self.crafting_menu_open and (event.type == pg.MOUSEMOTION or event.type == pg.MOUSEBUTTONDOWN):
                    recipe = self.crafting_menu.handle_event(event)
                    if recipe:
                        # Craft the item
                        if CraftingRecipes.craft_item(recipe, self.inventory):
                            # Update the crafting menu after crafting
                            self.crafting_menu.update(self.inventory)

            # Update the game
            self.update()
