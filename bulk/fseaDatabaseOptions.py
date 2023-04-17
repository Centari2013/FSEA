from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtCore, QtGui, QtWidgets
from bulk.baseWindows import windowWithToolbar
from bulk.colorPresets import *
from utils.searchEngine import search
import string
from bulk.infoWindow import employeeInfo
from utils.variables import employeeType, specimenType, originType, missionType, departmentType
import time

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


class idLabel(QLabel):  # used to emulate hyperlink on searchResults
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
    def __init__(self, parent=None, ID=None, type=None, lastName=None, firstName=None, description=None):
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
        self.type = type

        # allows for things with only one name to use this class
        if firstName is not None:
            nameLabel = elidedLabel('{},  {}'.format(self.lastName, self.firstName))
        else:
            nameLabel = elidedLabel(self.lastName)

        self.idLabel = idLabel(self.id)
        self.idLabel.mousePressEvent = self.openInfoWindow

        self.gridLayout.addWidget(self.idLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(nameLabel, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addWidget(elidedLabel(self.description), 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 20)
        self.gridLayout.setColumnStretch(2, 0)

        self.setLayout(self.gridLayout)
        self.Window = None

    def openInfoWindow(self, QMouseEvent):
        if self.type == employeeType:
            self.Window = employeeInfo(self.id)

        self.Window.show()


class panelButton(QPushButton):
    def __init__(self, buttonText, flag):
        super().__init__(buttonText)

        self.flag = flag
        self.setCheckable(True)
        self.clicked.connect(self.changeButtonColor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(100, 65))
        self.setStyleSheet("QPushButton { color: white;\n"
                           "background-color: %s;\n"
                           "border: none; }\n"
                           "QPushButton::pressed { background-color: %s; }" % (
                               push_button_color, push_button_pressed_color))

    def changeButtonColor(self):
        if self.isChecked():
            self.setStyleSheet("QPushButton { color: %s;\n"
                               "background-color: %s;\n"
                               "border: none; }\n"
                               "QPushButton::pressed { background-color: %s; }" % (
                                   push_button_text_color, push_button_pressed_color, push_button_pressed_color))
        else:
            self.setStyleSheet("QPushButton { color: %s;\n"
                               "background-color: %s;\n"
                               "border: none; }\n"
                               "QPushButton::pressed { background-color: %s; }" % (
                                   push_button_text_color, push_button_color, push_button_pressed_color))


class database_options(windowWithToolbar):
    def __init__(self):
        super().__init__()
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

        self.panelFrame = QtWidgets.QFrame(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panelFrame.sizePolicy().hasHeightForWidth())

        self.panelFrame.setSizePolicy(sizePolicy)
        self.panelFrame.setStyleSheet("background-color: %s;" % frame_color)
        self.panelFrame.setObjectName("leftPanelFrame")

        self.panelVLayout = QtWidgets.QVBoxLayout(self.panelFrame)
        self.panelVLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.panelVLayout.setContentsMargins(9, 0, 9, 9)
        self.panelVLayout.setSpacing(9)
        self.panelVLayout.setObjectName("panelVLayout")

        self.filterList = []

        self.employeeButton = panelButton("Employees", employeeType)
        self.employeeButton.clicked.connect(lambda: self.setFilterFlag(self.employeeButton))
        self.employeeButton.clicked.connect(lambda: self.sortResults(self.resultOrder))
        self.employeeButton.setObjectName("employeeButton")
        self.panelVLayout.addWidget(self.employeeButton)

        self.specimenButton = panelButton("Specimens", specimenType)
        self.specimenButton.clicked.connect(lambda: self.setFilterFlag(self.specimenButton))
        self.specimenButton.clicked.connect(lambda: self.sortResults(self.resultOrder))
        self.specimenButton.setObjectName("specimenButton")
        self.panelVLayout.addWidget(self.specimenButton)

        self.missionButton = panelButton("Missions", missionType)
        self.missionButton.clicked.connect(lambda: self.setFilterFlag(self.missionButton))
        self.missionButton.clicked.connect(lambda: self.sortResults(self.resultOrder))
        self.missionButton.setObjectName("missionButton")
        self.panelVLayout.addWidget(self.missionButton)

        self.departmentButton = panelButton("Departments", departmentType)
        self.departmentButton.clicked.connect(lambda: self.setFilterFlag(self.departmentButton))
        self.departmentButton.clicked.connect(lambda: self.sortResults(self.resultOrder))
        self.departmentButton.setObjectName("departmentButton")
        self.panelVLayout.addWidget(self.departmentButton)

        self.originButton = panelButton("Origins", originType)
        self.originButton.clicked.connect(lambda: self.setFilterFlag(self.originButton))
        self.originButton.clicked.connect(lambda: self.sortResults(self.resultOrder))
        self.originButton.setObjectName("originButton")
        self.panelVLayout.addWidget(self.originButton)

        self.primaryGridLayout.addWidget(self.panelFrame, 1, 0, 1, 1)
        self.searchFrame = QtWidgets.QFrame(self.centralWidget)
        self.searchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.searchFrame.setObjectName("searchFrame")

        self.searchGridLayout = QtWidgets.QGridLayout(self.searchFrame)
        self.searchGridLayout.setObjectName("searchGridLayout")

        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: %s;\n"
                                        "background-color: %s;\n"
                                        "border: none; }\n"
                                        "QPushButton::pressed { background-color: %s; }" % (
                                            push_button_text_color, search_button_color, push_button_color))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(lambda: self.getResults(self.sortSelect.currentIndex()))
        self.searchGridLayout.addWidget(self.searchButton, 0, 1, 1, 2)

        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setStyleSheet("background-color: %s;" % search_bar_color)
        self.searchBar.setObjectName("searchBar")
        self.searchBar.returnPressed.connect(self.searchButton.click)
        self.searchGridLayout.addWidget(self.searchBar, 0, 0, 1, 1)

        self.sortFrame = QFrame(self)
        self.sortGridLayout = QGridLayout(self.sortFrame)

        self.sortLabel = QLabel('Sort by')
        self.sortGridLayout.addWidget(self.sortLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.sortSelect = QtWidgets.QComboBox()

        self.sortSelect.addItem('Relevance')
        self.sortSelect.addItem('Alphabet')
        self.sortSelect.addItem(('Alphabet DESC'))
        self.sortSelect.currentIndexChanged.connect(self.sortResults)
        self.sortGridLayout.addWidget(self.sortSelect, 0, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)

        self.resultLimitDropDown = QComboBox(self)
        self.resultLimitDropDown.addItems(['10', '25', '50', '100'])
        self.sortGridLayout.addWidget(QLabel("Per Page"), 0, 2)
        self.sortGridLayout.addWidget(self.resultLimitDropDown, 0, 3, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.sortGridLayout.setColumnStretch(0, 0)
        self.sortGridLayout.setColumnStretch(1, 100)

        self.sortFrame.setLayout(self.sortGridLayout)

        self.searchGridLayout.addWidget(self.sortFrame)
        self.searchGridLayout.setVerticalSpacing(0)

        self.scrollArea = QtWidgets.QScrollArea(self.searchFrame)
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
        self.buttonSpacerFrame.setStyleSheet(" background-color: %s;" % frame_color)
        self.buttonSpacerFrame.setObjectName("buttonSpacerFrame")

        self.primaryGridLayout.addWidget(self.buttonSpacerFrame, 2, 0, 2, 1)

        self.footerFrame = QtWidgets.QFrame(self.centralWidget)
        self.footerFrame.setMaximumSize(QtCore.QSize(16777215, 10))
        self.footerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.footerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.footerFrame.setObjectName("footerFrame")

        self.footerLayout = QtWidgets.QHBoxLayout(self.footerFrame)
        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setSpacing(0)
        self.footerLayout.setObjectName("footerLayout")

        self.sizeGrip = QSizeGrip(self)
        self.footerLayout.addWidget(self.sizeGrip)

        self.pageSelect = QLineEdit()
        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^[0-9]*$"), self)
        self.pageSelect.setValidator(validator)
        self.pageSelect.setText("1")
        self.pageSelect.setFixedWidth(30)

        self.prevPage = QPushButton("<-")
        self.prevPage.setFixedWidth(30)
        self.nextPage = QPushButton("->")
        self.nextPage.setFixedWidth(30)

        of = QLabel("of")
        of.setMargin(5)
        of.setFixedWidth(25)
        self.totalPagesLabel = QLabel("1")
        self.totalPagesLabel.setFixedWidth(25)
        self.totalPagesLabel.setMargin(5)
        self.pageNavFrame = QHBoxLayout()

        self.initPageNav()

        self.pageNavFrame.addWidget(self.prevPage)
        self.pageNavFrame.addWidget(self.pageSelect)
        self.pageNavFrame.addWidget(of)
        self.pageNavFrame.addWidget(self.totalPagesLabel)
        self.pageNavFrame.addWidget(self.nextPage)

        self.primaryGridLayout.addLayout(self.pageNavFrame,2, 1, Qt.AlignmentFlag.AlignHCenter)

        self.primaryGridLayout.addWidget(self.footerFrame, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setCentralWidget(self.centralWidget)

        self.savedResults = None
        self.savedResultObjects = []
        self.newResults = True  # used to avoid needless object creation when sorting
        self.resultOrder = 0


    def initPageNav(self):
        def prevPage():
            page = self.pageSelect.text()
            if page != "":
                if int(page) > 1:
                    self.pageSelect.setText(str(int(page) - 1))
                    self.clearSearchResults()
                    self.addSearchResults(self.filterHelper(self.sortSelect.currentIndex()))

        def nextPage():
            page = self.pageSelect.text()
            if page != "":
                if int(page) < int(self.totalPagesLabel.text()):
                    self.pageSelect.setText(str(int(page) + 1))
                    self.clearSearchResults()
                    self.addSearchResults(self.filterHelper(self.sortSelect.currentIndex()))

        def submitPage():
            if self.pageSelect.text() != "":
                page = int(self.pageSelect.text())
                if page < 1:
                    self.pageSelect.setText("1")
                if page > int(self.totalPagesLabel.text()):
                    self.pageSelect.setText(self.totalPagesLabel.text())


        self.prevPage.clicked.connect(prevPage)
        self.nextPage.clicked.connect(nextPage)
        self.pageSelect.returnPressed.connect(submitPage)

    def clearSearchResults(self):
        start = time.time()
        # remove search results starting from last one
        for i in reversed(range(self.searchResultsVLayout.count())):
            self.searchResultsVLayout.itemAt(i).widget().setParent(None)
        end = time.time()
        executionTime = end - start
        print("clearSearchResults Execution Time: ", executionTime)
    def addSearchResults(self, results):
        start = time.time()
        limit = int(self.resultLimitDropDown.currentText())
        startingIndex = (int(self.pageSelect.text()) - 1) * limit
        for i in range(startingIndex, startingIndex + limit):
            if i == len(results):
                break
            self.searchResultsVLayout.addWidget(results[i])
        end = time.time()
        executionTime = end - start
        print("addSearchResults Execution Time: ", executionTime)

    def getResults(self, order):

        def showNoResults():
            self.clearSearchResults()
            noResults = searchResult(lastName='No Results')
            noResults.setStyleSheet('{border 0px;}')
            self.addSearchResults([noResults])

        self.newResults = True
        # text punctuation removed  here to avoid blank query (and any subsequent error resulting from it)
        query = str(self.searchBar.text()).translate(str.maketrans('', '', string.punctuation))
        if query != '':
            self.clearSearchResults()
            start = time.time()
            results = search(query)
            end = time.time()
            executionTime = end - start
            print("Search Execution Time: ", executionTime)
            if results:
                self.savedResults = results
                self.addSearchResults(self.filterHelper(order))
            else:
                showNoResults()
        else:
            showNoResults()

    def sortResults(self, order):
        self.resultOrder = order
        if self.savedResults is not None:
            self.clearSearchResults()
            self.addSearchResults(self.filterHelper(order))

    def filterHelper(self, order):
        start = time.time()
        if self.newResults:
            self.savedResultObjects.clear()
            for i in self.savedResults:
                poop = {s: s.type for s in (
                    searchResult(ID=r['id'], lastName=r['lastName'], firstName=r['firstName'], description=' '.join(
                        r['description'].split()), type=r['type']) for r in i)}
                self.savedResultObjects.append(poop)
            self.newResults = False

        if self.filterList:
            results = [k for k, v in self.savedResultObjects[order].items() if (v in self.filterList)]
        else:
            results = [k for k in self.savedResultObjects[order]]

        perPage = int(self.resultLimitDropDown.currentText())
        numOfResults = len(results)
        modResult = 0
        if numOfResults % perPage != 0:
            modResult = 1

        self.totalPagesLabel.setText(str(int(numOfResults / perPage) + modResult))
        end = time.time()
        executionTime = end - start
        print("filterHelper Execution Time: ", executionTime)
        return results

    def setFilterFlag(self, button):
        if button.isChecked():
            self.filterList.append(button.flag)
        else:
            self.filterList.remove(button.flag)

