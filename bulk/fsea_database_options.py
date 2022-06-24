from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/zmast/AppData/Local/Temp/fsea-databaseKGlGHs.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class search_result(Q):

class database_options(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.resize(550, 345)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(550, 345))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: white;")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.titlebar = QtWidgets.QFrame(self.centralwidget)
        self.titlebar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titlebar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titlebar.setStyleSheet("background-color: #31353D;\n"
                                    "color: white;")
        self.titlebar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.titlebar.setObjectName("titlebar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.titlebar)
        self.horizontalLayout.setContentsMargins(15, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.title = QtWidgets.QLabel("F-SEA Database")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.minimizeButton = QtWidgets.QPushButton(self.titlebar)
        self.minimizeButton.setMinimumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setMaximumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.minimizeButton.setStyleSheet("QPushButton { color: white;\n"
                                          "border-image: url(bulk/assets/minimize.png);"
                                          "background-color: #31353D;\n"
                                          "border: none; }\n"
                                          "QPushButton::pressed { background-color: #111314; }")

        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.restoreButton = QtWidgets.QPushButton(self.titlebar)
        self.restoreButton.setMinimumSize(QtCore.QSize(18, 18))
        self.restoreButton.setMaximumSize(QtCore.QSize(18, 18))
        self.restoreButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.restoreButton.setStyleSheet("QPushButton { color: white;\n"
                                         "border-image: url(bulk/assets/maximize.png);"
                                         "background-color: #31353D;\n"
                                         "border: none; }\n"
                                         "QPushButton::pressed { background-color: #111314; }")

        self.restoreButton.setObjectName("restoreButton")
        self.horizontalLayout.addWidget(self.restoreButton)
        self.exitButton = QtWidgets.QPushButton(self.titlebar)
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)
        self.exitButton.setMinimumSize(QtCore.QSize(18, 18))
        self.exitButton.setMaximumSize(QtCore.QSize(18, 18))
        self.exitButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.exitButton.setStyleSheet("QPushButton { color: white;\n"
                                      "                                    background-color: #31353D;\n"
                                      "                                    border-image: url(bulk/assets/closeButton.png); }\n"
                                      "                                    QPushButton::pressed { background-color: #111314; }")

        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)
        self.gridLayout_2.addWidget(self.titlebar, 0, 0, 1, 2)
        self.buttonFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())
        self.buttonFrame.setSizePolicy(sizePolicy)
        self.buttonFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonFrame.setObjectName("buttonFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.buttonFrame)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(9, 0, 9, 9)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.employeedbButton = QtWidgets.QPushButton("Employees")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.employeedbButton.sizePolicy().hasHeightForWidth())
        self.employeedbButton.setSizePolicy(sizePolicy)
        self.employeedbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.employeedbButton.setStyleSheet("QPushButton { color: white;\n"
                                            "                                    background-color: #262829;\n"
                                            "                                    border: none; }\n"
                                            "                                    QPushButton::pressed { background-color: #111314; }")
        self.employeedbButton.setObjectName("employeedbButton")
        self.verticalLayout_4.addWidget(self.employeedbButton)
        self.specimendbButton = QtWidgets.QPushButton("Specimens")
        self.specimendbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.specimendbButton.setStyleSheet("QPushButton { color: white;\n"
                                            "                                    background-color: #262829;\n"
                                            "                                    border: none; }\n"
                                            "                                    QPushButton::pressed { background-color: #111314; }")
        self.specimendbButton.setObjectName("specimendbButton")
        self.verticalLayout_4.addWidget(self.specimendbButton)
        self.missiondbButton = QtWidgets.QPushButton("Missions")
        self.missiondbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.missiondbButton.setStyleSheet("QPushButton { color: white;\n"
                                           "                                    background-color: #262829;\n"
                                           "                                    border: none; }\n"
                                           "                                    QPushButton::pressed { background-color: #111314; }")
        self.missiondbButton.setObjectName("missiondbButton")
        self.verticalLayout_4.addWidget(self.missiondbButton)
        self.departmentdbButton = QtWidgets.QPushButton("Departments")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.departmentdbButton.sizePolicy().hasHeightForWidth())
        self.departmentdbButton.setSizePolicy(sizePolicy)
        self.departmentdbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.departmentdbButton.setStyleSheet("QPushButton { color: white;\n"
                                              "                                    background-color: #262829;\n"
                                              "                                    border: none; }\n"
                                              "                                    QPushButton::pressed { background-color: #111314; }")
        self.departmentdbButton.setObjectName("departmentdbButton")
        self.verticalLayout_4.addWidget(self.departmentdbButton)
        self.gridLayout_2.addWidget(self.buttonFrame, 1, 0, 1, 1)
        self.searchFrame = QtWidgets.QFrame(self.centralwidget)
        self.searchFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.searchFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.searchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.searchFrame.setObjectName("searchFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.searchFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setObjectName("searchBar")
        self.gridLayout.addWidget(self.searchBar, 0, 0, 1, 1)
        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: white;\n"
                                        "                                    background-color: rgb(107, 116, 130);\n"
                                        "                                    border: none; }\n"
                                        "                                    QPushButton::pressed { background-color: #262829; }")
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 1, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(self.searchFrame)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 395, 260))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.gridLayout_2.addWidget(self.searchFrame, 1, 1, 2, 1)
        self.buttonSpacerFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonSpacerFrame.setEnabled(True)
        self.buttonSpacerFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonSpacerFrame.setObjectName("buttonSpacerFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonSpacerFrame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.buttonSpacerFrame, 2, 0, 2, 1)
        self.footer = QtWidgets.QFrame(self.centralwidget)
        self.footer.setMaximumSize(QtCore.QSize(16777215, 20))
        self.footer.setStyleSheet("background-color: white;")
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sizeGrip = QtWidgets.QFrame(self.footer)
        self.sizeGrip.setMaximumSize(QtCore.QSize(20, 20))
        self.sizeGrip.setStyleSheet("background-color: rgb(255, 85, 0);")
        self.sizeGrip.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sizeGrip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sizeGrip.setObjectName("sizeGrip")
        self.horizontalLayout_2.addWidget(self.sizeGrip)
        self.gridLayout_2.addWidget(self.footer, 3, 1, 1, 1, QtCore.Qt.AlignRight)
        self.setCentralWidget(self.centralwidget)


def test():
    app = QApplication([])
    options = database_options()
    options.show()
    app.exec()


test()
