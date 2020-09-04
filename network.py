""" Handles socket messaging for Client and Server
"""
import socket
import json
import string
import secrets
import time

from _thread import * 


from constants import SOCKET_MESSAGE_LENGTH
from constants import JOIN_TIMEOUT
from constants import ID_SUFFIX_LENGTH
from constants import N_PLAYER_CLIENTS_NEEDED


class Server:
    """ Handles server side socket connections
    """
    def __init__(self, ip_address='127.0.0.1', port=5555):
        """
        """
        self.clients = {}

        self.n_player_clients = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.sock = sock
            sock.bind((ip_address, port))
            sock.listen()

            print("Waiting for connections, server started..")

            def threaded_client(conn, client_idx):
                """
                """
                client_state = {'conn': conn, 'type': None, 'messages': []}

                buffer_ = ""
                beginning = time.time()
                done = False
                while not done:

                    if time.time() - beginning > JOIN_TIMEOUT:
                        print("Closed connection to " + str(client_idx))
                        conn.close()

                    try:
                        buffer_, messages = self.read_messages(conn, buffer_, client_idx)
                        for message in messages:
                            message_dict = json.loads(message)
                            if message_dict['type'] == 'PLAYER_JOIN':
                                if self.n_player_clients < N_PLAYER_CLIENTS_NEEDED:
                                    client_state['type'] = 'player'
                                    secure_str = ''.join((secrets.choice(string.ascii_letters) 
                                                          for i in range(ID_SUFFIX_LENGTH)))
                                    id_ = str(client_idx) + '#' + secure_str
                                    message_dict = {'type': 'PLAYER_JOIN_APPROVED',
                                                    'value': id_}
                                    conn.send(json.dumps(message_dict).encode('UTF-8') + 
                                              '$'.encode('utf-8'))
                                    self.n_player_clients += 1
                                    done = True
                                else:
                                    message_dict = {'type': 'PLAYER_JOIN_DECLINED'}
                                    conn.send(json.dumps(message_dict).encode('UTF-8') + 
                                              '$'.encode('utf-8'))
                                    conn.close()
                                    return

                            elif message_dict['type'] == 'GRAPHICS_JOIN':
                                client_state['type'] = 'graphics'
                                secure_str = ''.join((secrets.choice(string.ascii_letters) 
                                                      for i in range(ID_SUFFIX_LENGTH)))
                                id_ = 'x#' + secure_str
                                message_dict = {'type': 'GRAPHICS_JOIN_APPROVED',
                                                'value': id_}
                                conn.send(json.dumps(message_dict).encode('UTF-8') + 
                                          '$'.encode('utf-8'))
                                done = True

                    except Exception as exc:
                        print(str(exc))
                        break

                self.clients[client_idx] = client_state

                while True:
                    try:
                        buffer_, messages = self.read_messages(conn, buffer_, client_idx)
                        self.clients[client_idx]['messages'].extend(messages)
                    except Exception as exc:
                        print(str(exc))
                        break

                print("Lost connection to " + str(client_idx))
                conn.close()

            # Establish connections two players and then continue
            n_connected = 0
            while self.n_player_clients < N_PLAYER_CLIENTS_NEEDED:
                conn, addr = sock.accept()
                print("Connected to: " + str(addr))

                start_new_thread(threaded_client, (conn, n_connected))

                while True:
                    state = self.clients.get(n_connected)
                    if state and state.get('type') == 'player':
                        break

                n_connected += 1

    def read_messages(self, conn, buffer_, client_idx):
        message = conn.recv(SOCKET_MESSAGE_LENGTH)
        buffer_ = buffer_ + message.decode('utf-8')

        if not message:
            raise Exception("Disconnected by " + str(client_idx))
        else:
            parts = []
            # $ is used as a message separator
            while '$' in buffer_:
                idx = buffer_.index('$')
                parts.append(buffer_[:idx])
                buffer_ = buffer_[idx+1:]

        return buffer_, parts

    def send_game(self, game):
        """ Send "official" game from server to clients
        """
        message_dict = {'type': 'GAME',
                        'value': game}

        for client in self.clients:
            try:
                # Use $ as message separator
                client['conn'].send(json.dumps(message_dict).encode('UTF-8') + 
                                   '$'.encode('utf-8'))
            except OSError:
                continue

    def get_inputs(self):
        """ Get inputs from clients to server
        """
        inputs = []
        return inputs

        # # # MUST CHANGE THIS TO READ THE ID
        
        for idx in range(self.n_clients):
            player_inputs = []
            kept_messages = []
            for message in self.messages[idx]:
                message_dict = json.loads(message)
                if message_dict['type'] == 'INPUTS':
                    for val in message_dict['value']:
                        if val not in player_inputs:
                            player_inputs.append(val)
                else:
                    kept_messages.append(message)
            self.messages[idx] = kept_messages
            inputs.append(player_inputs)

        return inputs


