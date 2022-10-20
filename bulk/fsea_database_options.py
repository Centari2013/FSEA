from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets
from bulk.baseWindows import draggableFrameless


class database_options(draggableFrameless):

    # class searchResult(QTextBrowser):

    def __init__(self):
        super().__init__()

        sizePolicy = QtWidgets.QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QtCore.QSize(550, 345))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("background-color: #E3E4EA;")
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.titlebar = QtWidgets.QFrame(self.centralwidget)
        self.titlebar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.titlebar.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.titlebar.setStyleSheet("background-color: #31353D;\n"
                                    "color: white;")
        self.titlebar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.titlebar.setObjectName("titlebar")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.titlebar)
        self.horizontalLayout.setContentsMargins(15, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.title = QtWidgets.QLabel("F-SEA Database")
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.minimizeButton = QtWidgets.QPushButton(self.titlebar)
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.setMinimumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setMaximumSize(QtCore.QSize(18, 18))
        self.minimizeButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.minimizeButton.setStyleSheet("QPushButton { color: white;\n"
                                          "border-image: url(bulk/assets/minimize.png);"
                                          "background-color: #31353D;\n"
                                          "border: none; }\n"
                                          "QPushButton::pressed { background-color: #111314; }")

        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)

        self.restoreButton = QtWidgets.QPushButton(self.titlebar)

        def minOrMax():
            if self.isMaximized():
                self.showNormal()
                # self.restoreButton.setStyleSheet("border-image: url(bulk/assets/restore.png);")
            elif not self.isMaximized():
                self.showMaximized()
                # self.restoreButton.setStyleSheet("border-image: url(bulk/assets/maximize.png);")

        self.restoreButton.clicked.connect(minOrMax)
        self.restoreButton.setMinimumSize(QtCore.QSize(18, 18))
        self.restoreButton.setMaximumSize(QtCore.QSize(18, 18))
        self.restoreButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
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
        self.exitButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.exitButton.setStyleSheet("QPushButton { color: white;\n"
                                      "background-color: #31353D;\n"
                                      "border-image: url(bulk/assets/closeButton.png); }\n"
                                      "QPushButton::pressed { background-color: #111314; }")

        self.exitButton.setObjectName("exitButton")
        self.horizontalLayout.addWidget(self.exitButton)

        self.gridLayout_2.addWidget(self.titlebar, 0, 0, 1, 2)

        self.buttonFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonFrame.sizePolicy().hasHeightForWidth())

        self.buttonFrame.setSizePolicy(sizePolicy)
        self.buttonFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonFrame.setObjectName("buttonFrame")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.buttonFrame)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(9, 0, 9, 9)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.employeedbButton = QtWidgets.QPushButton("Employees")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.employeedbButton.sizePolicy().hasHeightForWidth())
        self.employeedbButton.setSizePolicy(sizePolicy)
        self.employeedbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.employeedbButton.setStyleSheet("QPushButton { color: white;\n"
                                            "background-color: #262829;\n"
                                            "border: none; }\n"
                                            "QPushButton::pressed { background-color: #111314; }")
        self.employeedbButton.setObjectName("employeedbButton")
        self.verticalLayout_4.addWidget(self.employeedbButton)

        self.specimendbButton = QtWidgets.QPushButton("Specimens")
        self.specimendbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.specimendbButton.setStyleSheet("QPushButton { color: white;\n"
                                            "background-color: #262829;\n"
                                            "border: none; }\n"
                                            "QPushButton::pressed { background-color: #111314; }")
        self.specimendbButton.setObjectName("specimendbButton")
        self.verticalLayout_4.addWidget(self.specimendbButton)

        self.missiondbButton = QtWidgets.QPushButton("Missions")
        self.missiondbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.missiondbButton.setStyleSheet("QPushButton { color: white;\n"
                                           "background-color: #262829;\n"
                                           "border: none; }\n"
                                           "QPushButton::pressed { background-color: #111314; }")
        self.missiondbButton.setObjectName("missiondbButton")
        self.verticalLayout_4.addWidget(self.missiondbButton)

        self.departmentdbButton = QtWidgets.QPushButton("Departments")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.departmentdbButton.sizePolicy().hasHeightForWidth())
        self.departmentdbButton.setSizePolicy(sizePolicy)
        self.departmentdbButton.setMinimumSize(QtCore.QSize(100, 65))
        self.departmentdbButton.setStyleSheet("QPushButton { color: white;\n"
                                              "background-color: #262829;\n"
                                              "border: none; }\n"
                                              "QPushButton::pressed { background-color: #111314; }")
        self.departmentdbButton.setObjectName("departmentdbButton")
        self.verticalLayout_4.addWidget(self.departmentdbButton)

        self.gridLayout_2.addWidget(self.buttonFrame, 1, 0, 1, 1)
        self.searchFrame = QtWidgets.QFrame(self.centralwidget)
        self.searchFrame.setStyleSheet("background-color: #E3E4A;")
        self.searchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.searchFrame.setObjectName("searchFrame")

        self.gridLayout = QtWidgets.QGridLayout(self.searchFrame)
        self.gridLayout.setObjectName("gridLayout")

        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setStyleSheet("background-color: white;")
        self.searchBar.setObjectName("searchBar")
        self.gridLayout.addWidget(self.searchBar, 0, 0, 1, 1)

        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: white;\n"
                                        "background-color: rgb(107, 116, 130);\n"
                                        "border: none; }\n"
                                        "QPushButton::pressed { background-color: #262829; }")
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 1, 1, 2)

        self.scrollArea = QtWidgets.QScrollArea(self.searchFrame)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaLayout = QtWidgets.QWidget()
        self.scrollAreaLayout.setLayout(QVBoxLayout())
        self.scrollAreaLayout.setGeometry(QtCore.QRect(0, 0, 395, 260))
        self.scrollAreaLayout.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaLayout)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)

        self.gridLayout_2.addWidget(self.searchFrame, 1, 1, 2, 1)
        self.buttonSpacerFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonSpacerFrame.setEnabled(True)
        self.buttonSpacerFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonSpacerFrame.setObjectName("buttonSpacerFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonSpacerFrame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.buttonSpacerFrame, 2, 0, 2, 1)
        self.footer = QtWidgets.QFrame(self.centralwidget)
        self.footer.setMaximumSize(QtCore.QSize(16777215, 10))
        self.footer.setStyleSheet("background-color: #E3E4EA;")
        self.footer.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.sizeGrip = QSizeGrip(self)

        self.horizontalLayout_2.addWidget(self.sizeGrip)
        self.gridLayout_2.addWidget(self.footer, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setCentralWidget(self.centralwidget)

        self.prevPos = None

    # TODO fix drag and resize overlap


