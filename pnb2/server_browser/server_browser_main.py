# coding: utf-8
"""
"""
import threading
import time
import sys

from pnb2.networking.network import StatusRequestClient

from pnb2.server_browser.server_browser_ui import Ui_ServerBrowser

from pnb2.server_browser.create_server_dialog_main import CreateServerDialogMain
from pnb2.server_browser.add_server_dialog_main import AddServerDialogMain

from pnb2.networking.server import start_server
from pnb2.networking.client import start_client

from PyQt5.Qt import QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore


STATUS_UPDATE_INTERVAL = 10
TABLE_UPDATE_INTERVAL = 3
MESSAGING_INTERVAL = 1


class ServerBrowserMain(QtWidgets.QMainWindow):
    """
    """

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_ServerBrowser()
        self.ui.setupUi(self)

        self.servers = self.read_servers()
        self.update_table()

        self.quit = False

        t = threading.Thread(target=self.status_updater)
        t.daemon = True
        t.start()

        timer = QtCore.QTimer(self)
        timer.setInterval(TABLE_UPDATE_INTERVAL*1000)
        timer.timeout.connect(self.update_table)
        timer.start()

        timer = QtCore.QTimer(self)
        timer.setInterval(MESSAGING_INTERVAL*1000)
        timer.timeout.connect(self.messaging_timer)
        timer.start()
        self.could_not_connect = False


    def on_tableWidgetServers_currentItemChanged(self, item):
        """
        """
        # update basic info for now
        row_idx = self.ui.tableWidgetServers.currentRow()
        text = '\n'.join([
            'Name: ' + str(self.servers[row_idx]['name']),
            'Players: ' + str(self.servers[row_idx]['n_players']),
            'Type: ' + str(self.servers[row_idx]['game_type']),
            'Address: ' + str(self.servers[row_idx]['address']),
            'Port: ' + str(self.servers[row_idx]['port']),
            'Status: ' + str(self.servers[row_idx]['status']),
        ])
        self.ui.textEditServerInfo.setText(text)

    def on_actionQuit_triggered(self, checked=None):
        """
        """
        if checked is None:
            return

        self.close()

    def on_actionAbout_triggered(self, checked=None):
        """ 
        """
        if checked is None:
            return

        msg = QtWidgets.QMessageBox(self)
        msg.setText('For Finnish baseball (2020)')
        msg.setWindowTitle('PNB')
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.show()

    def on_pushButtonObserve_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        current_row = self.ui.tableWidgetServers.currentRow()
        if current_row == -1:
            return

        sel_server = self.servers[current_row]
        address = sel_server['address']
        port = sel_server['port']

        def callback(client_id):
            if not client_id:
                self.could_not_connect = True
           

        args = (address, port)
        kwargs = {
            'obs': True,
            'player': False,
            'callback': callback,
        }

        t = threading.Thread(target=start_client, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        dialog = AddServerDialogMain(self, self.add_server_callback)
        dialog.show()

    def on_pushButtonCreate_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        dialog = CreateServerDialogMain(self, self.create_server_callback)
        dialog.show()

    def on_pushButtonJoin_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        current_row = self.ui.tableWidgetServers.currentRow()
        if current_row == -1:
            return

        sel_server = self.servers[current_row]
        address = sel_server['address']
        port = sel_server['port']

        def callback(client_id):
            if not client_id:
                self.could_not_connect = True
            else:
                self.servers[current_row]['rejoin_key'] = client_id

        args = (address, port)
        kwargs = {
            'obs': True,
            'player': True,
            'rejoin_key': sel_server.get('rejoin_key'),
            'callback': callback,
        }

        t = threading.Thread(target=start_client, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
 

    def read_servers(self):
        """
        """
        servers = [
            {'name': 'Teeluola',
             'n_players': 0,
             'game_type': '4-4-1',
             'address': '0.0.0.0',
             'port': 5555,
             'status': 'down',
             'server_id': 100},
            {'name': 'Örkkien maa',
             'n_players': 0,
             'game_type': '2-2-1',
             'address': '0.0.0.0',
             'port': 5555,
             'status': 'down',
             'server_id': 101}
        ]
        return servers

    def update_table(self):
        """
        """
        print("Updating table...")
        self.ui.tableWidgetServers.setRowCount(len(self.servers))
        self.ui.tableWidgetServers.setColumnCount(6)
        self.ui.tableWidgetServers.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Name'))
        self.ui.tableWidgetServers.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Players'))
        self.ui.tableWidgetServers.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Game type'))
        self.ui.tableWidgetServers.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('Address'))
        self.ui.tableWidgetServers.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('Port'))
        self.ui.tableWidgetServers.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem('Status'))

        for idx, server in enumerate(self.servers):

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(idx))
            self.ui.tableWidgetServers.setVerticalHeaderItem(idx, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['name']))
            self.ui.tableWidgetServers.setItem(idx, 0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['n_players']))
            self.ui.tableWidgetServers.setItem(idx, 1, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['game_type']))
            self.ui.tableWidgetServers.setItem(idx, 2, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['address']))
            self.ui.tableWidgetServers.setItem(idx, 3, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['port']))
            self.ui.tableWidgetServers.setItem(idx, 4, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText(str(server['status']))
            self.ui.tableWidgetServers.setItem(idx, 5, item)

    def messaging_timer(self):
        if self.could_not_connect:
            self.could_not_connect = False
            msg = QtWidgets.QMessageBox(self)
            msg.setText('Could not connect to the server')
            msg.setWindowTitle('PNB')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.show()

    def create_server_callback(self, name, port, game_type):
        """
        """
        address = '0.0.0.0'

        def ready(server_id): 
            options = {}
            options['name'] = name
            options['game_type'] = game_type
            options['n_players'] = 0
            options['address'] = address
            options['port'] = port
            options['status'] = 'open'
            options['server_id'] = server_id
            self.servers.append(options)

        args = (address, port, name, game_type, ready)

        t = threading.Thread(target=start_server, args=args)
        t.daemon = True
        t.start()


    def add_server_callback(self, address, port):
        """
        """

        def callback(message_type, server_id, n_players, name, game_type):
            server = {}
            if message_type == 'SERVER_STATUS_RUNNING':
                server['status'] = 'running'
            elif message_type == 'SERVER_STATUS_PLAYER_MISSING':
                server['status'] = 'player_missing'
            elif message_type == 'SERVER_STATUS_OPEN':
                server['status'] = 'open'
            elif message_type == 'SERVER_STATUS_DOWN':
                return

            if server_id in [serv['server_id'] for serv in self.servers]:
                return

            server['n_players'] = n_players
            server['name'] = name
            server['game_type'] = game_type
            server['address'] = address
            server['port'] = port
            server['server_id'] = server_id

            self.servers.append(server)

        requester = StatusRequestClient(address=address, 
                                        port=port)
        requester.get_status(callback)

    def closeEvent(self, event):
        self.quit = True
        event.accept()

    def status_updater(self):
        """
        """
        def callback(message_type, server_id, n_players, name, game_type):
            for server in self.servers:
                if server['server_id'] == server_id:
                    if message_type == 'SERVER_STATUS_RUNNING':
                        server['status'] = 'running'
                    elif message_type == 'SERVER_STATUS_PLAYER_MISSING':
                        server['status'] = 'player_missing'
                    elif message_type == 'SERVER_STATUS_OPEN':
                        server['status'] = 'open'
                    elif message_type == 'SERVER_STATUS_DOWN':
                        server['status'] = 'down'

                    server['n_players'] = n_players
                    server['name'] = name
                    server['game_type'] = game_type

        while not self.quit:
            time.sleep(STATUS_UPDATE_INTERVAL)
            print("Updating servers..")

            for server in self.servers:
                requester = StatusRequestClient(address=server['address'], 
                                                port=server['port'])
                requester.get_status(callback)


def main():
    """
    """
    app = QtWidgets.QApplication(sys.argv)
    window = ServerBrowserMain(app)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
