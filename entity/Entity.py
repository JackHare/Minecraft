import pygame as pg
from typing import Any

from rendering import SpriteManager


class Entity:
    """
    Base class for all game entities.

    This class provides the basic functionality for rendering and positioning
    entities in the game world. All game entities should inherit from this class.

    Attributes:
        x (float): The x-coordinate of the entity in the game world.
        y (float): The y-coordinate of the entity in the game world.
        width (int): The width of the entity in pixels.
        height (int): The height of the entity in pixels.
        type (str): The type of the entity, used for loading the appropriate sprite.
        image (pygame.Surface): The sprite image for the entity.
        rect (pygame.Rect): The rectangle representing the entity's position and size.
    """

    def __init__(self, x: float, y: float, width: int, height: int, type: str) -> None:
        """
        Initialize a new Entity.

        Args:
            x: The initial x-coordinate of the entity.
            y: The initial y-coordinate of the entity.
            width: The width of the entity in pixels.
            height: The height of the entity in pixels.
            type: The type of the entity, used for loading the appropriate sprite.
        """
        self.x = x  # Fixed: Initialize x to the parameter value
        self.y = y  # Fixed: Initialize y to the parameter value
        self.width = width
        self.height = height
        self.type = type
        self.image = SpriteManager.load_entity_sprite(type)
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.rect.width = self.width
        self.rect.height = self.height  # Fixed: Use height instead of width

    def render(self, screen: pg.Surface, camera: Any) -> None:
        """
        Render the entity on the screen.

        This method updates the entity's rectangle position based on the camera
        position and then draws the entity's image on the screen.

        Args:
            screen: The pygame surface to render the entity on.
            camera: The camera object that determines the view position.
        """
        self.rect.x = self.x - camera.x
        self.rect.y = self.y - camera.y
        screen.blit(self.image, self.rect)
