from engine.Update import update_input
from input.Event import poll_events
from rendering import SpriteManager
import pygame as pg
from entity.Camera import Camera
from world.Chunk import Chunk, calculate_player_position
from rendering.Drawer import Drawer
from input.Keyboard import Keyboard
from entity.Player import Player
from entity.Gravity import Gravity
from world.World import load_chunks


class Game:
    dt = None
    camera = None
    drawer = None
    keyboard = None
    chunk_list = None
    player = None
    clock = None
    fps = 0

    def __init__(self):
        # Init a camera object
        self.camera = Camera()

        # Init our renderer object
        self.drawer = Drawer(self.camera)

        # Init a Keyboard object
        self.keyboard = Keyboard()

        # Create our chunks
        self.chunk_list = [Chunk(-1), Chunk(0), Chunk(1)]

        # Create our player object
        self.player = Player()

        # Create our clock object
        self.clock = pg.time.Clock()

        self.gravity = Gravity(self.player, self)

        # Tracks game fps
        self.fps = 0

    def update(self):
        update_input(dt=self.dt, keyboard=self.keyboard, player=self.player, gravity=self.gravity, clock=self.clock)

        self.player.update_player_position(self.chunk_list)
        self.camera.center_on_player(self.player)


        load_chunks(self.chunk_list, self.player)

        self.drawer.render_frame(self.player, self.chunk_list, self.fps)

        # Update FPS
        self.fps = int(self.clock.get_fps())


    def control_updates(self):
        self.dt = self.clock.tick() / 1000  # Convert milliseconds to seconds
        movement_speed = 600
        print(self.gravity.vertical_velocity )
        if self.keyboard.up or self.keyboard.w and self.gravity.vertical_velocity == 0:
            self.gravity.jump(self.dt)
        if self.keyboard.left or self.keyboard.a:
            self.player.x_change -= movement_speed * self.dt
        if self.keyboard.right or self.keyboard.d:
            self.player.x_change += movement_speed * self.dt
        self.gravity.apply_gravity(self.dt)





    # Loop over the game
    def main_loop(self):
        while True:

            # Update the game
            self.update()

            # Poll events
            poll_events(keyboard=self.keyboard)