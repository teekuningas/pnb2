""" Contains basic way to run client side game loop
"""

import argparse
import time

from pnb2.networking.network import PlayerClient
from pnb2.game.input_ import get_inputs
from pnb2.game.game import update
from pnb2.game.constants import UPDATE_INTERVAL

N_PLAYER_CLIENTS_NEEDED = 2


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--address')
    parser.add_argument('--port')
    parser.add_argument('--bind_key')
    parser.add_argument('--rejoin_key')

    cli_args = parser.parse_args()

    address = '127.0.0.1'
    if cli_args.address:
        address = cli_args.address

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
    client = PlayerClient(address, port, rejoin_key)

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
        lag += current - previous
        previous = current

        if not client.connection_alive:
            print("Connection dead.. Quitting..")
            break

        new_inputs = get_inputs(bind_key)

        # Send inputs to upstream
        if new_inputs:
            client.send_inputs(new_inputs)

        # Try to get game synchronized
        while lag >= UPDATE_INTERVAL:

            new_game = client.get_game()
            if new_game:
                # if game available from socket, use it
                game = new_game
            else:
                # else, predict
                update(game)

            lag -= UPDATE_INTERVAL

    print("Finished.")

