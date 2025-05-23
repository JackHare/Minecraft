"""
Crafting menu module for the game.

This module provides the CraftingMenu class for displaying and interacting
with the crafting menu.
"""
import pygame as pg
from typing import List, Dict, Tuple, Any, Optional, Callable

from world import CraftingRecipes
from rendering import SpriteManager
from world.Block import BLOCK_SIZE


class CraftingMenu:
    """
    Handles the display and interaction with the crafting menu.
    
    This class is responsible for rendering the crafting menu, handling
    button interactions, and providing visual feedback for available recipes.
    
    Attributes:
        MENU_BACKGROUND_COLOR (Tuple[int, int, int, int]): The background color of the menu.
        MENU_BORDER_COLOR (Tuple[int, int, int]): The border color of the menu.
        MENU_BORDER_WIDTH (int): The width of the menu border.
        BUTTON_BACKGROUND_COLOR (Tuple[int, int, int]): The background color of buttons.
        BUTTON_HOVER_COLOR (Tuple[int, int, int]): The background color of buttons when hovered.
        BUTTON_DISABLED_COLOR (Tuple[int, int, int]): The background color of disabled buttons.
        BUTTON_BORDER_COLOR (Tuple[int, int, int]): The border color of buttons.
        BUTTON_BORDER_WIDTH (int): The width of button borders.
        BUTTON_TEXT_COLOR (Tuple[int, int, int]): The color of button text.
        BUTTON_TEXT_DISABLED_COLOR (Tuple[int, int, int]): The color of disabled button text.
        TITLE_TEXT_COLOR (Tuple[int, int, int]): The color of the menu title.
        screen_width (int): The width of the game screen.
        screen_height (int): The height of the game screen.
        menu_width (int): The width of the crafting menu.
        menu_height (int): The height of the crafting menu.
        menu_x (int): The x-coordinate of the crafting menu.
        menu_y (int): The y-coordinate of the crafting menu.
        font (pg.font.Font): The font used for text rendering.
        title_font (pg.font.Font): The font used for the menu title.
        buttons (List[Dict]): List of button data for recipe buttons.
        inventory (Any): The player's inventory.
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
        self.menu_width = 400
        self.menu_height = 300
        self.menu_x = (screen_width - self.menu_width) // 2
        self.menu_y = (screen_height - self.menu_height) // 2
        
        # Initialize fonts
        self.font = pg.font.Font(None, 24)
        self.title_font = pg.font.Font(None, 36)
        
        # Initialize button list (will be populated in update)
        self.buttons = []
        
        # Store reference to inventory (will be set in update)
        self.inventory = None
    
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
        
        # Clear existing buttons
        self.buttons = []
        
        # Create a button for each recipe
        button_height = 60
        button_spacing = 10
        button_width = self.menu_width - 40  # 20px padding on each side
        
        for i, recipe in enumerate(recipes):
            # Calculate button position
            button_x = self.menu_x + 20
            button_y = self.menu_y + 60 + (button_height + button_spacing) * i
            
            # Check if recipe can be crafted
            can_craft = CraftingRecipes.can_craft(recipe, inventory)
            
            # Create button data
            button = {
                'rect': pg.Rect(button_x, button_y, button_width, button_height),
                'recipe': recipe,
                'can_craft': can_craft,
                'hover': False
            }
            
            self.buttons.append(button)
    
    def handle_event(self, event: pg.event.Event) -> Optional[Dict]:
        """
        Handle mouse events for the crafting menu.
        
        Args:
            event: The pygame event to handle.
            
        Returns:
            The recipe that was clicked, or None if no recipe was clicked.
        """
        if event.type == pg.MOUSEMOTION:
            # Update hover state for buttons
            mouse_pos = pg.mouse.get_pos()
            for button in self.buttons:
                button['hover'] = button['rect'].collidepoint(mouse_pos)
        
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Check if a button was clicked
            mouse_pos = pg.mouse.get_pos()
            for button in self.buttons:
                if button['rect'].collidepoint(mouse_pos) and button['can_craft']:
                    return button['recipe']
        
        return None
    
    def draw(self, screen: pg.Surface) -> None:
        """
        Draw the crafting menu to the screen.
        
        Args:
            screen: The pygame surface to render to.
        """
        # Create a surface for the menu background
        menu_surface = pg.Surface((self.menu_width, self.menu_height), pg.SRCALPHA)
        menu_surface.fill(self.MENU_BACKGROUND_COLOR)
        
        # Draw the menu background
        screen.blit(menu_surface, (self.menu_x, self.menu_y))
        
        # Draw the menu border
        pg.draw.rect(
            screen,
            self.MENU_BORDER_COLOR,
            (self.menu_x, self.menu_y, self.menu_width, self.menu_height),
            self.MENU_BORDER_WIDTH
        )
        
        # Draw the menu title
        title_text = self.title_font.render("Crafting", True, self.TITLE_TEXT_COLOR)
        title_rect = title_text.get_rect(centerx=self.menu_x + self.menu_width // 2, y=self.menu_y + 10)
        screen.blit(title_text, title_rect)
        
        # Draw each button
        for button in self.buttons:
            # Determine button color based on state
            if not button['can_craft']:
                bg_color = self.BUTTON_DISABLED_COLOR
                text_color = self.BUTTON_TEXT_DISABLED_COLOR
            elif button['hover']:
                bg_color = self.BUTTON_HOVER_COLOR
                text_color = self.BUTTON_TEXT_COLOR
            else:
                bg_color = self.BUTTON_BACKGROUND_COLOR
                text_color = self.BUTTON_TEXT_COLOR
            
            # Draw button background
            pg.draw.rect(screen, bg_color, button['rect'])
            
            # Draw button border
            pg.draw.rect(screen, self.BUTTON_BORDER_COLOR, button['rect'], self.BUTTON_BORDER_WIDTH)
            
            # Get recipe data
            recipe = button['recipe']
            recipe_name = recipe['name']
            output_type, output_quantity = recipe['output']
            
            # Draw recipe name
            name_text = self.font.render(recipe_name, True, text_color)
            name_rect = name_text.get_rect(x=button['rect'].x + 10, y=button['rect'].y + 5)
            screen.blit(name_text, name_rect)
            
            # Draw input materials
            input_text = "Requires: "
            for block_type, quantity in recipe['inputs'].items():
                input_text += f"{quantity}x {block_type}, "
            input_text = input_text[:-2]  # Remove trailing comma and space
            
            inputs_text = self.font.render(input_text, True, text_color)
            inputs_rect = inputs_text.get_rect(x=button['rect'].x + 10, y=button['rect'].y + 30)
            screen.blit(inputs_text, inputs_rect)
            
            # Draw output item
            output_text = f"Creates: {output_quantity}x {output_type}"
            outputs_text = self.font.render(output_text, True, text_color)
            outputs_rect = outputs_text.get_rect(right=button['rect'].right - 10, centery=button['rect'].centery)
            screen.blit(outputs_text, outputs_rect)