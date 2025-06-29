from operator import truediv
from typing import Optional
import pygame as pg

# Movement constants
MOVEMENT_SPEED = 600  # Player movement speed in pixels per second
WATER_MOVEMENT_SPEED = 300  # Player movement speed in water (pixels per second)

def update_input(dt: float, keyboard: 'Keyboard', player: 'Player', gravity: 'Gravity') -> None:
    """
    Process input and update player movement and physics.

    This function handles keyboard input for player movement and applies
    gravity physics. It should be called once per frame.

    Args:
        dt: Delta time in seconds since the last frame.
        keyboard: The keyboard input handler.
        player: The player entity to update.
        gravity: The gravity physics component for the player.
    """
    # Determine movement speed based on whether player is in water
    current_speed = WATER_MOVEMENT_SPEED if player.in_water else MOVEMENT_SPEED

    # Process player movement based on keyboard input
    # Only allow jumping when the player is on the ground
    if (keyboard.up or keyboard.w or keyboard.space) and player.grounded is True:
        gravity.jump(dt)
    if keyboard.left or keyboard.a:
        player.x_change -= current_speed * dt
    if keyboard.right or keyboard.d:
        player.x_change += current_speed * dt

    # Apply gravity physics
    gravity.apply_gravity(dt)
