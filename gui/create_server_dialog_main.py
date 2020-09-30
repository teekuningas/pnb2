# coding: utf-8

"""
"""
from PyQt5 import QtWidgets

from create_server_dialog_ui import Ui_CreateServerDialog


class CreateServerDialogMain(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateServerDialog()
        self.ui.setupUi(self)

    def accept(self):
        """
        """
        self.close()
