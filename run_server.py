""" Contains basic way to run server side game loop
"""
import argparse
import time

from pprint import pprint

from game import initialize_game
from game import update

from network import Server

from constants import UPDATE_INTERVAL


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_address')
    parser.add_argument('--port')

    cli_args = parser.parse_args()

    print("Initializing game..")
    game = initialize_game()

    print("Searching for clients..")
    server = Server()

    print("Starting the main loop..")
    previous = time.time()
    inputs = [[], []]
    while True:

        if server.n_connected < 2:
            print("Number of players decresed. Quitting..")
            break

        current = time.time()

        new_inputs = server.get_inputs()
        for input_ in new_inputs[0]:
            if input_ not in inputs[0]:
                inputs[0].append(input_)
        for input_ in new_inputs[1]:
            if input_ not in inputs[1]:
                inputs[1].append(input_)

        if current - previous >= UPDATE_INTERVAL:
            pprint("Current inputs: " + str(inputs))
            update(game, inputs)
            server.send_game(game)
            previous = current
            inputs = [[], []]

    print("Finished.")

