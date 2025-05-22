import pygame as pg
from typing import Any

from world.Block import BLOCK_SIZE
from entity.Hitbox import Hitbox


class Player(Hitbox):
    """
    Represents the player character in the game.

    The player is a special type of entity with a hitbox for collision detection
    and the ability to move and interact with the game world.

    Attributes:
        image_copy (pygame.Surface): A copy of the original player image.
        facingLeft (bool): Whether the player is facing left.
    """

    def __init__(self) -> None:
        """
        Initialize a new Player entity.

        The player starts at position (0, 0) with a width of 0.6 blocks
        and a height of 1.8 blocks.
        """
        # Create a player with a hitbox slightly smaller than the block size
        super().__init__(0, 0, BLOCK_SIZE * 0.6, BLOCK_SIZE * 1.8, "Player")

        # Store a copy of the original image for flipping
        self.image_copy = self.image.copy()

        # Player starts facing left
        self.facingLeft = True

    def render(self, screen: pg.Surface, camera: Any) -> None:
        """
        Render the player on the screen.

        This method updates the player's rectangle position based on the camera
        position, flips the player image if facing left, and then draws the
        player's image on the screen.

        Args:
            screen: The pygame surface to render the player on.
            camera: The camera object that determines the view position.
        """
        # Update player position relative to camera
        self.rect.x = self.x - camera.x
        self.rect.y = self.y - camera.y

        # Flip the player image if facing left
        if self.facingLeft:
            self.image = pg.transform.flip(self.image_copy, True, False)
            self.image.set_colorkey((0, 0, 0))  # Make black transparent

        # Draw the player on the screen
        screen.blit(self.image, self.rect)
