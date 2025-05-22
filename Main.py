"""
Main entry point for the Minecraft 2D game.

This module initializes the game and starts the main game loop.
"""
import pygame as pg

from Game import Game


def main() -> None:
    """
    Initialize and start the game.

    This function creates a new Game instance and starts the main game loop.
    """
    # Initialize pygame
    pg.init()

    # Create a new game instance
    game = Game()

    # Start the main game loop
    game.main_loop()


if __name__ == "__main__":
    main()
