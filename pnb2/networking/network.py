""" Handles socket messaging for Client and Server
"""
import socket
import select
import json
import string
import secrets
import time
import sys

import threading


SOCKET_MESSAGE_LENGTH = 2048
IS_ALIVE_TIMEOUT = 5
ID_SUFFIX_LENGTH = 10
N_PLAYER_CLIENTS_NEEDED = 2


def recv_with_timeout(conn):
    """ recv that will timeout after 1s """
    conn.setblocking(0)
    ready = select.select([conn], [], [], 1)
    if ready[0]:
        return conn.recv(SOCKET_MESSAGE_LENGTH)
    return "".encode('utf-8')


class Server:
    """ Handles server side socket connections
    """
    def __init__(self, address='0.0.0.0', port=5555, name='Default', game_type='2-2-1'):
        """
        """
        self.quit = False

        self.server_id = ''.join((secrets.choice(string.ascii_letters) 
                                 for i in range(ID_SUFFIX_LENGTH)))

        self.name = name
        self.game_type = game_type

        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((address, port))
        self.sock.listen()

        print("Waiting for connections, server started..")

        t = threading.Thread(target=self.look_for_clients)
        t.start()

    def wait_for_players(self):
        while True:
            if self.n_player_clients_connected() == N_PLAYER_CLIENTS_NEEDED:
                break

    def shutdown(self):
        print("Shutdown called for server")
        self.quit = True

    def threaded_client(self, conn, client_idx):
        """
        """
        client_state = {'conn': conn, 
                        'type': None, 
                        'id': None, 
                        'messages': [],
                        'messages_lock': threading.Lock(),
                        'connected': True, 
                        'initialized': False,
                        'active': True,
                        'is_alive_sent': False}
        self.clients[client_idx] = client_state

        # start communication
        buffer_ = ""
        previous_message_time = time.time()
        while True:
            try:
                buffer_, messages = self.read_messages(conn, buffer_, client_idx)

                # query client if still alive
                current_time = time.time()
                if current_time - previous_message_time > IS_ALIVE_TIMEOUT:
                    previous_message_time = current_time
                    
                    if not client_state['initialized']:
                        raise Exception('Connection not initialized in time')

                    if client_state['is_alive_sent']:
                        raise Exception('Connection closed as is_alive message not answered')
                    else:
                        message_dict = {'type': 'PLAYER_IS_ALIVE_REQUEST'}
                        conn.send(json.dumps(message_dict).encode('UTF-8') + 
                                  '$'.encode('utf-8'))
                        client_state['is_alive_sent'] = True

                if messages:
                    previous_message_time = time.time()

                    self.clients[client_idx]['messages_lock'].acquire()
                    self.clients[client_idx]['messages'].extend(messages)
                    self.clients[client_idx]['messages_lock'].release()

                    self.handle_negotiation(client_idx, messages)

                if self.quit:
                    raise Exception('Quit initiated by parent')

            except Exception as exc:
                print("Server: " + str(exc))
                print("Lost connection to " + str(client_idx))
                client_state['connected'] = False
                client_state['initialized'] = True
                conn.close()
                return

    def handle_negotiation(self, client_idx, messages):
        client_state = self.clients[client_idx]
        conn = client_state['conn']

        for message in messages:
            message_dict = json.loads(message)

            # on IS_ALIVE answer
            if message_dict.get('type', '') == 'PLAYER_IS_ALIVE_ANSWER':
                client_state['is_alive_sent'] = False

            # on STATUS_REQUEST
            if message_dict.get('type', '') == 'SERVER_STATUS_REQUEST':
                answer_dict = {}
                answer_dict['server_id'] = self.server_id
                answer_dict['n_players'] = self.n_player_clients_connected()
                answer_dict['name'] = self.name
                answer_dict['game_type'] = self.game_type

                if self.n_player_clients_connected() == N_PLAYER_CLIENTS_NEEDED:
                    answer_dict['type'] = 'SERVER_STATUS_RUNNING'
                elif self.n_player_clients_joined() == N_PLAYER_CLIENTS_NEEDED:
                    answer_dict['type'] = 'SERVER_STATUS_PLAYER_MISSING'
                else:
                    answer_dict['type'] = 'SERVER_STATUS_OPEN'

                conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                          '$'.encode('utf-8'))

                raise Exception('SERVER_STATUS_REQUEST answered, quitting.')

            # on PLAYER_JOIN
            if message_dict.get('type', '') == 'PLAYER_JOIN':
                player_idx = self.n_player_clients_joined()
                if player_idx < N_PLAYER_CLIENTS_NEEDED:
                    secure_str = ''.join((secrets.choice(string.ascii_letters) 
                                          for i in range(ID_SUFFIX_LENGTH)))
                    id_ = str(player_idx) + '#' + secure_str

                    client_state['type'] = 'player'
                    client_state['id'] = id_

                    answer_dict = {'type': 'PLAYER_JOIN_APPROVED',
                                   'value': id_}
                    conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                              '$'.encode('utf-8'))
                    client_state['initialized'] = True

                else:
                    answer_dict = {'type': 'PLAYER_JOIN_DECLINED'}
                    conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                              '$'.encode('utf-8'))

                    raise Exception('PLAYER_JOIN_DECLINED sent, quitting.')

            # on PLAYER_REJOIN
            elif message_dict.get('type', '') == 'PLAYER_REJOIN':
                rejoin_key = message_dict.get('value', '')

                # check if valid old client state exists and mark it as inactive
                found = False
                for idx, state in self.clients.items():
                    if state.get('type') == 'player' and state.get('active') == True:
                        if state.get('connected') == False:
                            if state.get('id') == rejoin_key:
                                state['active'] = False
                                found = True
                if found:
                    client_state['type'] = 'player'
                    client_state['id'] = rejoin_key

                    answer_dict = {'type': 'PLAYER_REJOIN_APPROVED',
                                    'value': rejoin_key}
                    conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                              '$'.encode('utf-8'))
                    client_state['initialized'] = True
                else:
                    answer_dict = {'type': 'PLAYER_REJOIN_DECLINED'}
                    conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                              '$'.encode('utf-8'))

                    raise Exception('PLAYER_REJOIN_DECLINED sent, quitting.')

            # on OBSERVATION_JOIN
            elif message_dict.get('type', '') == 'OBSERVATION_JOIN':
                secure_str = ''.join((secrets.choice(string.ascii_letters) 
                                      for i in range(ID_SUFFIX_LENGTH)))
                id_ = 'x#' + secure_str

                client_state['type'] = 'observation'
                client_state['id'] = id_

                answer_dict = {'type': 'OBSERVATION_JOIN_APPROVED',
                               'value': id_}
                conn.send(json.dumps(answer_dict).encode('UTF-8') + 
                          '$'.encode('utf-8'))

                client_state['initialized'] = True


    def look_for_clients(self):
        """ Actively, in a thread, look for new clients
        """
        while True:
            # this might respond with delay as sock.accept blocks..
            if self.quit:
                return

            conn, addr = self.sock.accept()
            print("Negotiating with: " + str(addr))

            keys = list(self.clients.keys())
            if keys:
                client_idx = max(self.clients.keys()) + 1
            else:
                client_idx = 0

            t = threading.Thread(target=self.threaded_client, args=(conn, client_idx))
            t.start()

            # start processing next client only after the current has 
            # been marked as initialized
            while True:
                if client_idx in self.clients:
                    if self.clients[client_idx].get('initialized'):
                        break

    def n_player_clients_connected(self):
        """ How many player clients connected 
        """
        count = 0
        for state in list(self.clients.values()):
            if state.get('type', '') == 'player':
                if state.get('connected') == True:
                    count += 1
        return count


    def n_player_clients_joined(self):
        """ How many players have been connected
        """
        count = 0
        for state in list(self.clients.values()):
            if state.get('type', '') == 'player':
                count += 1
        return count

    def handle_disconnections(self):
        """ Check for disconnections and if disconnection detected,
        inform all clients and block until the same player has joined back
        """

        # check if any player has disconnected
        disconnections = False
        for state in list(self.clients.values()):
            if state.get('type') == 'player' and state.get('active') == True:
                if state.get('connected') == False:
                    disconnections = True
                    break

        if not disconnections:
            return

        print("Player has disconnected.. Taking a break..")

        # if yes, send message of break to every client
        message_dict = {'type': 'DISCONNECTION_BREAK'}
        for state in list(self.clients.values()):
            if state.get('connected') == True:
                state['conn'].send(
                    json.dumps(message_dict).encode('UTF-8') + 
                    '$'.encode('utf-8'))

        while True:
            if self.quit:
                return

            if self.n_player_clients_connected() == N_PLAYER_CLIENTS_NEEDED:
                break

        print("Player has rejoined.. Continuing.")

    def read_messages(self, conn, buffer_, client_idx):
        """
        """
        message = recv_with_timeout(conn)

        parts = []
        if message:
            buffer_ = buffer_ + message.decode('utf-8')
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

        for state in list(self.clients.values()):
            try:
                # Use $ as message separator
                state['conn'].send(json.dumps(message_dict).encode('UTF-8') + 
                                   '$'.encode('utf-8'))
            except OSError:
                continue

    def get_inputs(self):
        """ Get inputs from clients to server
        """
        inputs = [[] for idx in range(N_PLAYER_CLIENTS_NEEDED)]
        
        for state in list(self.clients.values()):
            if state.get('type') == 'player' and state.get('connected'):
                player_inputs = []

                input_idx = int(state.get('id').split('#')[0])

                state['messages_lock'].acquire()
                for message_idx, message in enumerate(state['messages']):
                    message_dict = json.loads(message)

                    if message_dict['type'] == 'INPUTS':
                        state['messages'].pop(message_idx)
                        for val in message_dict['value']:
                            if val not in player_inputs:
                                player_inputs.append(val)
                state['messages_lock'].release()
                inputs[input_idx] = player_inputs
        return inputs


