# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_server_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddServerDialog(object):
    def setupUi(self, AddServerDialog):
        AddServerDialog.setObjectName("AddServerDialog")
        AddServerDialog.resize(427, 364)
        self.gridLayout = QtWidgets.QGridLayout(AddServerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(AddServerDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 407, 314))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(400, 200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName("formLayout")
        self.labelAddress = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelAddress.setObjectName("labelAddress")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelAddress)
        self.lineEditAddress = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEditAddress.setText("")
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditAddress)
        self.labelPort = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelPort.setObjectName("labelPort")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelPort)
        self.lineEditPort = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEditPort.setObjectName("lineEditPort")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditPort)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddServerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(AddServerDialog)
        self.buttonBox.accepted.connect(AddServerDialog.accept)
        self.buttonBox.rejected.connect(AddServerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddServerDialog)

    def retranslateUi(self, AddServerDialog):
        _translate = QtCore.QCoreApplication.translate
        AddServerDialog.setWindowTitle(_translate("AddServerDialog", "PNB - Add server"))
        self.labelAddress.setText(_translate("AddServerDialog", "Address"))
        self.labelPort.setText(_translate("AddServerDialog", "Port"))
        self.lineEditPort.setText(_translate("AddServerDialog", "5555"))
