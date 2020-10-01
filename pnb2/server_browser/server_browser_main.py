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

from PyQt5.Qt import QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtCore


STATUS_UPDATE_INTERVAL = 15
TABLE_UPDATE_INTERVAL = 3


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
        t.start()

        timer = QtCore.QTimer(self)
        timer.setInterval(TABLE_UPDATE_INTERVAL*1000)
        timer.timeout.connect(self.update_table)
        timer.start()

    def on_tableWidgetServers_currentItemChanged(self, item):
        """
        """
        # update basic info for now
        row_idx = self.ui.tableWidgetServers.currentRow()
        text = '\n'.join([
            'Name: ' + str(self.servers[row_idx]['name']),
            'Players: ' + str(self.servers[row_idx]['n_players']),
            'Type: ' + str(self.servers[row_idx]['type']),
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

        print("About clicked")

    def on_pushButtonObserve_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        print("Observe clicked")

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        dialog = AddServerDialogMain(self)
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

        print("Join clicked")

    def read_servers(self):
        """
        """
        servers = [
            {'name': 'Teeluola',
             'n_players': 0,
             'type': '4-4-1',
             'address': '0.0.0.0',
             'port': 5555,
             'status': 'down',
             'server_id': 100},
            {'name': 'Örkkien maa',
             'n_players': 1,
             'type': '2-2-1',
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
        self.ui.tableWidgetServers.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Type'))
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
            item.setText(str(server['type']))
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


    def create_server_callback(self, options):
        """
        """
        self.servers.append(options)

    def closeEvent(self, event):
        self.quit = True
        event.accept()

    def status_updater(self):
        """
        """
        def callback(type_, server_id):
            for server in self.servers:
                if server['server_id'] == server_id:
                    if type_ == 'SERVER_STATUS_RUNNING':
                        server['status'] = 'running'
                    elif type_ == 'SERVER_STATUS_PLAYER_MISSING':
                        server['status'] = 'player_missing'
                    elif type_ == 'SERVER_STATUS_OPEN':
                        server['status'] = 'open'
                    elif type_ == 'SERVER_STATUS_DOWN':
                        server['status'] = 'down'
                    print("Getting info " + str(type_) + ", " + str(server_id))

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
