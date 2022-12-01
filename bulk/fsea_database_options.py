from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets
from bulk.baseWindows import windowWithToolbar
from utils.searchEngine import searchEmployee


class elidedLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('border: 0px; padding: 0px;')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.TextElideMode.ElideRight, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)


class clickableLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('border: 0px; padding: 0px;')

    def enterEvent(self, event):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor('blue'))
        palette.setColor(self.foregroundRole(), QtGui.QColor('blue'))
        self.setPalette(palette)

        f = QtGui.QFont()
        f.setUnderline(True)
        self.setFont(f)

    def leaveEvent(self, event):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtGui.QColor('black'))
        palette.setColor(self.foregroundRole(), QtGui.QColor('black'))
        self.setPalette(palette)

        f = QtGui.QFont()
        f.setUnderline(False)
        self.setFont(f)


class searchResult(QFrame):
    def __init__(self, parent=None, ID='', lastName='', firstName='', description=''):
        super(searchResult, self).__init__(parent=None)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 90))
        self.setMaximumSize(QtCore.QSize(16777215, 90))
        self.setAutoFillBackground(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setObjectName("search_label")
        self.setStyleSheet("border: 1px solid gray; padding: 6;")

        self.gridLayout = QGridLayout(parent)

        self.id = ID
        self.lastName = lastName
        self.firstName = firstName
        self.description = description

        self.gridLayout.addWidget(clickableLabel(self.id), 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(elidedLabel('{},  {}'.format(self.lastName, self.firstName)), 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        # self.gridLayout.addWidget(elidedLabel('{}'.format(self.firstName)), 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(elidedLabel(self.description), 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 20)
        self.gridLayout.setColumnStretch(2, 0)

        self.setLayout(self.gridLayout)

    '''
    def enterEvent(self, enter):
        self.setStyleSheet("border: 1px solid blue; padding: 6; ")

    def leaveEvent(self, event):
        self.setStyleSheet("border: 1px solid gray; padding: 6;")
    '''


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

        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: white;\n"
                                        "background-color: rgb(107, 116, 130);\n"
                                        "border: none; }\n"
                                        "QPushButton::pressed { background-color: #262829; }")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self.getResults)
        self.gridLayout.addWidget(self.searchButton, 0, 1, 1, 2)

        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setStyleSheet("background-color: white;")
        self.searchBar.setObjectName("searchBar")
        self.searchBar.returnPressed.connect(self.searchButton.click)
        self.gridLayout.addWidget(self.searchBar, 0, 0, 1, 1)

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

    def addSearchResult(self, parent=None, ID='', lastName='', firstName='', description=''):
        self.verticalLayout_2.addWidget(searchResult(parent, ID, lastName, firstName, description))

    def getResults(self):
        query = str(self.searchBar.text())
        if query != '':
            results = searchEmployee(query)

            for r in results:
                self.addSearchResult(ID=r['empID'], firstName=r['firstName'], lastName=r['lastName'], description=r['summary'])





