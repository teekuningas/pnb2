# coding: utf-8

"""
"""
from PyQt5 import QtWidgets

from pnb2.server_browser.create_server_dialog_ui import Ui_CreateServerDialog


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

        port = self.ui.lineEditPort.text()
        name = self.ui.lineEditName.text()
        type_ = self.ui.comboBoxType.currentText()

        try:
            port = int(port)
        except:
            raise Exception("Invalid port number")

        self.callback(name, port, type_)
        self.close()