class Client:
    """ Handles client side socket connections
    """

    def __init__(self, ip_address, port):
        """
        """
        self.messages = []
        self.client_id = None
        self.sock = None
        self.connection_alive = False

        def threaded_connection():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                self.sock = sock
                sock.connect((ip_address, port))

                self.connection_alive = True

                buffer_ = ""
                while True:
                    try:
                        message = sock.recv(SOCKET_MESSAGE_LENGTH)
                        buffer_ = buffer_ + message.decode('utf-8')

                        if not message:
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
        while True:
            if not self.sock:
                continue
            self.join_game()
            return self

    def join_game(self):
        """
        """

    def get_game(self):
        """ Get upstream game from server to client side
        """
        game = None
        kept_messages = []
        for message in self.messages:
            message_dict = json.loads(message)
            if message_dict['type'] == 'GAME':
                game = message_dict['value']
            else:
                kept_messages.append(message)
        self.messages = kept_messages

        return game


class PlayerClient(Client):
    """ Handles server side socket connections for player client
    """

    def __init__(self, ip_address='127.0.0.1', port=5555):
        """
        """
        Client.__init__(self, ip_address, port)


    def join_game(self):
        """
        """
        message_dict = {'type': 'PLAYER_JOIN'}
        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            raise Exception('Could not send PLAYER_JOIN message to the server')

        done = False
        while not done:
            kept_messages = []
            for message in self.messages:
                message_dict = json.loads(message)
                if message_dict['type'] == 'PLAYER_JOIN_APPROVED':
                    self.client_id = message_dict['value']
                    done = True
                elif message_dict['type'] == 'PLAYER_JOIN_DECLINED':
                    raise Exception('PLAYER_JOIN DECLINED BY SERVER')
                else:
                    kept_messages.append(message)
            self.messages = kept_messages


    def send_inputs(self, inputs):
        """ Send inputs from client to server side
        """
        message_dict = {'type': 'INPUTS',
                        'value': inputs}

        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            pass


class GraphicsClient(Client):
    """ Handles server side connections for graphics client
    """
    def __init__(self, ip_address='127.0.0.1', port=5555):
        """
        """
        Client.__init__(self, ip_address, port)

    def join_game(self):
        """
        """
        message_dict = {'type': 'GRAPHICS_JOIN'}
        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            raise Exception('Could not send GRAPHICS_JOIN message to the server')

        done = False
        while not done:
            kept_messages = []
            for message in self.messages:
                message_dict = json.loads(message)
                if message_dict['type'] == 'GRAPHICS_JOIN_APPROVED':
                    self.client_id = message_dict['value']
                    done = True
                elif message_dict['type'] == 'GRAPHICS_JOIN_DECLINED':
                    raise Exception('GRAPHICS_JOIN DECLINED BY SERVER')
                else:
                    kept_messages.append(message)
            self.messages = kept_messages

