from Camera import Camera
from Chunk import Chunk
from Drawer import Drawer
from Keyboard import Keyboard
from Player import Player


class Game:
    def __init__(self):

        # Init a camera object
        self.camera = Camera()

        # Init a renderer object
        self.drawer = Drawer(self.camera)

        # Init a Keyboard object
        self.keyboard = Keyboard()

        # Create our chunks
        self.chunk_list = [Chunk()]

        # Create our player object
        self.player = Player()

    def update(self):
        self.control_updates()

        print(self.player.x, self.player.y)
        self.camera.center_on_player(self.player)
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