import pygame as pg

def load_sprite(block_type):
    if block_type == 1:
        return pg.image.load('./sprites/grass.webp').convert()
    return None