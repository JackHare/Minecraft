from typing import Any

class Camera:
    """
    Represents a 2D camera system for managing a viewing area in a game or graphical
    application. The camera determines what portion of the game world is"""
    
    # Class constants for view dimensions
    TILE_SIZE: int = 48
    VIEW_TILES_WIDTH: int = 24
    VIEW_TILES_HEIGHT: int = 16
    DEFAULT_VIEW_WIDTH: int = TILE_SIZE * VIEW_TILES_WIDTH
    DEFAULT_VIEW_HEIGHT: int = TILE_SIZE * VIEW_TILES_HEIGHT

    def __init__(self) -> None:
        self.x: float = 0
        self.y: float = 0
        self.view_width: int = self.DEFAULT_VIEW_WIDTH
        self.view_height: int = self.DEFAULT_VIEW_HEIGHT

    def _calculate_bound(self, position: float, size: float) -> float:
        """Helper method to calculate boundary position."""
        return position + (size / 2)

    @property
    def left_bound(self) -> float:
        return self._calculate_bound(self.x, -self.view_width)

    @property
    def right_bound(self) -> float:
        return self._calculate_bound(self.x, self.view_width)

    @property
    def top_bound(self) -> float:
        return self._calculate_bound(self.y, -self.view_height)

    @property
    def bottom_bound(self) -> float:
        return self._calculate_bound(self.y, self.view_height)

    def set_center_position(self, x: float, y: float) -> None:
        """Sets camera position relative to the top-left boundary."""
        self.x = x - self.view_width / 2
        self.y = y - self.view_height / 2

    def center_on_player(self, player: Any) -> None:
        """
        Centers the view or camera on the specified player. This method calculates
        the center position of the player based on their x, y coordinates and
        dimensions (width and height), and sets the camera's center accordingly.

        :param player: The player object whose center position is used to center the
            view or camera. The player object must have 'x', 'y', 'width', and 'height'
            attributes.
        :type player: Any
        :return: None
        """
        player_center_x = player.x + (player.width / 2)
        player_center_y = player.y + (player.height / 2)
        self.set_center_position(player_center_x, player_center_y)