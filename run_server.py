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

    ip_address = '127.0.0.1'
    if cli_args.ip_address:
        ip_address = cli_args.ip_address

    port = 5555
    if cli_args.port:
        port = cli_args.port

    print("Initializing game..")
    game = initialize_game()

    print("Searching for clients..")
    server = Server(ip_address=ip_address, port=port)

    import pdb; pdb.set_trace()
    print("n_clients etc not implemented so stop here")

    print("Starting the main loop..")
    previous = time.time()
    inputs = [[] for idx in range(n_clients)]
    while True:

        if server.n_connected < n_clients:
            print("Number of players decresed. Quitting..")
            break

        current = time.time()

        new_inputs = server.get_inputs()
        for idx in range(n_clients):
            for input_ in new_inputs[idx]:
                if input_ not in inputs[idx]:
                    inputs[idx].append(input_)

        if current - previous >= UPDATE_INTERVAL:
            pprint("Current inputs: " + str(inputs))
            update(game, inputs)
            server.send_game(game)
            previous = current
            inputs = [[] for idx in range(n_clients)]

    print("Finished.")

