"""
Mouse input handling module for the game.

This module provides classes for tracking and handling mouse input,
including position and button clicks.
"""
from typing import Tuple
import pygame as pg

class Mouse:
    """
    Handles mouse input for the game.

    This class tracks the state of the mouse, including its position
    and button states.

    Attributes:
        x (int): The x-coordinate of the mouse cursor.
        y (int): The y-coordinate of the mouse cursor.
        right_click (bool): Whether the right mouse button is pressed.
        left_click (bool): Whether the left mouse button is pressed.
        right_click_event (bool): Whether a right click event occurred this frame.
        left_click_event (bool): Whether a left click event occurred this frame.
    """

    def __init__(self) -> None:
        """Initialize a new Mouse input handler with default values."""
        self.x = 0
        self.y = 0
        self.right_click = False
        self.left_click = False
        self.right_click_event = False
        self.left_click_event = False

    def get_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position.

        Returns:
            A tuple containing the (x, y) coordinates of the mouse cursor.
        """
        return (self.x, self.y)

    def update_position(self, x: int, y: int) -> None:
        """
        Update the mouse position.

        Args:
            x: The new x-coordinate of the mouse cursor.
            y: The new y-coordinate of the mouse cursor.
        """
        self.x = x
        self.y = y

    def handle_events(self, event: 'pg.event.Event') -> None:
        """
        Handle mouse events to update mouse state.

        This method updates the state of the mouse based on mouse events
        (button presses and releases).

        Args:
            event: The pygame event to handle (must be MOUSEBUTTONDOWN or MOUSEBUTTONUP).
        """
        # Reset click events at the beginning of each frame
        self.left_click_event = False
        self.right_click_event = False

        # Handle mouse button events
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.left_click = True
                self.left_click_event = True
            elif event.button == 3:  # Right mouse button
                self.right_click = True
                self.right_click_event = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.left_click = False
            elif event.button == 3:  # Right mouse button
                self.right_click = False

    def reset_click_events(self) -> None:
        """Reset click events at the beginning of each frame."""
        self.left_click_event = False
        self.right_click_event = False
