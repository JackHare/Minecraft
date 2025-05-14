import pygame as pg
import Camera
import Block


class Drawer:

    background_colour = (100, 200, 255)
    screen_width = 1280
    screen_height = 720
    window_title = "Minecraft2d"

    def __init__(self,  camera):
        self.camera = camera

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), vsync=1)
        pg.display.set_caption(self.window_title)
        self.screen.fill(self.background_colour)
        self.clock = pg.time.Clock()
        pg.font.init()
        self.font = pg.font.Font(None, 36)
        self.fps = 0

    def render_frame(self, player, chunk_list):
        self.screen.fill(self.background_colour)

        for chunk in chunk_list:
            chunk.render_chunk(self.screen, self.camera)

        player.render(self.screen, self.camera)

        self.fps = int(self.clock.get_fps())
        fps_text = self.font.render(f'FPS: {self.fps}', True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(fps_text, fps_rect)

        pg.display.flip()
        self.clock.tick(250)
