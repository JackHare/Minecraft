import math
from enum import nonmember

import Block
from Chunk import Chunk, CHUNK_WIDTH, CHUNK_HEIGHT, calculate_player_position
from Entity import Entity


GRAVITY = 9.8  # m/s^2, adjust as needed for your game's scale

class Hitbox(Entity):
    def __init__(self, x, y, width, height, type, mass=1.0, friction_coefficient=0.5):
        super().__init__(x, y, width, height, type)
        self.chunk_y = None
        self.chunk_x = None
        self.x_change = 0
        self.y_change = 0
        self.mass = mass
        self.friction_coefficient = friction_coefficient
        self.grounded = True  # Add a grounded state
        
    """ Applies the x and y change to x and y, if the change puts its inside of a block it doesnt do it, and moves it against the hit box of the block"""
    def apply_change(self, chunk_list):

        absolute_x = self.x
        self.chunk_x = math.floor((absolute_x % (CHUNK_WIDTH * Block.BLOCK_SIZE)) / Block.BLOCK_SIZE)
        self.chunk_y = math.floor(self.y / Block.BLOCK_SIZE)
        chunk_number = calculate_player_position(self)
        
        # Calculate if we are on the left or right edge of a chunk
        onLeftEdge = self.chunk_x % CHUNK_WIDTH == 0
        onRightEdge = self.chunk_x % CHUNK_WIDTH == CHUNK_WIDTH - 1

        left_chunk = chunk_list[1]
        center_chunk = chunk_list[1]
        right_chunk = chunk_list[1]

        if onLeftEdge:
            left_chunk = chunk_list[0]

        if onRightEdge:
            right_chunk = chunk_list[2]

        # contains a list of blocks the player is colliding with if we were to move to x_change
        block_list = list()

        # Check blocks in a 5x6 area around the player
        for dy in range(-2, 4):
            for dx in range(-2, 3):
                check_x = self.chunk_x + dx
                check_y = self.chunk_y + dy

                # Determine which chunk to check based on position
                current_chunk = center_chunk
                if check_x < 0:
                    if left_chunk:
                        check_x = CHUNK_WIDTH + check_x
                        current_chunk = left_chunk
                elif check_x >= CHUNK_WIDTH:
                    if right_chunk:
                        check_x = check_x - CHUNK_WIDTH
                        current_chunk = right_chunk
                    else:
                        continue
                else:
                    current_chunk = center_chunk

                # Add block to list if it exists in the chunk
                if 0 <= check_x < CHUNK_WIDTH and 0 <= check_y < CHUNK_HEIGHT and current_chunk:
                    block = current_chunk.blocks[check_y][check_x]
                    if block is not None and block.block_type != 0:
                        # Adjust block's absolute position based on chunk
                        block.x = (current_chunk.position * CHUNK_WIDTH * Block.BLOCK_SIZE) + (
                                    check_x * Block.BLOCK_SIZE)
                        if self.check_collision(block, self.x_change, self.y_change):
                            block_list.append(block)

        # Resolve collisions
        for block in block_list:
            # Calculate overlap in x and y axes
            x_overlap = min(self.x + self.width, block.x + block.width) - max(self.x, block.x)
            y_overlap = min(self.y + self.height, block.y + block.height) - max(self.y, block.y)

            # Determine collision side and adjust position
            if x_overlap < y_overlap:
                if self.x < block.x:  # Collision on the left
                    self.x_change = block.x - self.width
                else:  # Collision on the right
                    self.x_change = block.x + block.width
            else:
                if self.y < block.y:  # Collision from above
                    self.y_change = block.y - self.height
                    self.grounded = True
                    self.y_change = self.y
                else:  # Collision from below
                    self.y_change = block.y + block.height

    
        self.x = self.x_change
        self.y = self.y_change

    def check_collision(self, block, x, y):
        # Check if rectangles overlap in both x and y axes
        if (x < block.x + block.width and
                x + self.width > block.x and
                y < block.y + block.height and
                y + self.height > block.y):
            return True
        return False
