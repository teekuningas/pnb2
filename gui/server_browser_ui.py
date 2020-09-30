# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_browser.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ServerBrowser(object):
    def setupUi(self, ServerBrowser):
        ServerBrowser.setObjectName("ServerBrowser")
        ServerBrowser.resize(652, 444)
        self.centralwidget = QtWidgets.QWidget(ServerBrowser)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(400, 140))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 632, 382))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonJoin = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonJoin.setObjectName("pushButtonJoin")
        self.gridLayout.addWidget(self.pushButtonJoin, 1, 2, 1, 1)
        self.pushButtonCreate = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonCreate.setObjectName("pushButtonCreate")
        self.gridLayout.addWidget(self.pushButtonCreate, 0, 2, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout.addWidget(self.pushButtonAdd, 3, 2, 1, 1)
        self.tableWidgetServers = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidgetServers.setEnabled(True)
        self.tableWidgetServers.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidgetServers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetServers.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidgetServers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetServers.setShowGrid(True)
        self.tableWidgetServers.setCornerButtonEnabled(True)
        self.tableWidgetServers.setObjectName("tableWidgetServers")
        self.tableWidgetServers.setColumnCount(3)
        self.tableWidgetServers.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetServers.setItem(0, 2, item)
        self.tableWidgetServers.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetServers.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetServers.verticalHeader().setVisible(False)
        self.tableWidgetServers.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidgetServers.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tableWidgetServers, 0, 0, 5, 1)
        self.pushButtonObserve = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonObserve.setObjectName("pushButtonObserve")
        self.gridLayout.addWidget(self.pushButtonObserve, 2, 2, 1, 1)
        self.textEditServerInfo = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEditServerInfo.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textEditServerInfo.setObjectName("textEditServerInfo")
        self.gridLayout.addWidget(self.textEditServerInfo, 5, 0, 1, 1)
        self.lineSplit = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.lineSplit.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineSplit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lineSplit.setObjectName("lineSplit")
        self.gridLayout.addWidget(self.lineSplit, 0, 1, 6, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        ServerBrowser.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ServerBrowser)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 652, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        ServerBrowser.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ServerBrowser)
        self.statusbar.setObjectName("statusbar")
        ServerBrowser.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(ServerBrowser)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(ServerBrowser)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(ServerBrowser)
        QtCore.QMetaObject.connectSlotsByName(ServerBrowser)

    def retranslateUi(self, ServerBrowser):
        _translate = QtCore.QCoreApplication.translate
        ServerBrowser.setWindowTitle(_translate("ServerBrowser", "PNB - Server browser"))
        self.pushButtonJoin.setText(_translate("ServerBrowser", "Join"))
        self.pushButtonCreate.setText(_translate("ServerBrowser", "Create"))
        self.pushButtonAdd.setText(_translate("ServerBrowser", "Add"))
        self.tableWidgetServers.setSortingEnabled(True)
        item = self.tableWidgetServers.verticalHeaderItem(0)
        item.setText(_translate("ServerBrowser", "1"))
        item = self.tableWidgetServers.horizontalHeaderItem(0)
        item.setText(_translate("ServerBrowser", "Name"))
        item = self.tableWidgetServers.horizontalHeaderItem(1)
        item.setText(_translate("ServerBrowser", "Players"))
        item = self.tableWidgetServers.horizontalHeaderItem(2)
        item.setText(_translate("ServerBrowser", "Type"))
        __sortingEnabled = self.tableWidgetServers.isSortingEnabled()
        self.tableWidgetServers.setSortingEnabled(False)
        item = self.tableWidgetServers.item(0, 0)
        item.setText(_translate("ServerBrowser", "Teeluola"))
        item = self.tableWidgetServers.item(0, 1)
        item.setText(_translate("ServerBrowser", "1"))
        item = self.tableWidgetServers.item(0, 2)
        item.setText(_translate("ServerBrowser", "Normal"))
        self.tableWidgetServers.setSortingEnabled(__sortingEnabled)
        self.pushButtonObserve.setText(_translate("ServerBrowser", "Observe"))
        self.menuFile.setTitle(_translate("ServerBrowser", "File"))
        self.menuHelp.setTitle(_translate("ServerBrowser", "Help"))
        self.actionAbout.setText(_translate("ServerBrowser", "About..."))
        self.actionQuit.setText(_translate("ServerBrowser", "Quit"))
