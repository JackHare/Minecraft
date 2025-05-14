import pygame as pg

import Block


block_sprites = {}

def load_block_sprites():
    block_sprites[0] = pg.transform.scale(pg.image.load('./sprites/air.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[1] = pg.transform.scale(pg.image.load('./sprites/grass.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[2] = pg.transform.scale(pg.image.load('./sprites/dirt.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[3] = pg.transform.scale(pg.image.load('./sprites/stone.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))

def get_block_sprite(block_type):
    if block_type in block_sprites:
        return block_sprites[block_type]
    else:
        return None



def load_entity_sprite(entity_type):

    if entity_type == "Player":
        return pg.transform.scale(pg.image.load('./sprites/steve.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))

    return None