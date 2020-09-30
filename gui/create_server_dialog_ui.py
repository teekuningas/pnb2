# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_server_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateServerDialog(object):
    def setupUi(self, CreateServerDialog):
        CreateServerDialog.setObjectName("CreateServerDialog")
        CreateServerDialog.resize(427, 364)
        self.gridLayout = QtWidgets.QGridLayout(CreateServerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(CreateServerDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 407, 314))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(400, 200))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName("formLayout")
        self.labelName = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.lineEditName = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.labelType = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelType.setObjectName("labelType")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelType)
        self.comboBoxType = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBoxType.setObjectName("comboBoxType")
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxType)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateServerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(CreateServerDialog)
        self.buttonBox.accepted.connect(CreateServerDialog.accept)
        self.buttonBox.rejected.connect(CreateServerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateServerDialog)

    def retranslateUi(self, CreateServerDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateServerDialog.setWindowTitle(_translate("CreateServerDialog", "PNB - Create server"))
        self.labelName.setText(_translate("CreateServerDialog", "Name"))
        self.lineEditName.setText(_translate("CreateServerDialog", "Ottelu"))
        self.labelType.setText(_translate("CreateServerDialog", "Type"))
        self.comboBoxType.setItemText(0, _translate("CreateServerDialog", "2-2-1"))
        self.comboBoxType.setItemText(1, _translate("CreateServerDialog", "4-4-1"))
