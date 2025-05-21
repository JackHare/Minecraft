import pygame as pg

from rendering import SpriteManager


class Drawer:

    background_colour = (100, 200, 255)
    screen_width = 1280
    screen_height = 720
    window_title = "Minecraft2d"

    DRAW_FPS = True

    def __init__(self,  camera):

        # Initialize all fonts for text rendering
        pg.font.init()

        # Set our camera object
        self.camera = camera

        # Create the window
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), vsync=1)
        pg.display.set_caption(self.window_title)

        # Set sky color
        self.screen.fill(self.background_colour)

        # Load sprites
        SpriteManager.load_block_sprites()

        # Set game font
        self.font = pg.font.Font(None, 36)

    # Draw a frame to the screen
    def render_frame(self, player, chunk_list, fps):

        # Clear the screen and draw background
        self.screen.fill(self.background_colour)

        # Loop over each chunk and render it
        for chunk in chunk_list:
            chunk.render_chunk(self.screen, self.camera)

        # Draw the player
        player.render(self.screen, self.camera)

        # Draw the FPS
        if self.DRAW_FPS:
            self.draw_fps(fps)

        # Update the display
        pg.display.flip()

    # Draw the fps to the screen
    def draw_fps(self, fps):
        fps_text = self.font.render(f'FPS: {fps}', True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(fps_text, fps_rect)