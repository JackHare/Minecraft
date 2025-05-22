"""
Event handling module for the game.

This module provides functions for polling and handling game events
such as keyboard input, mouse input, and window close events.
"""
import pygame as pg
from typing import Any, Optional


def poll_events(keyboard: Any, mouse: Optional[Any] = None) -> None:
    """
    Poll and handle all pending pygame events.

    This function processes all pending events in the pygame event queue,
    including window close events, keyboard events, and mouse events.

    Args:
        keyboard: The keyboard input handler to update with keyboard events.
        mouse: The mouse input handler to update with mouse events.
    """
    # Reset mouse click events at the beginning of each frame
    if mouse:
        mouse.reset_click_events()

    # Update mouse position
    if mouse:
        mouse.x, mouse.y = pg.mouse.get_pos()

    for event in pg.event.get():
        # Handle window close event
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        # Handle keyboard events (key press and release)
        if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
            keyboard.handle_events(event)

        # Handle mouse events (button press and release)
        if mouse and (event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP):
            mouse.handle_events(event)