class Client:
    """ Handles client side socket connections
    """

    def __init__(self, address, port):
        """
        """
        self.messages = []
        self.messages_lock = threading.Lock()
        self.client_id = None
        self.sock = None
        self.connection_alive = False
        self.quit = False

        def threaded_connection():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    self.sock = sock
                    sock.connect((address, port))

                    self.connection_alive = True

                    buffer_ = ""
                    while True:

                        if self.quit:
                            sock.close()
                            print("Quit initiated by parent")
                            return

                        message = sock.recv(SOCKET_MESSAGE_LENGTH)
                        buffer_ = buffer_ + message.decode('utf-8')

                        if not message:
                            print("Disconnected.")
                            sock.close()
                            break
                        else:
                            parts = []

                            while '$' in buffer_:
                                idx = buffer_.index('$')
                                parts.append(buffer_[:idx])
                                buffer_ = buffer_[idx+1:]

                            if parts:
                                self.messages_lock.acquire()
                                self.messages.extend(parts)
                                self.messages_lock.release()

                                self.handle_is_alive(parts)

            except Exception as exc:
                sock.close()
                print("Client: " + str(exc))

            self.connection_alive = False
            print("Lost connection to server.")

        # Run client-side socket messaging in thread

        t = threading.Thread(target=threaded_connection)
        t.start()


    def shutdown(self):
        print("Shutdown called for client")
        self.quit = True

    def handle_is_alive(self, messages):
        for message in messages:
            message_dict = json.loads(message)
            if message_dict['type'] == 'PLAYER_IS_ALIVE_REQUEST':
                answer_dict = {'type': 'PLAYER_IS_ALIVE_ANSWER'}
                # Use $ as a message separator
                self.sock.send(json.dumps(answer_dict).encode('UTF-8') + 
                               '$'.encode('utf-8'))
                break

    def get_game(self):
        """ Get upstream game from server to client side
        """
        game = None

        self.messages_lock.acquire()
        for message_idx, message in enumerate(self.messages):
            message_dict = json.loads(message)
            if message_dict['type'] == 'GAME':
                self.messages.pop(message_idx)
                game = message_dict['value']
        self.messages_lock.release()

        return game


