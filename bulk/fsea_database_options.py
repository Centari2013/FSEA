from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets
from bulk.baseWindows import windowWithToolbar
from utils.searchEngine import searchEmployee
import string


class elidedLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('border: 0px; padding: 0px;')

    # allows for long text to appear elided; when label is expanded, more elided text is shown
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.TextElideMode.ElideRight, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)


class clickableLabel(QLabel):  # used to emulate hyperlink on searchResults
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


class searchResult(QFrame):  # used to populate search results
    def __init__(self, parent=None, ID='', lastName='', firstName='', description=''):
        super(searchResult, self).__init__(parent=None)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 90))
        self.setMaximumSize(QtCore.QSize(16777215, 100))
        self.setAutoFillBackground(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setObjectName("search_label")
        self.setStyleSheet("border: 1px solid gray; padding: 6;")

        self.gridLayout = QGridLayout(parent)

        self.id = ID
        self.lastName = lastName
        self.firstName = firstName
        self.description = description

        # allows for things with only one name to use this class
        if lastName != '':
            nameLabel = elidedLabel('{},  {}'.format(self.lastName, self.firstName))
        else:
            nameLabel = elidedLabel(self.firstName)

        self.gridLayout.addWidget(clickableLabel(self.id), 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(nameLabel, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(elidedLabel(self.description), 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 20)
        self.gridLayout.setColumnStretch(2, 0)

        self.setLayout(self.gridLayout)


class database_options(windowWithToolbar):
    def __init__(self):
        super().__init__()

        self.panelFrame = QtWidgets.QFrame(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panelFrame.sizePolicy().hasHeightForWidth())

        self.panelFrame.setSizePolicy(sizePolicy)
        self.panelFrame.setStyleSheet("background-color: #31353d;")
        self.panelFrame.setObjectName("leftPanelFrame")

        self.panelVLayout = QtWidgets.QVBoxLayout(self.panelFrame)
        self.panelVLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.panelVLayout.setContentsMargins(9, 0, 9, 9)
        self.panelVLayout.setSpacing(9)
        self.panelVLayout.setObjectName("panelVLayout")

        self.employeeButton = QtWidgets.QPushButton("Employees")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.employeeButton.sizePolicy().hasHeightForWidth())
        self.employeeButton.setSizePolicy(sizePolicy)
        self.employeeButton.setMinimumSize(QtCore.QSize(100, 65))
        self.employeeButton.setStyleSheet("QPushButton { color: white;\n"
                                          "background-color: #262829;\n"
                                          "border: none; }\n"
                                          "QPushButton::pressed { background-color: #111314; }")
        self.employeeButton.setObjectName("employeeButton")
        self.panelVLayout.addWidget(self.employeeButton)

        self.specimenButton = QtWidgets.QPushButton("Specimens")
        self.specimenButton.setMinimumSize(QtCore.QSize(100, 65))
        self.specimenButton.setStyleSheet("QPushButton { color: white;\n"
                                          "background-color: #262829;\n"
                                          "border: none; }\n"
                                          "QPushButton::pressed { background-color: #111314; }")
        self.specimenButton.setObjectName("specimenButton")
        self.panelVLayout.addWidget(self.specimenButton)

        self.missionButton = QtWidgets.QPushButton("Missions")
        self.missionButton.setMinimumSize(QtCore.QSize(100, 65))
        self.missionButton.setStyleSheet("QPushButton { color: white;\n"
                                         "background-color: #262829;\n"
                                         "border: none; }\n"
                                         "QPushButton::pressed { background-color: #111314; }")
        self.missionButton.setObjectName("missionButton")
        self.panelVLayout.addWidget(self.missionButton)

        self.departmentButton = QtWidgets.QPushButton("Departments")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.departmentButton.sizePolicy().hasHeightForWidth())
        self.departmentButton.setSizePolicy(sizePolicy)
        self.departmentButton.setMinimumSize(QtCore.QSize(100, 65))
        self.departmentButton.setStyleSheet("QPushButton { color: white;\n"
                                            "background-color: #262829;\n"
                                            "border: none; }\n"
                                            "QPushButton::pressed { background-color: #111314; }")
        self.departmentButton.setObjectName("departmentButton")
        self.panelVLayout.addWidget(self.departmentButton)

        self.primaryGridLayout.addWidget(self.panelFrame, 1, 0, 1, 1)
        self.searchFrame = QtWidgets.QFrame(self.centralWidget)
        self.searchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.searchFrame.setObjectName("searchFrame")

        self.searchGridLayout = QtWidgets.QGridLayout(self.searchFrame)
        self.searchGridLayout.setObjectName("searchGridLayout")

        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: white;\n"
                                        "background-color: rgb(107, 116, 130);\n"
                                        "border: none; }\n"
                                        "QPushButton::pressed { background-color: #262829; }")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(lambda: self.getResults(self.sortSelect.currentIndex()))
        self.searchGridLayout.addWidget(self.searchButton, 0, 1, 1, 2)

        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setStyleSheet("background-color: white;")
        self.searchBar.setObjectName("searchBar")
        self.searchBar.returnPressed.connect(self.searchButton.click)
        self.searchGridLayout.addWidget(self.searchBar, 0, 0, 1, 1)

        self.sortFrame = QFrame()
        self.sortGridLayout = QGridLayout(self.sortFrame)

        self.sortLabel = QLabel('Sort by:')
        self.sortGridLayout.addWidget(self.sortLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.sortSelect = QtWidgets.QComboBox()

        self.sortSelect.addItem('Relevance')
        self.sortSelect.addItem('Alphabet')
        self.sortSelect.addItem(('Alphabet DESC'))
        self.sortSelect.currentIndexChanged.connect(self.sortResults)
        self.sortGridLayout.addWidget(self.sortSelect, 0, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)

        self.sortGridLayout.setColumnStretch(0, 0)
        self.sortGridLayout.setColumnStretch(1, 100)

        self.sortFrame.setLayout(self.sortGridLayout)

        self.searchGridLayout.addWidget(self.sortFrame)
        self.searchGridLayout.setVerticalSpacing(0)

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

        # vertical layout for scrollAreaContentsFrame
        self.scrollAreaVLayout = QtWidgets.QVBoxLayout(self.scrollAreaContents)
        self.scrollAreaVLayout.setObjectName("scrollAreaVLayout")
        self.scrollAreaContentsFrame = QtWidgets.QFrame(self.scrollAreaContents)
        self.scrollAreaContentsFrame.setObjectName("scrollAreaContentsFrame")

        # vertical layout for search results
        self.searchResultsVLayout = QtWidgets.QVBoxLayout(self.scrollAreaContentsFrame)
        self.searchResultsVLayout.setContentsMargins(0, 0, 0, 0)
        self.searchResultsVLayout.setSpacing(10)
        self.searchResultsVLayout.setObjectName("searchResultsVLayout")

        # add search result scrollArea to vertical layout
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.searchGridLayout.addWidget(self.scrollArea, 2, 0, 1, 3)
        self.scrollAreaVLayout.addWidget(self.scrollAreaContentsFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.primaryGridLayout.addWidget(self.searchFrame, 1, 1, 2, 1)
        self.buttonSpacerFrame = QtWidgets.QFrame(self.centralWidget)
        self.buttonSpacerFrame.setEnabled(True)
        self.buttonSpacerFrame.setStyleSheet(" background-color: #31353d;")
        self.buttonSpacerFrame.setObjectName("buttonSpacerFrame")

        self.primaryGridLayout.addWidget(self.buttonSpacerFrame, 2, 0, 2, 1)

        self.footerFrame = QtWidgets.QFrame(self.centralWidget)
        self.footerFrame.setMaximumSize(QtCore.QSize(16777215, 10))
        self.footerFrame.setStyleSheet("background-color: #E3E4EA;")
        self.footerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footerFrame.setObjectName("footerFrame")

        self.footerLayout = QtWidgets.QHBoxLayout(self.footerFrame)
        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setSpacing(0)
        self.footerLayout.setObjectName("footerLayout")

        self.sizeGrip = QSizeGrip(self)

        self.footerLayout.addWidget(self.sizeGrip)
        self.primaryGridLayout.addWidget(self.footerFrame, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setCentralWidget(self.centralWidget)

    def clearSearchResults(self):
        # remove search results starting from last one
        for i in reversed(range(self.searchResultsVLayout.count())):
            self.searchResultsVLayout.itemAt(i).widget().setParent(None)

    def addSearchResult(self, parent=None, ID='', lastName='', firstName='', description='', resultObj=None):
        if resultObj is None:
            self.searchResultsVLayout.addWidget(searchResult(parent, ID, lastName, firstName, description))
        else:
            self.searchResultsVLayout.addWidget(resultObj)

    def getResults(self, order):
        def showNoResults():
            self.clearSearchResults()
            noResults = searchResult(firstName='No Results')
            noResults.setStyleSheet('{border 0px;}')
            self.addSearchResult(resultObj=noResults)

        def cleanText(text):  # remove punctuation for fts5 search in sqlite
            return text.translate(str.maketrans('', '', string.punctuation))

        # text cleaned here to avoid blank query (and any subsequent error resulting from it)
        query = cleanText(str(self.searchBar.text()))
        if query != '':
            self.clearSearchResults()
            results = searchEmployee(query)
            if results[order]:
                self.savedResults = results
                for r in results[order]:
                    self.addSearchResult(ID=r['empID'], firstName=r['firstName'], lastName=r['lastName'],
                                         description=' '.join(r["summary"].split()))
            else:
                showNoResults()
        else:
            showNoResults()

    def sortResults(self, order):
        if self.savedResults is not None:
            self.clearSearchResults()
            for r in self.savedResults[order]:
                self.addSearchResult(ID=r['empID'], firstName=r['firstName'], lastName=r['lastName'],
                                     description=' '.join(r["summary"].split()))
