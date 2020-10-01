""" Contains basic way to run server side game loop
"""
import argparse
import time

from pprint import pprint

from pnb2.networking.network import Server

from pnb2.game.game import initialize_game
from pnb2.game.game import update

from pnb2.game.constants import UPDATE_INTERVAL


N_PLAYER_CLIENTS_NEEDED = 2


def start_server(address, port, server_id_callback=None):
    """
    """
    address = address or '0.0.0.0'
    port = port or 5555

    print("Initializing game..")
    game = initialize_game()

    print("Searching for clients..")
    server = Server(address=address, port=port)

    if server_id_callback:
        server_id_callback(server.server_id)

    server.wait_for_players()

    print("Starting the main loop..")
    previous = time.time()
    inputs = [[] for idx in range(N_PLAYER_CLIENTS_NEEDED)]
    while True:

        server.handle_disconnections()

        current = time.time()

        # pile up inputs
        new_inputs = server.get_inputs()
        for idx in range(N_PLAYER_CLIENTS_NEEDED):
            for input_ in new_inputs[idx]:
                if input_ not in inputs[idx]:
                    inputs[idx].append(input_)

        # and if enough time has passed, update game state
        if current - previous >= UPDATE_INTERVAL:
            update(game, inputs)
            server.send_game(game)
            previous = current
            # start piling up new round of inputs
            inputs = [[] for idx in range(N_PLAYER_CLIENTS_NEEDED)]

    print("Finished.")


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--address')
    parser.add_argument('--port')

    cli_args = parser.parse_args()
    start_server(cli_args.address, cli_args.port)

