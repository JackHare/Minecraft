import pygame as pg
import Camera
import Block

class Drawer:

    background_colour = (100, 200, 255)
    screen_width = 24 * Block.BLOCK_SIZE
    screen_height = 16 * Block.BLOCK_SIZE
    window_title = "Minecraft2d"

    def __init__(self,  camera):
        self.camera = camera

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption(self.window_title)
        self.screen.fill(self.background_colour)


    def render_frame(self, player, chunk_list):
        self.screen.fill(self.background_colour)

        for chunk in chunk_list:
            chunk.render_chunk(self.screen, self.camera)

        player.render(self.screen, self.camera)

        pg.display.flip()
