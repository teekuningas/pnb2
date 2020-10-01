""" Contains basic way to run observation client
"""

import argparse
import time

from pnb2.networking.network import ObservationClient

from pnb2.game.graphics import initialize
from pnb2.game.graphics import render
from pnb2.game.game import update


from pnb2.game.constants import UPDATE_INTERVAL


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--address')
    parser.add_argument('--port')

    cli_args = parser.parse_args()

    address = '0.0.0.0'
    if cli_args.address:
        address = cli_args.address

    port = 5555
    if cli_args.port:
        port = cli_args.port

    # Initialize graphics engine
    gfx_engine = initialize()

    # Establish connection
    client = ObservationClient(address, port)
    print("Client ID: " + client.client_id)

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

        # Try to get game synchronized
        while lag >= UPDATE_INTERVAL:

            new_game = client.get_game()
            if new_game:
                # if game available from socket, use it
                game = new_game
            else:
                # otherwise, predict
                update(game)

            lag -= UPDATE_INTERVAL

        # Render when not occupied with the update
        render(gfx_engine, game, lag / UPDATE_INTERVAL)

    print("Finished.")

