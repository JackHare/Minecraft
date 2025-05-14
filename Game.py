import Block
import SpriteManager
from Camera import Camera
from Chunk import Chunk, CHUNK_WIDTH, calculate_player_position
from Drawer import Drawer
from Keyboard import Keyboard
from Player import Player


class Game:
    def __init__(self):

        # Init a camera object
        self.camera = Camera()


        # Init a renderer object
        self.drawer = Drawer(self.camera)
        SpriteManager.load_block_sprites()

        # Init a Keyboard object
        self.keyboard = Keyboard()

        self.chunk_list = [Chunk(-1), Chunk(0), Chunk(1)]

        # Create our player object
        self.player = Player()

    def update(self):
        self.control_updates()
        self.camera.center_on_player(self.player)
        self.update_chunks()
      #  self.camera.x = self.player.x
      #  self.camera.y = self.player.y

        self.drawer.render_frame(self.player, self.chunk_list)

    def control_updates(self):
        if self.keyboard.up or self.keyboard.w:
            self.player.y -= 10
        if self.keyboard.down or self.keyboard.s:
            self.player.y += 10
        if self.keyboard.left or self.keyboard.a:
            self.player.x -= 10
        if self.keyboard.right or self.keyboard.d:
            self.player.x += 10

    def update_chunks(self):


        if self.chunk_list[0].position == calculate_player_position(self.player):
            self.chunk_list.insert(0, Chunk(self.chunk_list[0].position - 1))
            self.chunk_list.pop()

        if self.chunk_list[2].position == calculate_player_position(self.player):
            self.chunk_list.append(Chunk(self.chunk_list[-1].position + 1))
            self.chunk_list.pop(0)

