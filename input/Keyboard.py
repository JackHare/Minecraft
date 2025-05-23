import pygame as pg
from typing import Dict, Any


class Keyboard:
    """
    Handles keyboard input for the game.

    This class tracks the state of keyboard keys and provides methods
    for handling keyboard events.

    Attributes:
        up (bool): Whether the up arrow key is pressed.
        down (bool): Whether the down arrow key is pressed.
        left (bool): Whether the left arrow key is pressed.
        right (bool): Whether the right arrow key is pressed.
        w (bool): Whether the W key is pressed.
        a (bool): Whether the A key is pressed.
        s (bool): Whether the S key is pressed.
        d (bool): Whether the D key is pressed.
        space (bool): Whether the space bar is pressed.
        key_1 (bool): Whether the 1 key is pressed.
        key_2 (bool): Whether the 2 key is pressed.
        key_3 (bool): Whether the 3 key is pressed.
        key_4 (bool): Whether the 4 key is pressed.
        e (bool): Whether the E key is pressed.
        e_pressed (bool): Whether the E key was just pressed this frame.
    """

    def __init__(self) -> None:
        """Initialize a new Keyboard input handler with all keys unpressed."""
        # Arrow keys
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        # WASD keys
        self.w = False
        self.a = False
        self.s = False
        self.d = False

        # Space bar
        self.space = False

        # Number keys for block selection
        self.key_1 = False
        self.key_2 = False
        self.key_3 = False
        self.key_4 = False

        # E key for crafting menu
        self.e = False
        self.e_pressed = False
        self._e_was_pressed = False  # Track previous frame state

    def handle_events(self, event: pg.event.Event) -> None:
        """
        Handle keyboard events to update key states.

        This method updates the state of tracked keys based on
        keyboard events (key presses and releases).

        Args:
            event: The pygame event to handle (must be KEYDOWN or KEYUP).

        Precondition: event is KEYDOWN or KEYUP
        """
        # Set handle to True for key down events, False for key up events
        handle = event.type == pg.KEYDOWN

        # Update the appropriate key state based on the event
        if event.key == pg.K_UP:
            self.up = handle
        elif event.key == pg.K_DOWN:
            self.down = handle
        elif event.key == pg.K_LEFT:
            self.left = handle
        elif event.key == pg.K_RIGHT:
            self.right = handle
        elif event.key == pg.K_w:
            self.w = handle
        elif event.key == pg.K_a:
            self.a = handle
        elif event.key == pg.K_s:
            self.s = handle
        elif event.key == pg.K_d:
            self.d = handle
        # Number keys for block selection
        elif event.key == pg.K_1:
            self.key_1 = handle
        elif event.key == pg.K_2:
            self.key_2 = handle
        elif event.key == pg.K_3:
            self.key_3 = handle
        elif event.key == pg.K_4:
            self.key_4 = handle
        elif event.key == pg.K_SPACE:
            self.space = handle
        elif event.key == pg.K_e:
            self.e = handle

    def update(self) -> None:
        """
        Update the keyboard state for the current frame.

        This method should be called once per frame to reset one-frame flags.
        """
        # Check if E was just pressed (is pressed now but wasn't pressed last frame)
        self.e_pressed = self.e and not self._e_was_pressed

        # Update the previous frame state for next frame
        self._e_was_pressed = self.e