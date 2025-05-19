import Block
import SpriteManager
import pygame as pg
from Camera import Camera
from Chunk import Chunk, CHUNK_WIDTH, calculate_player_position
from Drawer import Drawer
from Keyboard import Keyboard
from Player import Player
from Gravity import Gravity

class Game:
    def __init__(self):

        # Initialize all fonts for text rendering
        self.dt = None
        pg.font.init()

        # Init a camera object
        self.camera = Camera()



        # Init a renderer object
        self.drawer = Drawer(self.camera)
        SpriteManager.load_block_sprites()

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

        # Set the max frame rate to 300

    def update(self):
        self.control_updates()
        self.player.apply_change(self.chunk_list)
        self.camera.center_on_player(self.player)


        self.update_chunks()
      #  self.camera.x = self.player.x
      #  self.camera.y = self.player.y

        self.drawer.render_frame(self.player, self.chunk_list, self.fps)

        # Update FPS
        self.fps = int(self.clock.get_fps())


    def control_updates(self):
        self.dt = self.clock.tick() / 1000  # Convert milliseconds to seconds
        movement_speed = 600

        if self.keyboard.up or self.keyboard.w:
            self.gravity.jump()
        if self.keyboard.left or self.keyboard.a:
            self.player.x_change -= movement_speed * self.dt
        if self.keyboard.right or self.keyboard.d:
            self.player.x_change += movement_speed * self.dt
        self.gravity.apply_gravity(self.dt)



    def update_chunks(self):


        if self.chunk_list[0].position == calculate_player_position(self.player):
            self.chunk_list.insert(0, Chunk(self.chunk_list[0].position - 1))
            
            self.chunk_list.pop()

        if self.chunk_list[2].position == calculate_player_position(self.player):
            self.chunk_list.append(Chunk(self.chunk_list[-1].position + 1))
            self.chunk_list.pop(0)
