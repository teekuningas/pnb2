""" Contains logics of the game
"""

from constants import GRAVITATION_CONSTANT
from constants import N_PLAYER_CLIENTS_NEEDED


def initialize_game():
    """ Gets an initial game position, which is simply a dictionary
    """
    game = {}
    game['players'] = [
        {'controlled': True, 
         'team': 0,
         'x': 0,
         'z': -1,
         'dx': 0,
         'dz': 0},
        {'controlled': True, 
         'team': 1,
         'x': 0,
         'z': 1,
         'dx': 0,
         'dz': 0}
    ]
    game['ball'] = {
        'x': 0,
        'y': 10,
        'z': 0,
        'dx': 0,
        'dy': 0,
        'dz': 0,
    }
    return game


def update(game, inputs=None):
    """ Update game variables based on inputs
    """

    if not inputs:
        inputs = [[] for _ in range(N_PLAYER_CLIENTS_NEEDED)]

    # update ball
    game['ball']['dy'] -= GRAVITATION_CONSTANT

    if game['ball']['y'] + game['ball']['dy'] < 0:
        game['ball']['dy'] = -game['ball']['dy']

    game['ball']['y'] += game['ball']['dy']

    # update players
    for player in game['players']:
        if not player['controlled']:
            continue

        if 'CONTROLLED_MOVE_LEFT' in inputs[player['team']]:
            player['dx'] = -0.5
        if 'CONTROLLED_MOVE_RIGHT' in inputs[player['team']]:
            player['dx'] = 0.5
        if 'CONTROLLED_MOVE_LEFTRIGHT_STOP' in inputs[player['team']]:
            player['dx'] = 0
        if 'CONTROLLED_MOVE_DOWN' in inputs[player['team']]:
            player['dz'] = -0.5
        if 'CONTROLLED_MOVE_UP' in inputs[player['team']]:
            player['dz'] = 0.5
        if 'CONTROLLED_MOVE_UPDOWN_STOP' in inputs[player['team']]:
            player['dz'] = 0

    for player in game['players']:
        player['x'] += player['dx']
        player['z'] += player['dz']

