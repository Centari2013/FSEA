from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets
from bulk.baseWindows import windowWithToolbar


class searchResult(QtWidgets.QLabel):
    def __init__(self, parent):
        super(searchResult, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 75))
        self.setMaximumSize(QtCore.QSize(16777215, 75))
        self.setAutoFillBackground(False)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setObjectName("search_label")
        #self.setAcceptRichText(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.setStyleSheet("border: 1px solid gray; padding: 6")
        self.append_text()

        #self.verticalScrollBar().setValue(self.verticalScrollBar().minimum())

    def append_text(self):
        text = '''Plain Text
                <b>Bold</b>
                <i>Italic</i>
                <p style="color: red">Red</p>
                <p style="font-size: 20px">20px</p>
                <a href="https://www.google.com">Google</a>'''
        self.setText(text)

    def clear_text(self):
        self.clear()

    def mouseMoveEvent(self):
        if self.underMouse():
            self.setStyleSheet("border: 1px solid blue"
                               "; padding: 6")
    def wheelEvent(self, event):
        if event.type() == QtCore.QEvent.Type.Wheel:
            event.ignore()


class database_options(windowWithToolbar):
    def __init__(self):
        super().__init__()

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
        self.scrollAreaContents = QtWidgets.QWidget()
        self.scrollAreaContents.setEnabled(True)
        self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 395, 660))
        self.scrollAreaContents.setMinimumSize(QtCore.QSize(395, 0))
        self.scrollAreaContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalFrame = QtWidgets.QFrame(self.scrollAreaContents)
        self.verticalFrame.setObjectName("verticalFrame")

        # vertical layout for scroll area
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # add search result to vertical layout
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # add search result text browser to vertical layout
        self.verticalLayout_2.addWidget(searchResult(self.verticalFrame))
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.verticalLayout_3.addWidget(self.verticalFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.gridLayout_2.addWidget(self.searchFrame, 1, 1, 2, 1)
        self.buttonSpacerFrame = QtWidgets.QFrame(self.centralwidget)
        self.buttonSpacerFrame.setEnabled(True)
        self.buttonSpacerFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonSpacerFrame.setObjectName("buttonSpacerFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.buttonSpacerFrame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Fixed)
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