class StatusRequestClient(Client):
    """ Handles status requests
    """

    def get_status(self, callback):
        beginning = time.time()
        request_sent = False
        while True:
            if not request_sent:
                if self.connection_alive:
                    answer_dict = {'type': 'SERVER_STATUS_REQUEST'}
                    self.sock.send(json.dumps(answer_dict).encode('UTF-8') + 
                                   '$'.encode('utf-8'))
                    request_sent = True

            if time.time() - beginning > IS_ALIVE_TIMEOUT:
                callback('SERVER_STATUS_DOWN', None, None, None, None)
                return

            if not self.messages:
                continue

            for message in self.messages:
                message_dict = json.loads(message)
                if 'SERVER_STATUS' in message_dict['type']:
                    type_ = message_dict['type']
                    server_id = message_dict['server_id']
                    n_players = message_dict['n_players']
                    name = message_dict['name']
                    game_type = message_dict['game_type']
                    callback(type_, server_id, n_players, name, game_type)
                    return
 

class PlayerClient(Client):
    """ Handles server side socket connections for player client
    """

    def __init__(self, address='0.0.0.0', port=5555, rejoin_key=None):
        """
        """
        Client.__init__(self, address, port)

        beginning = time.time()
        while True:
            if time.time() - beginning > IS_ALIVE_TIMEOUT:
                print("Could not connect to the server")
                self.shutdown()
                return

            if not self.connection_alive:
                continue

            try:
                self.join_game(rejoin_key)
            except Exception as exc:
                print(str(exc))
                self.shutdown()
                return

            return

    def join_game(self, rejoin_key=None):
        """
        """
        if rejoin_key:
            message_dict = {'type': 'PLAYER_REJOIN',
                            'value': rejoin_key}
        else:
            message_dict = {'type': 'PLAYER_JOIN'}

        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            if rejoin_key:
                raise Exception('Could not send PLAYER_REJOIN message to the server')
            else:
                raise Exception('Could not send PLAYER_JOIN message to the server')

        done = False
        beginning = time.time()
        while not done:
            if time.time() - beginning > IS_ALIVE_TIMEOUT:
                raise Exception('Could not connect to the server.')

            self.messages_lock.acquire()
            for message_idx, message in enumerate(self.messages):
                message_dict = json.loads(message)
                if message_dict['type'] == 'PLAYER_REJOIN_APPROVED':
                    self.messages.pop(message_idx)
                    self.client_id = message_dict['value']
                    done = True
                elif message_dict['type'] == 'PLAYER_REJOIN_DECLINED':
                    self.messages.pop(message_idx)
                    raise Exception('PLAYER_REJOIN DECLINED BY SERVER')
                elif message_dict['type'] == 'PLAYER_JOIN_APPROVED':
                    self.messages.pop(message_idx)
                    self.client_id = message_dict['value']
                    done = True
                elif message_dict['type'] == 'PLAYER_JOIN_DECLINED':
                    self.messages.pop(message_idx)
                    raise Exception('PLAYER_JOIN DECLINED BY SERVER')
            self.messages_lock.release()

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


