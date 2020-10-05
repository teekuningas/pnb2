""" Contains basic way to run server side game loop
"""
import argparse
import time

from pprint import pprint

from pnb2.networking.network import Server

from pnb2.game.game import initialize_game
from pnb2.game.game import update

from pnb2.game.constants import UPDATE_INTERVAL


def start_server(address, port, name, game_type, server_id_callback=None):
    """
    """
    try:
        address = address or '0.0.0.0'
        port = port or 5555
        name = name or 'Default'
        game_type = game_type or '2-2-1'

        server = None

        print("Initializing game..")
        game = initialize_game()

        print("Searching for clients..")
        server = Server(address=address, port=port, name=name, game_type=game_type)

        if server_id_callback:
            server_id_callback(server.server_id)

        server.wait_for_players()

        print("Starting the main loop..")
        previous = time.time()
        while True:

            server.handle_disconnections()

            current = time.time()

            # and if enough time has passed, update game state
            if current - previous >= UPDATE_INTERVAL:

                inputs = server.get_inputs()
                update(game, inputs)
                server.send_game(game)

                previous = current

    except Exception as exc:
        print(str(exc))
        if server:
            server.shutdown()
        
    print("Finished gracefully.")


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--address')
    parser.add_argument('--port')
    parser.add_argument('--name')
    parser.add_argument('--game_type')

    cli_args = parser.parse_args()
    start_server(cli_args.address, cli_args.port, cli_args.name, cli_args.game_type)

