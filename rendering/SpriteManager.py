import pygame as pg

from world import Block

block_sprites = {}

def load_block_sprites():
    block_sprites[0] = pg.transform.scale(pg.image.load('./rendering/sprites/air.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[1] = pg.transform.scale(pg.image.load('./rendering/sprites/grass.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[2] = pg.transform.scale(pg.image.load('./rendering/sprites/dirt.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[3] = pg.transform.scale(pg.image.load('./rendering/sprites/stone.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[4] = pg.transform.scale(pg.image.load('./rendering/sprites/coal.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[5] = pg.transform.scale(pg.image.load('./rendering/sprites/iron.jpeg').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[6] = pg.transform.scale(pg.image.load('./rendering/sprites/gold.jpeg').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[7] = pg.transform.scale(pg.image.load('./rendering/sprites/diamond.jpeg').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[8] = pg.transform.scale(pg.image.load('./rendering/sprites/oaklog.jpg').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))
    block_sprites[9] = pg.transform.scale(pg.image.load('./rendering/sprites/leaves.webp').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))

def get_block_sprite(block_type):
    if block_type in block_sprites:
        return block_sprites[block_type]
    else:
        return None



def load_entity_sprite(entity_type):

    if entity_type == "Player":
        return pg.transform.scale(pg.image.load('./rendering/sprites/steve.png').convert(), (Block.BLOCK_SIZE, Block.BLOCK_SIZE))

    return None