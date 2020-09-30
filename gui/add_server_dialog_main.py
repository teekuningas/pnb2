# coding: utf-8

"""
"""
from PyQt5 import QtWidgets

from add_server_dialog_ui import Ui_AddServerDialog


class AddServerDialogMain(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_AddServerDialog()
        self.ui.setupUi(self)

    def accept(self):
        """
        """
        self.close()