class ObservationClient(Client):
    """ Handles server side connections for observation client
    """
    def __init__(self, address='0.0.0.0', port=5555):
        """
        """
        Client.__init__(self, address, port)

        beginning = time.time()
        while True:
            if time.time() - beginning > IS_ALIVE_TIMEOUT:
                raise Exception('Could not connect to the server.')

            if not self.connection_alive:
                continue

            try:
                self.join_game()
            except Exception as exc:
                print(str(exc))
                self.shutdown()
                return

            return

    def join_game(self, rejoin_key=None):
        """
        """
        message_dict = {'type': 'OBSERVATION_JOIN'}
        try:
            # Use $ as a message separator
            self.sock.send(json.dumps(message_dict).encode('UTF-8') + 
                           '$'.encode('utf-8'))
        except OSError:
            raise Exception('Could not send OBSERVATION_JOIN message to the server')

        done = False
        beginning = time.time()
        while not done:
            if time.time() - beginning > IS_ALIVE_TIMEOUT:
                raise Exception('Could not connect to the server.')

            self.messages_lock.acquire()
            for message_idx, message in enumerate(self.messages):
                message_dict = json.loads(message)
                if message_dict['type'] == 'OBSERVATION_JOIN_APPROVED':
                    self.messages.pop(message_idx)
                    self.client_id = message_dict['value']
                    done = True
                elif message_dict['type'] == 'OBSERVATION_JOIN_DECLINED':
                    raise Exception('OBSERVATION_JOIN DECLINED BY SERVER')
            self.messages_lock.release()

