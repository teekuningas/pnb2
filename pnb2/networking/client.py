""" Contains basic way to run client side game loop
"""

import argparse
import time

from pnb2.networking.network import PlayerClient
from pnb2.networking.network import ObservationClient
from pnb2.game.input_ import initialize as input_initialize
from pnb2.game.graphics import initialize as gfx_initialize
from pnb2.game.graphics import render
from pnb2.game.game import update
from pnb2.game.constants import UPDATE_INTERVAL

N_PLAYER_CLIENTS_NEEDED = 2


def start_client(address, port, obs=True, player=True, bind_key=None, rejoin_key=None, callback=None):
    """
    """
    try:
        address = address or '0.0.0.0'
        port = port or 5555

        bind_key = bind_key or 'keyboard_right'
        rejoin_key = rejoin_key or None

        input_engine = None
        gfx_engine = None

        try:
            if obs and not player:
                client = ObservationClient(address, port)
            elif obs and player:
                client = PlayerClient(address, port, rejoin_key=rejoin_key)
            elif not obs and player:
                client = PlayerClient(address, port, rejoin_key=rejoin_key)
            else:
                raise Exception('Must be player or obs client')
        except Exception as exc:
            if callback:
                callback(None)
            raise exc

        print('Client ID (use on rejoin): ' + str(client.client_id))

        if callback:
            callback(client.client_id)

        if not client.client_id:
            raise Exception('Could not connect')

        player_idx = client.client_id.split('#')[0]

        # Get initial copy of the game state
        while True:
            game = client.get_game()
            if game:
                break

        if obs:
            gfx_engine = gfx_initialize()

        if player:
            input_engine = input_initialize()

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

                if player:
                    new_inputs = input_engine.get_inputs(bind_key)
                    client.send_inputs(new_inputs)

                new_game = client.get_game()
                if new_game:
                    # if game available from server, use it
                    game = new_game
                else:
                    # else, predict.. 
                    if not player:
                        update(game)
                    else:
                        update(game, [new_inputs if idx==player_idx else [] 
                                      for idx in range(N_PLAYER_CLIENTS_NEEDED)])

                lag -= UPDATE_INTERVAL

            if obs:
                render(gfx_engine, game, lag / UPDATE_INTERVAL)

    except Exception as exc:
        print(str(exc))
        if client:
            client.shutdown()
        if player and input_engine:
            input_engine.shutdown()
        print("Finishing gracefully.")


if __name__ == '__main__':
    """
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--address')
    parser.add_argument('--port')
    parser.add_argument('--bind_key')
    parser.add_argument('--rejoin_key')

    parser.add_argument('--obs', dest='obs', action='store_true')
    parser.add_argument('--no-obs', dest='obs', action='store_false')
    parser.set_defaults(obs=True)

    parser.add_argument('--player', dest='player', action='store_true')
    parser.add_argument('--no-player', dest='player', action='store_false')
    parser.set_defaults(player=True)

    cli_args = parser.parse_args()

    start_client(cli_args.address, cli_args.port, cli_args.obs,
                 cli_args.player, cli_args.bind_key, cli_args.rejoin_key)
