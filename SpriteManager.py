import pygame as pg

import Block


def load_sprite(block_type):
    if block_type == 0:
        return pg.transform.scale(pg.image.load('./sprites/air.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    if block_type == 1:
        return pg.transform.scale(pg.image.load('./sprites/grass.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    if block_type == 2:
        return pg.transform.scale(pg.image.load('./sprites/dirt.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    return None