# coding: utf-8

"""
"""
import threading

from PyQt5 import QtWidgets

from pnb2.server_browser.create_server_dialog_ui import Ui_CreateServerDialog

from pnb2.networking.server import start_server


class CreateServerDialogMain(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent, callback):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateServerDialog()
        self.ui.setupUi(self)

        self.callback = callback

    def accept(self):
        """
        """

        address = '0.0.0.0'
        port = self.ui.lineEditPort.text()

        try:
            port = int(port)
        except:
            raise Exception("Invalid port number")

        def ready(server_id):
            options = {}
            options['name'] = self.ui.lineEditName.text()
            options['type'] = self.ui.comboBoxType.currentText()
            options['n_players'] = 0
            options['address'] = address
            options['port'] = port
            options['status'] = 'open'
            options['server_id'] = server_id

            self.callback(options)

        # create server
        t = threading.Thread(target=start_server, args=(address, port, ready))
        t.start()
        self.close()

