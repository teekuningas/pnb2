""" Contains logics of the game
"""

from constants import GRAVITATION_CONSTANT


def initialize_game():
    """ Gets an initial game position, which is simply a dictionary
    """
    game = {}
    game['players'] = [
        {'id': 0, 'team': 0},
        {'id': 1, 'team': 1}
    ]
    game['ball'] = {
        'x': 0,
        'y': 10,
        'z': 0,
        'dx': 0,
        'dy': 1,
        'dz': 0,
    }
    return game


def update(game, inputs):
    """ Update game variables based on inputs
    """

def deepmerge(destination, source):
    """ Merges two nested dictionaries 
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            deepmerge(node, value)
        else:
            destination[key] = value

    return destination

def merge(game, new_game):
    """ Merges upstream game to local one 
    """
    deepmerge(game, new_game) 

