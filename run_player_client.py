""" Contains basic way to run client side game loop
"""

import argparse
import time

from network import PlayerClient

from input_ import get_inputs

from game import update
from game import merge

from constants import UPDATE_INTERVAL
from constants import N_PLAYER_CLIENTS_NEEDED


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address')
    parser.add_argument('--port')
    parser.add_argument('--bind_key')
    parser.add_argument('--rejoin_key')

    cli_args = parser.parse_args()

    ip_address = '127.0.0.1'
    if cli_args.ip_address:
        ip_address = cli_args.ip_address

    port = 5555
    if cli_args.port:
        port = cli_args.port

    bind_key = 'keyboard_right'
    if cli_args.bind_key:
        bind_key = cli_args.bind_key

    rejoin_key = None
    if cli_args.rejoin_key:
        rejoin_key = cli_args.rejoin_key

    # Establish connection
    client = PlayerClient(ip_address, port, rejoin_key)

    print('Client ID (use on rejoin): ' + client.client_id)

    player_idx = client.client_id.split('#')[0]

    # Get initial copy of the game state
    while True:
        game = client.get_game()
        if game:
            break

    previous = time.time()
    lag = 0
    while True:
        current = time.time()
        elapsed = current - previous
        previous = current
        lag += elapsed

        if not client.connection_alive:
            print("Connection dead.. Quitting..")
            break

        new_inputs = get_inputs(bind_key)

        # Send inputs to upstream
        if new_inputs:
            client.send_inputs(new_inputs)

        # Try to get game synchronized
        while lag >= UPDATE_INTERVAL:

            # Get official version of the game from upstream and merge
            new_game = client.get_game()
            if new_game:
                merge(game, new_game)

            # Predict state of the game with local copy
            update(game)

            lag -= UPDATE_INTERVAL

    print("Finished.")

