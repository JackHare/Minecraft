"""
Crafting menu module for the game.

This module provides the CraftingMenu class for displaying and interacting
with the crafting menu.
"""
import pygame as pg
from typing import List, Dict, Tuple, Any, Optional, Callable

from world import CraftingRecipes
from rendering import SpriteManager
from world.Block import BLOCK_SIZE, AIR, COAL_BLOCK, OAK_LOG, DIAMOND, DIAMOND_BLOCK, GOLD, GOLD_BLOCK, IRON, \
    IRON_BLOCK, OAK_PLANK, COAL, STONE, COBBLE_STONE

BLOCK_NAMES = {
    AIR : "Air",
    COAL_BLOCK : "Coal",
    OAK_LOG : "Oak Log",
    DIAMOND : "Diamond",
    DIAMOND_BLOCK : "Diamond Block",
    GOLD : "Gold",
    GOLD_BLOCK : "Gold Block",
    IRON : "Iron",
    IRON_BLOCK : "Iron Block",
    OAK_PLANK  : "Oak Plank",
    COAL : "Coal",
    STONE : "Stone",
    COBBLE_STONE : "Cobblestone"
}

class CraftingMenu:
    """
    Handles the display and interaction with the crafting menu with scrolling support.
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
        """Initialize the crafting menu."""

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

        # Initialize button list
        self.buttons = []
        self.inventory = None

        # Scrolling variables
        self.scroll_offset = 0  # How much we've scrolled down (in pixels)
        self.scroll_speed = 30  # Pixels per scroll step

        # Button layout constants
        self.button_height = 60
        self.button_spacing = 10
        self.title_height = 50  # Space reserved for title
        self.padding = 20

        # Calculate scrollable area
        self.scroll_area_top = self.menu_y + self.title_height
        self.scroll_area_height = self.menu_height - self.title_height - self.padding
        self.scroll_area_bottom = self.scroll_area_top + self.scroll_area_height

    def get_max_scroll(self) -> int:
        """Calculate the maximum scroll offset."""
        if not self.buttons:
            return 0

        total_buttons_height = len(self.buttons) * (self.button_height + self.button_spacing)
        max_scroll = total_buttons_height - self.scroll_area_height
        return max(0, max_scroll)

    def clamp_scroll(self) -> None:
        """Ensure scroll offset is within valid bounds."""
        max_scroll = self.get_max_scroll()
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def update(self, inventory: Any) -> None:
        """Update the crafting menu state."""
        self.inventory = inventory
        recipes = CraftingRecipes.get_all_recipes()

        # Clear and rebuild buttons
        self.buttons = []
        button_width = self.menu_width - (self.padding * 2)

        for i, recipe in enumerate(recipes):
            # Calculate ORIGINAL position (before applying scroll)
            button_x = self.menu_x + self.padding
            button_y = self.scroll_area_top + self.padding // 2 + (self.button_height + self.button_spacing) * i

            can_craft = CraftingRecipes.can_craft(recipe, inventory)

            button = {
                'original_rect': pg.Rect(button_x, button_y, button_width, self.button_height),
                'recipe': recipe,
                'can_craft': can_craft,
                'hover': False,
                'index': i
            }
            self.buttons.append(button)

        # Clamp scroll after updating buttons
        self.clamp_scroll()

    def handle_event(self, event: pg.event.Event) -> Optional[Dict]:
        """Handle events including scrolling."""

        # Handle scrolling with mouse wheel
        if event.type == pg.MOUSEWHEEL:
            mouse_pos = pg.mouse.get_pos()
            menu_rect = pg.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)

            if menu_rect.collidepoint(mouse_pos):
                # Scroll up = negative y, scroll down = positive y
                self.scroll_offset -= event.y * self.scroll_speed
                self.clamp_scroll()
                print(f"Mouse scroll: event.y={event.y}, new offset={self.scroll_offset}")  # Debug
                return None

        # Handle scrolling with keyboard
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.scroll_offset -= self.scroll_speed
                self.clamp_scroll()
                print(f"Key UP: new offset={self.scroll_offset}")  # Debug
                return None
            elif event.key == pg.K_DOWN:
                self.scroll_offset += self.scroll_speed
                self.clamp_scroll()
                print(f"Key DOWN: new offset={self.scroll_offset}")  # Debug
                return None

        # Handle mouse movement for hover detection
        elif event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()

            for button in self.buttons:
                # Calculate current displayed position
                display_rect = self.get_button_display_rect(button)

                # Check if mouse is over this button and button is visible
                if (self.is_button_visible(button) and
                    display_rect.collidepoint(mouse_pos)):
                    button['hover'] = True
                else:
                    button['hover'] = False

        # Handle mouse clicks
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = pg.mouse.get_pos()

            for button in self.buttons:
                display_rect = self.get_button_display_rect(button)

                if (self.is_button_visible(button) and
                    display_rect.collidepoint(mouse_pos) and
                    button['can_craft']):
                    return button['recipe']

        return None

    def get_button_display_rect(self, button: Dict) -> pg.Rect:
        """Get the current display rectangle for a button (with scroll applied)."""
        original_rect = button['original_rect']
        return pg.Rect(
            original_rect.x,
            original_rect.y - self.scroll_offset,  # Apply scroll offset
            original_rect.width,
            original_rect.height
        )

    def is_button_visible(self, button: Dict) -> bool:
        """Check if a button is currently visible in the scroll area."""
        display_rect = self.get_button_display_rect(button)
        return (display_rect.bottom > self.scroll_area_top and
                display_rect.top < self.scroll_area_bottom)

    def draw(self, screen: pg.Surface) -> None:
        """Draw the crafting menu to the screen."""

        # Draw menu background
        menu_surface = pg.Surface((self.menu_width, self.menu_height), pg.SRCALPHA)
        menu_surface.fill(self.MENU_BACKGROUND_COLOR)
        screen.blit(menu_surface, (self.menu_x, self.menu_y))

        # Draw menu border
        pg.draw.rect(
            screen,
            self.MENU_BORDER_COLOR,
            (self.menu_x, self.menu_y, self.menu_width, self.menu_height),
            self.MENU_BORDER_WIDTH
        )

        # Draw title
        title_text = self.title_font.render("Crafting", True, self.TITLE_TEXT_COLOR)
        title_rect = title_text.get_rect(centerx=self.menu_x + self.menu_width // 2, y=self.menu_y + 10)
        screen.blit(title_text, title_rect)

        # Set clipping rectangle for scrollable content
        scroll_clip_rect = pg.Rect(
            self.menu_x,
            self.scroll_area_top,
            self.menu_width,
            self.scroll_area_height
        )
        old_clip = screen.get_clip()
        screen.set_clip(scroll_clip_rect)

        # Draw buttons
        visible_count = 0
        for button in self.buttons:
            if self.is_button_visible(button):
                visible_count += 1
                display_rect = self.get_button_display_rect(button)
                self.draw_button(screen, button, display_rect)

        # Restore clipping
        screen.set_clip(old_clip)

        # Draw scroll indicator
        self.draw_scroll_indicator(screen)

        # Debug info (remove in production)
        debug_text = f"Scroll: {self.scroll_offset}/{self.get_max_scroll()}, Visible: {visible_count}/{len(self.buttons)}"
        debug_surface = self.font.render(debug_text, True, (255, 255, 0))
        screen.blit(debug_surface, (10, 10))

    def draw_button(self, screen: pg.Surface, button: Dict, display_rect: pg.Rect) -> None:
        """Draw a single button."""

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
        pg.draw.rect(screen, bg_color, display_rect)

        # Draw button border
        pg.draw.rect(screen, self.BUTTON_BORDER_COLOR, display_rect, self.BUTTON_BORDER_WIDTH)

        # Get recipe data
        recipe = button['recipe']
        recipe_name = recipe['name']
        output_type, output_quantity = recipe['output']

        # Draw recipe name
        name_text = self.font.render(recipe_name, True, text_color)
        name_rect = name_text.get_rect(x=display_rect.x + 10, y=display_rect.y + 5)
        screen.blit(name_text, name_rect)

        # Draw input materials
        input_text = "Requires: "
        for block_type, quantity in recipe['inputs'].items():
            input_text += f"{quantity}x {BLOCK_NAMES[block_type]}, "
        input_text = input_text[:-2]  # Remove trailing comma and space

        inputs_text = self.font.render(input_text, True, text_color)
        inputs_rect = inputs_text.get_rect(x=display_rect.x + 10, y=display_rect.y + 30)
        screen.blit(inputs_text, inputs_rect)

        # Draw output item
        output_text = f"Creates: {output_quantity}"
        outputs_text = self.font.render(output_text, True, text_color)
        outputs_rect = outputs_text.get_rect(right=display_rect.right - 10, centery=display_rect.centery)
        screen.blit(outputs_text, outputs_rect)

    def draw_scroll_indicator(self, screen: pg.Surface) -> None:
        """Draw a simple scroll indicator."""
        max_scroll = self.get_max_scroll()

        if max_scroll > 0:
            # Draw scroll track
            track_rect = pg.Rect(
                self.menu_x + self.menu_width - 15,
                self.scroll_area_top,
                10,
                self.scroll_area_height
            )
            pg.draw.rect(screen, (100, 100, 100), track_rect)

            # Draw scroll thumb
            thumb_height = max(20, int((self.scroll_area_height / (max_scroll + self.scroll_area_height)) * self.scroll_area_height))
            thumb_y = track_rect.y + int((self.scroll_offset / max_scroll) * (track_rect.height - thumb_height))

            thumb_rect = pg.Rect(
                track_rect.x + 2,
                thumb_y,
                track_rect.width - 4,
                thumb_height
            )
            pg.draw.rect(screen, (200, 200, 200), thumb_rect)