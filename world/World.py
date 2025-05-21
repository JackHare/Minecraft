"""
Checks to see if chunks need to be loaded in or out relative to the player
Precondition: chunk_list consists of 3 chunks in the world in a sequence ordered left to right
"""
from world.Chunk import Chunk, calculate_player_position


def load_chunks(chunk_list, player):
    if chunk_list[0].position == calculate_player_position(player):
        chunk_list.insert(0, Chunk(chunk_list[0].position - 1))

        chunk_list.pop()

    if chunk_list[2].position == calculate_player_position(player):
        chunk_list.append(Chunk(chunk_list[-1].position + 1))
        chunk_list.pop(0)