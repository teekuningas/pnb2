""" Handles socket messaging for Client and Server
"""
import socket
import json

from _thread import * 

from pprint import pprint

from constants import SOCKET_MESSAGE_LENGTH


class Server:
    """ Handles server side socket connections
    """
    def __init__(self, ip_address='127.0.0.1', port=5555, n_clients=2):
        """
        """
        self.messages = [[] for idx in range(n_clients)]
        self.clients = []
        self.n_clients = n_clients

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.sock = sock
            sock.bind((ip_address, port))
            sock.listen()

            print("Waiting for a connection, server started..")

            def threaded_client(conn, client_idx):
                """
                """
                message_dict = {'type': 'conn_established',
                                'value': client_idx}
                conn.send(json.dumps(message_dict).encode('UTF-8') + 
                          '$'.encode('utf-8'))

                self.clients.append(conn)

                # read to buffer to avoid problems from messages splitting
                buffer_ = ""
                while True:
                    try:
                        reply = conn.recv(SOCKET_MESSAGE_LENGTH)
                        buffer_ = buffer_ + reply.decode('utf-8')

                        if not reply:
                            print("Disconnected by " + str(client_idx))
                            break
                        else:
                            parts = []

                            # $ is used as a message separator
                            while '$' in buffer_:
                                idx = buffer_.index('$')
                                parts.append(buffer_[:idx])
                                buffer_ = buffer_[idx+1:]

                            self.messages[client_idx].extend(parts)

                    except Exception as exc:
                        print(str(exc))
                        break

                print("Lost connection to " + str(client_idx))
                self.n_connected -= 1
                conn.close()

            self.n_connected = 0

            # Establish connections two players and then continue
            while self.n_connected < self.n_clients:
                conn, addr = sock.accept()
                print("Connected to: " + str(addr))

                start_new_thread(threaded_client, (conn, self.n_connected))
                self.n_connected += 1

    def send_game(self, game):
        """ Send "official" game from server to clients
        """
        message_dict = {'type': 'game',
                        'value': game}

        for conn in self.clients:
            try:
                # Use $ as message separator
                conn.send(json.dumps(message_dict).encode('UTF-8') + 
                          '$'.encode('utf-8'))
            except OSError:
                continue

    def get_inputs(self):
        """ Get inputs from clients to server
        """
        inputs = []
        
        for idx in range(self.n_clients):
            player_inputs = []
            kept_messages = []
            for message in self.messages[idx]:
                message_dict = json.loads(message)
                if message_dict['type'] == 'inputs':
                    for val in message_dict['value']:
                        if val not in player_inputs:
                            player_inputs.append(val)
                else:
                    kept_messages.append(message)
            self.messages[idx] = kept_messages
            inputs.append(player_inputs)

        return inputs


class Client:
    """ Handles server side socket connections
    """

    def __init__(self, ip_address='127.0.0.1', port=5555):
        """
        """
        self.messages = []
        self.connection_alive = False

        def threaded_connection():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                self.sock = sock
                sock.connect((ip_address, port))
                self.connection_alive = True

                buffer_ = ""
                while True:
                    try:
                        reply = sock.recv(SOCKET_MESSAGE_LENGTH)
                        buffer_ = buffer_ + reply.decode('utf-8')

                        if not reply:
                            print("Disconnected.")
                            break
                        else:
                            parts = []

                            while '$' in buffer_:
                                idx = buffer_.index('$')
                                parts.append(buffer_[:idx])
                                buffer_ = buffer_[idx+1:]

                            self.messages.extend(parts)

                    except Exception as exc:
                        print(str(exc))
                        break

                self.connection_alive = False
                print("Lost connection to server.")

        # Run client-side socket messaging in thread
        start_new_thread(threaded_connection, ())


    def send_inputs(self, inputs):
        """ Send inputs from client to server side
        """
        message_dict = {'type': 'inputs',
                        'value': inputs}

        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            pass

    def get_game(self):
        """ Get upstream game from server to client side
        """
        game = None
        kept_messages = []
        for message in self.messages:
            message_dict = json.loads(message)
            if message_dict['type'] == 'game':
                game = message_dict['value']
            else:
                kept_messages.append(message)
        self.messages = kept_messages

        return game

    def get_client_idx(self):
        """ Get player idx from server
        """
        client_idx = None
        kept_messages = []
        for message in self.messages:
            message_dict = json.loads(message)
            if message_dict['type'] == 'conn_established':
                client_idx = message_dict['value']
            else:
                kept_messages.append(message)

        self.messages = kept_messages

        return client_idx

