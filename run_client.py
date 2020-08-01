""" Contains basic way to run client side game loop
"""

import argparse
import keyboard
import time

from network import Client

from graphics import initialize
from graphics import render

from input_ import get_inputs

from game import update
from game import merge

from constants import UPDATE_INTERVAL


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address')
    parser.add_argument('--port')

    cli_args = parser.parse_args()

    ip_address = '127.0.0.1'
    if cli_args.ip_address:
        ip_address = cli_args.ip_address

    port = 5555
    if cli_args.port:
        port = cli_args.port

    # Initialize graphics
    window = initialize()

    # Establish connection
    client = Client(ip_address, port)

    while True:
        client_idx = client.get_client_idx()
        if client_idx is not None:
            break

    # Get initial copy of the game state
    while True:
        game = client.get_game()
        if game:
            break

    previous = time.time()
    inputs = [[], []]
    lag = 0
    while True:
        current = time.time()
        elapsed = current - previous
        previous = current
        lag += elapsed

        if not client.connection_alive:
            print("Connection dead.. Quitting..")
            break

        new_inputs = get_inputs()

        # Send inputs to upstream
        if new_inputs:
            client.send_inputs(inputs)

        for input_ in new_inputs:
            if input_ not in inputs[client_idx]:
                inputs[client_idx].append(input_)

        # Try to get game synchronized
        while lag >= UPDATE_INTERVAL:
            print("Updating game.")

            # Get official version of the game from upstream and merge
            new_game = client.get_game()
            if new_game:
                merge(game, new_game)

            # Predict state of the game with local copy
            update(game, inputs)

            inputs = [[], []]

            lag -= UPDATE_INTERVAL

        # Render when not occupied with the update
        render(window, game, lag / UPDATE_INTERVAL)

    print("Finished.")

