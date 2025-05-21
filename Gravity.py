import pygame as pg
import Player
import Game
import Entity

'''
Forces player to stay on ground but is able to jump
'''
class Gravity():
    GRAVITY_ACCELERATION = 980.0
    TERMINAL_VELOCITY = 1000.0
    GROUND_FRICTION = 0.8

    def __init__(self, player, game):
        self.player = player
        self.game = game
        self.vertical_velocity = 0
        self.is_grounded = False
        self.can_jump = False

    def apply_gravity(self, dt):
        if not self.is_grounded:
            self.vertical_velocity += self.GRAVITY_ACCELERATION * dt
            self.vertical_velocity = min(self.vertical_velocity, self.TERMINAL_VELOCITY)
            self.player.y_change += self.vertical_velocity * dt

        else:
                self.vertical_velocity = -375.0
                self.is_grounded = False

    def jump(self, dt):
        self.is_grounded = True
        self.can_jump = True
        self.apply_gravity(dt)
