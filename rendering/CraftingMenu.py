"""
Crafting menu module for the game.

This module provides the CraftingMenu class for displaying and interacting
with the crafting menu using pygame_menu.
"""
import pygame as pg
from typing import List, Dict, Tuple, Any, Optional, Callable
import pygame_menu as pm
from pygame_menu.locals import ALIGN_LEFT, ALIGN_CENTER
import pygame_menu.widgets as widgets

from world import CraftingRecipes
from rendering import SpriteManager
from world.Block import BLOCK_SIZE


class CraftingMenu:
    """
    Handles the display and interaction with the crafting menu.

    This class is responsible for rendering the crafting menu, handling
    button interactions, and providing visual feedback for available recipes.
    It uses pygame_menu for rendering and interaction.

    Attributes:
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        menu_width (int): The width of the crafting menu.
        menu_height (int): The height of the crafting menu.
        menu (pm.Menu): The pygame_menu instance.
        inventory (Any): The player's inventory.
        recipe_widgets (List[Dict]): List of widgets for each recipe.
    """

    # Menu appearance settings
    MENU_BACKGROUND_COLOR = (64, 64, 64, 220)  # Dark gray, semi-transparent
    MENU_BORDER_COLOR = (200, 200, 200)  # Light gray
    MENU_BORDER_WIDTH = 2

    # Button appearance settings
    BUTTON_BACKGROUND_COLOR = (100, 100, 100)  # Medium gray
    BUTTON_HOVER_COLOR = (120, 120, 120)  # Lighter gray
    BUTTON_DISABLED_COLOR = (80, 80, 80)  # Darker gray
    BUTTON_BORDER_COLOR = (150, 150, 150)  # Light gray
    BUTTON_BORDER_WIDTH = 1
    BUTTON_TEXT_COLOR = (255, 255, 255)  # White
    BUTTON_TEXT_DISABLED_COLOR = (150, 150, 150)  # Light gray

    # Title appearance settings
    TITLE_TEXT_COLOR = (255, 255, 255)  # White

    # Block type to name mapping
    BLOCK_NAMES = {
        1: "Grass",
        2: "Dirt",
        3: "Stone",
        4: "Coal",
        5: "Iron",
        6: "Gold",
        7: "Diamond",
        8: "Oak Log",
        9: "Oak Leaves",
        10: "Oak Plank",
        11: "Cobblestone",
        12: "Diamond Block",
        13: "Gold Block",
        14: "Iron Block",
        15: "Coal Block"
    }

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """
        Initialize the crafting menu.

        Args:
            screen_width: The width of the game screen.
            screen_height: The height of the game screen.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set menu dimensions (centered on screen)
        self.menu_width = 500
        self.menu_height = 400

        # Create theme for the menu
        self.theme = pm.themes.THEME_DARK.copy()
        self.theme.background_color = self.MENU_BACKGROUND_COLOR
        self.theme.title_background_color = (50, 50, 50)
        self.theme.title_font_color = self.TITLE_TEXT_COLOR
        self.theme.widget_font_color = self.BUTTON_TEXT_COLOR
        self.theme.widget_font_size = 18
        self.theme.title_font_size = 28
        self.theme.widget_margin = (5, 5)
        self.theme.scrollbar_color = self.BUTTON_BORDER_COLOR
        self.theme.scrollbar_slider_color = self.BUTTON_HOVER_COLOR
        self.theme.scrollbar_slider_hover_color = (180, 180, 180)
        self.theme.scrollbar_thickness = 15

        # Store reference to inventory (will be set in update)
        self.inventory = None

        # List to keep track of recipe widgets
        self.recipe_widgets = []

        # Track selected recipe
        self._selected_recipe = None

        # Initialize menu
        self._setup_menu()

    def _get_block_name(self, block_type: int) -> str:
        """Get the display name for a block type."""
        return self.BLOCK_NAMES.get(block_type, f"Block {block_type}")

    def _create_recipe_button(self, recipe: Dict) -> None:
        """
        Create a button for a recipe.

        Args:
            recipe: The recipe dictionary to create a button for.
        """
        # Check if recipe can be crafted
        can_craft = CraftingRecipes.can_craft(recipe, self.inventory)

        # Get recipe data
        recipe_name = recipe['name']
        output_type, output_quantity = recipe['output']

        # Create input requirements text
        input_parts = []
        for block_type, quantity in recipe['inputs'].items():
            block_name = self._get_block_name(block_type)
            input_parts.append(f"{quantity}x {block_name}")
        input_text = ", ".join(input_parts)

        # Create output text
        output_name = self._get_block_name(output_type)
        output_text = f"{output_quantity}x {output_name}"

        # Create button text - keep it concise to fit better
        button_text = f"{output_text}"


        # Create the button
        if can_craft:
            button = self.menu.add.button(
                button_text,
                lambda: self._on_recipe_selected(recipe),  # Use _on_recipe_selected to handle crafting
                font_size=18,
                background_color=self.BUTTON_BACKGROUND_COLOR,
                font_color=self.BUTTON_TEXT_COLOR,
                padding=(10, 8, 10, 8),
                margin=(0, 2)
            )
            # Add requirements as a separate label underneath
            self.menu.add.label(
                f"Needs: {input_text}",
                font_size=14,
                font_color=(200, 200, 200),
                margin=(0, 0)
            )
        else:
            # Disabled button for recipes that can't be crafted
            button = self.menu.add.button(
                button_text,
                lambda: None,  # No action for disabled buttons
                font_size=18,
                background_color=self.BUTTON_DISABLED_COLOR,
                font_color=self.BUTTON_TEXT_DISABLED_COLOR,
                padding=(10, 8, 10, 8),
                margin=(0, 2)
            )
            # Add requirements label for disabled recipes too
            self.menu.add.label(
                f"Needs: {input_text}",
                font_size=14,
                font_color=(120, 120, 120),
                margin=(0, 0)
            )
            # Disable the button
            button.is_selectable = False

    def _on_recipe_selected(self, recipe: Dict) -> None:
        """
        Handle recipe selection and crafting.

        Args:
            recipe: The selected recipe dictionary.
        """
        # Check if recipe can still be crafted (materials available)
        if not CraftingRecipes.can_craft(recipe, self.inventory):
            return

        # Get output block type and quantity
        output_type, output_quantity = recipe['output']

        # Check if inventory has space for the output
        if not self.inventory.can_add(output_type, output_quantity):
            return

        # Remove input materials from inventory
        for block_type, quantity in recipe['inputs'].items():
            self.inventory.remove(block_type, quantity)

        # Add crafted items to inventory
        self.inventory.add(output_type, output_quantity)

        # Store the selected recipe for reference
        self._selected_recipe = recipe

    def update(self, inventory: Any) -> None:
        """
        Update the crafting menu state.

        This method updates the list of available recipes based on the
        player's inventory and updates button states accordingly.

        Args:
            inventory: The player's inventory.
        """
        self.inventory = inventory

        # Get all recipes
        recipes = CraftingRecipes.get_all_recipes()

        # Clear the menu
        self.menu.clear()
        self.recipe_widgets = []

        # Add recipes as buttons
        for recipe in recipes:
            self._create_recipe_button(recipe)
            # Add a separator between recipes for better visual separation
            if recipe != recipes[-1]:  # Don't add separator after last recipe
                self.menu.add.vertical_margin(5)

        # If no recipes available, show a message
        if not recipes:
            self.menu.add.label("No recipes available", font_size=20)

    def handle_event(self, event: pg.event.Event) -> Optional[Dict]:
        """
        Handle events for the crafting menu.

        Args:
            event: The pygame event to handle.

        Returns:
            The recipe that was selected, or None if no recipe was selected.
        """
        # Only process events if menu is enabled
        if not self.menu.is_enabled():
            return None

        # Reset selected recipe at start of event handling
        self._selected_recipe = None

        # Process menu events
        if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            self.menu.update([event])

        # Return selected recipe if one was chosen
        if self._selected_recipe is not None:
            recipe = self._selected_recipe
            self._selected_recipe = None
            return recipe

        return None

    def draw(self, screen: pg.Surface) -> None:
        """
        Draw the crafting menu to the screen.

        Args:
            screen: The pygame surface to render to.
        """
        if self.menu.is_enabled():
            self.menu.draw(screen)


    def toggle(self) -> None:
        """Toggle the crafting menu visibility."""
        if self.menu.is_enabled():
            self.menu.disable()
        else:
            self._setup_menu()
            self.menu.enable()

    def _setup_menu(self) -> None:
        """Create and setup the crafting menu."""
        self.menu = pm.Menu(
            title='Crafting Menu',
            width=self.menu_width,
            height=self.menu_height,
            theme=self.theme,
            center_content=False,
            overflow=True,  # Allow scrolling when content exceeds visible area
            columns=1,
            rows=None  # Allow unlimited rows with scrolling
        )
