# coding: utf-8

"""
"""
from PyQt5 import QtWidgets

from pnb2.server_browser.add_server_dialog_ui import Ui_AddServerDialog


class AddServerDialogMain(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent, callback):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_AddServerDialog()
        self.ui.setupUi(self)

        self.callback = callback

    def accept(self):
        """
        """
        port = self.ui.lineEditPort.text()
        address = self.ui.lineEditAddress.text()

        try:
            port = int(port)
        except:
            raise Exception('Invalid port number')

        self.callback(address, port)
        self.close()
