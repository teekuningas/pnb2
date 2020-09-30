# coding: utf-8
import sys

"""
"""
from server_browser_ui import Ui_ServerBrowser

from PyQt5.Qt import QApplication
from PyQt5 import QtWidgets


def set_trace():
    from PyQt5.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()
    import pdb; pdb.set_trace()


class ServerBrowserMain(QtWidgets.QMainWindow):
    """
    """

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_ServerBrowser()
        self.ui.setupUi(self)

        self.servers = self.read_servers()
        self.update_table()

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

        print("Add clicked")

    def on_pushButtonCreate_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        print("Create clicked")

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
             'description': "Mukava huone kaikille teen ystäville"},
            {'name': 'Örkkien maa',
             'n_players': 1,
             'type': '2-2-1',
             'description': "Tämä ei puolestaan ole mikään leikin asia!"}
        ]
        return servers

    def update_table(self):
        """
        """
        self.ui.tableWidgetServers.setRowCount(len(self.servers))

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


def main():
    """
    """
    app = QtWidgets.QApplication(sys.argv)
    window = ServerBrowserMain(app)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
