from typing import Any

class Gravity:
    """
    Handles gravity physics for entities in the game.

    This class applies gravity to entities, allowing them to fall and jump.
    It simulates basic physics including acceleration due to gravity,
    terminal velocity, and ground friction.

    Attributes:
        GRAVITY_ACCELERATION (float): Acceleration due to gravity in pixels/second².
        TERMINAL_VELOCITY (float): Maximum falling speed in pixels/second.
        GROUND_FRICTION (float): Friction coefficient when entity is on ground.
        JUMP_VELOCITY (float): Initial upward velocity when jumping in pixels/second.
        player (Any): The entity affected by gravity.
        game (Any): The game instance.
        vertical_velocity (float): Current vertical velocity in pixels/second.
        is_grounded (bool): Whether the entity is on the ground.
        can_jump (bool): Whether the entity can jump.
    """

    # Physics constants
    GRAVITY_ACCELERATION = 980.0  # pixels/second²
    TERMINAL_VELOCITY = 1000.0    # pixels/second
    GROUND_FRICTION = 0.8         # friction coefficient
    JUMP_VELOCITY = -375.0        # pixels/second (negative is up)

    def __init__(self, player: Any, game: Any) -> None:
        """
        Initialize the gravity physics for an entity.

        Args:
            player: The entity affected by gravity.
            game: The game instance.
        """
        self.player = player
        self.game = game
        self.vertical_velocity = 0.0
        self.is_grounded = False
        self.can_jump = False

    def apply_gravity(self, dt: float) -> None:
        """
        Apply gravity to the entity for the current frame.

        This method updates the entity's vertical velocity and position
        based on gravity acceleration and the time elapsed since the last frame.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        if not self.is_grounded:
            # Apply gravity acceleration
            self.vertical_velocity += self.GRAVITY_ACCELERATION * dt

            # Limit to terminal velocity
            self.vertical_velocity = min(self.vertical_velocity, self.TERMINAL_VELOCITY)

            # Update entity position
            self.player.y_change += self.vertical_velocity * dt
        else:
            # Apply jump velocity
            self.vertical_velocity = self.JUMP_VELOCITY
            self.is_grounded = False

    def jump(self, dt: float) -> None:
        """
        Make the entity jump.

        This method sets the entity's state to jumping and applies
        the initial jump velocity.

        Args:
            dt: Delta time in seconds since the last frame.
        """
        self.is_grounded = True
        self.can_jump = True
        self.apply_gravity(dt)
