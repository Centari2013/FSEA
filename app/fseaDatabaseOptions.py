from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QFrame, QGridLayout, QPushButton, QComboBox, QLineEdit, QSpacerItem, QSizePolicy

from app.baseWindows import windowWithTitleBar
from app.stylePresets import colors, stylesheets
from app.customQWidgets import PanelButton, ElidedLabel, IdLabel
from app.infoWindow import EmployeeInfo
from utils.searchEngine import searchEngine
from utils.dbVariables import (employeeType, specimenType, originType,
                               missionType, departmentType)



class database_options(windowWithTitleBar):
    def __init__(self):
        super(database_options, self).__init__(None)

        self.sEngine = searchEngine()

        self.sidePanelFrame = QtWidgets.QFrame(self.centralWidget)
        self.sidePanelVLayout = QtWidgets.QVBoxLayout(self.sidePanelFrame)
        self.filterList = []

        self.employeeButton = PanelButton("Employees", employeeType)
        self.specimenButton = PanelButton("Specimens", specimenType)
        self.missionButton = PanelButton("Missions", missionType)
        self.departmentButton = PanelButton("Departments", departmentType)
        self.originButton = PanelButton("Origins", originType)
        self._initSidePanel()

        self.searchFrame = QtWidgets.QFrame(self.centralWidget)
        self.searchGridLayout = QtWidgets.QGridLayout(self.searchFrame)
        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchBar = QtWidgets.QLineEdit(self.searchFrame)
        self.searchBar.setFocus()
        self.sortFrame = QFrame(self)
        self.sortGridLayout = QGridLayout(self.sortFrame)
        self.sortSelect = QtWidgets.QComboBox()
        self.resultLimitDropDown = QComboBox(self)
        self._initSearchFrame()

        self.scrollArea = QtWidgets.QScrollArea(self.searchFrame)
        self.scrollAreaContents = QtWidgets.QWidget()
        self.scrollAreaContentsFrame = QtWidgets.QFrame(self.scrollAreaContents)
        self.scrollAreaVLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaContents)  # vertical layout for scrollAreaContentsFrame
        self.searchResultsVLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaContentsFrame)  # vertical layout for search results
        self._initSearchResultsArea()

        self.pageSelect = QLineEdit()
        self.prevPage = QPushButton("<-")
        self.nextPage = QPushButton("->")
        self.totalPagesLabel = QLabel("1")
        self.maxResultLabel = QLabel("of\t0")
        self.resultPos = QLabel("0 - 0")
        self.pageNavFrame = QFrame(self)
        self.pageNavLayout = QGridLayout(self.pageNavFrame)
        self._initPageNav()

        self.initFooter(self.pageNavFrame)

        self.savedResults = None
        self.resultOrder = 0
        self.numOfResults = None

    def _add_filter_button(self, button):
        button.clicked.connect(lambda: self._setFilterFlag(button))
        button.clicked.connect(lambda: self._sortResults(self.resultOrder))
        button.setObjectName(button.objectName())
        self.sidePanelVLayout.addWidget(button)

    def _initSidePanel(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidePanelFrame.sizePolicy().hasHeightForWidth())

        self.sidePanelFrame.setSizePolicy(sizePolicy)
        self.sidePanelFrame.setStyleSheet("background-color: %s;" % colors["FRAME_COLOR"])
        self.sidePanelFrame.setObjectName("leftPanelFrame")

        self.sidePanelVLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.sidePanelVLayout.setSpacing(9)
        self.sidePanelVLayout.setObjectName("panelVLayout")

        self.employeeButton.setObjectName("employeeButton")
        self.specimenButton.setObjectName("specimenButton")
        self.missionButton.setObjectName("missionButton")
        self.departmentButton.setObjectName("departmentButton")
        self.originButton.setObjectName("originButton")

        self._add_filter_button(self.employeeButton)
        self._add_filter_button(self.specimenButton)
        self._add_filter_button(self.missionButton)
        self._add_filter_button(self.departmentButton)
        self._add_filter_button(self.originButton)

        self.sidePanelVLayout.addStretch()

        self.primaryGridLayout.addWidget(self.sidePanelFrame, 1, 0, 1, 1)

    def _initSearchFrame(self):
        self.searchFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.searchFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.searchFrame.setObjectName("searchFrame")

        self.searchGridLayout.setObjectName("searchGridLayout")

        self.searchButton.setMinimumSize(QtCore.QSize(50, 20))
        self.searchButton.setStyleSheet("QPushButton { color: %s;\n"
                                        "background-color: %s;\n"
                                        "border: none; }\n"
                                        "QPushButton::pressed { background-color: %s; }" % (
                                            colors["PUSH_BUTTON_TEXT_COLOR"], colors["SEARCH_BUTTON_COLOR"],
                                            colors["PUSH_BUTTON_COLOR"]))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(self._getResults)
        self.searchGridLayout.addWidget(self.searchButton, 0, 1, 1, 2)

        self.searchBar.setStyleSheet("background-color: %s;" % colors["SEARCH_BAR_COLOR"])
        self.searchBar.setObjectName("searchBar")
        self.searchBar.returnPressed.connect(self.searchButton.click)
        self.searchGridLayout.addWidget(self.searchBar, 0, 0, 1, 1)

        sortLabel = QLabel('Sort by')
        self.sortGridLayout.addWidget(sortLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.sortSelect.addItem('Relevance')
        self.sortSelect.addItem('Alphabet')
        self.sortSelect.addItem('Alphabet DESC')
        self.sortSelect.currentIndexChanged.connect(self._sortResults)
        self.sortGridLayout.addWidget(self.sortSelect, 0, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)

        self.resultLimitDropDown.addItems(['10', '25', '50'])
        self.sortGridLayout.addWidget(QLabel("Per Page"), 0, 2)
        self.sortGridLayout.addWidget(self.resultLimitDropDown, 0, 3, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.sortGridLayout.setColumnStretch(1, 100)

        self.sortFrame.setLayout(self.sortGridLayout)

        self.searchGridLayout.addWidget(self.sortFrame)
        self.searchGridLayout.setVerticalSpacing(0)

    def _initSearchResultsArea(self):
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        bar = self.scrollArea.verticalScrollBar()
        bar.setStyleSheet(stylesheets["SCROLL_BAR"])
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaContents.setEnabled(True)
        self.scrollAreaContents.setGeometry(QtCore.QRect(0, 0, 395, 660))
        self.scrollAreaContents.setMinimumSize(QtCore.QSize(395, 0))
        self.scrollAreaContents.setObjectName("scrollAreaWidgetContents")

        self.scrollAreaVLayout.setObjectName("scrollAreaVLayout")
        self.scrollAreaContentsFrame.setObjectName("scrollAreaContentsFrame")

        self.searchResultsVLayout.setContentsMargins(0, 0, 0, 0)
        self.searchResultsVLayout.setSpacing(10)
        self.searchResultsVLayout.setObjectName("searchResultsVLayout")

        # add search result scrollArea to vertical layout
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.searchGridLayout.addWidget(self.scrollArea, 2, 0, 1, 3)
        self.scrollAreaVLayout.addWidget(self.scrollAreaContentsFrame, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.primaryGridLayout.addWidget(self.searchFrame, 1, 1, 2, 1)
        buttonSpacerFrame = QtWidgets.QFrame(self.centralWidget)
        buttonSpacerFrame.setEnabled(True)
        buttonSpacerFrame.setStyleSheet(" background-color: %s;" % colors["FRAME_COLOR"])
        buttonSpacerFrame.setObjectName("buttonSpacerFrame")
        self.primaryGridLayout.addWidget(buttonSpacerFrame, 2, 0, 2, 1)

    def _initPageNav(self):

        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("^[0-9]*$"), self)
        self.pageSelect.setValidator(validator)
        self.pageSelect.setText("1")
        self.pageSelect.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.pageSelect.setFixedWidth(30)
        self.prevPage.setFixedWidth(30)
        self.nextPage.setFixedWidth(30)
        self.maxResultLabel.setFixedWidth(75)

        of = QLabel("of")
        of.setMargin(5)
        of.setFixedWidth(25)

        self.totalPagesLabel.setFixedWidth(25)
        self.totalPagesLabel.setMargin(5)

        self.resultPos.setFixedWidth(50)

        resultPosLabel = QLabel("Results")
        resultPosLabel.setMargin(5)
        resultPosLabel.setFixedWidth(50)

        def _prevPage():
            page = self.pageSelect.text()
            if page != "":
                if int(page) > 1:
                    self.pageSelect.setText(str(int(page) - 1))
                    self._updateResults()

        def _nextPage():
            page = self.pageSelect.text()
            if page != "":
                if int(page) < int(self.totalPagesLabel.text()):
                    self.pageSelect.setText(str(int(page) + 1))
                    self._updateResults()

        def _submitPage():
            if self.pageSelect.text() != "":
                page = int(self.pageSelect.text())
                if page < 1:
                    self.pageSelect.setText("1")
                if page > int(self.totalPagesLabel.text()):
                    self.pageSelect.setText(self.totalPagesLabel.text())

                self._updateResults()

        self.prevPage.clicked.connect(_prevPage)
        self.nextPage.clicked.connect(_nextPage)
        self.pageSelect.returnPressed.connect(_submitPage)
        self.resultLimitDropDown.currentIndexChanged.connect(lambda: self.pageSelect.setText("1"))
        self.resultLimitDropDown.currentIndexChanged.connect(self._updateResults)

        self.pageNavLayout.setSpacing(10)
        self.pageNavLayout.setContentsMargins(5, 0, 0, 5)
        self.pageNavLayout.addWidget(resultPosLabel, 0, 0)
        self.pageNavLayout.addWidget(self.resultPos, 0, 1)
        self.pageNavLayout.addWidget(self.maxResultLabel, 0, 2, Qt.AlignmentFlag.AlignLeft)
        self.pageNavLayout.addWidget(self.prevPage, 0, 3)
        self.pageNavLayout.addWidget(self.pageSelect, 0, 4)
        self.pageNavLayout.addWidget(of, 0, 5)
        self.pageNavLayout.addWidget(self.totalPagesLabel, 0, 6)
        self.pageNavLayout.addWidget(self.nextPage, 0, 7)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.pageNavLayout.addItem(spacer, 0, 8, 1, 2)

        self.pageNavFrame.setLayout(self.pageNavLayout)

    def _updateResults(self):
        def showNoResults():
            self._clearSearchResults()
            noResults = {'id': '',
                         'lastName': 'No Results',
                         'firstName': None,
                         'description': '',
                         'type': ''}
            self.populateSearchResults([noResults])
            self.pageSelect.setText("1")
            self.totalPagesLabel.setText("1")
        results = self._filterHelper()
        if results:
            perPage = int(self.resultLimitDropDown.currentText())
            numOfResults = len(results)
            extraPage = 0
            if (numOfResults % perPage != 0) or numOfResults == 0:
                extraPage = 1
            self.totalPagesLabel.setText(f"{int(numOfResults / perPage) + extraPage}")

            self._clearSearchResults()
            self.populateSearchResults(results)
            bar = self.scrollArea.verticalScrollBar()
            bar.setValue(bar.minimum())

            page = int(self.pageSelect.text())
            limit = int(self.resultLimitDropDown.currentText())
            fromResultNum = (page - 1) * limit + 1

            toResultNum = fromResultNum + limit - 1

            if page == int(self.totalPagesLabel.text()):
                toResultNum = fromResultNum + (self.numOfResults % limit) - 1

            self.resultPos.setText(f"{fromResultNum} - {toResultNum}")
            self.maxResultLabel.setText(f"of\t{self.numOfResults}")
        else:
            showNoResults()

    def _clearSearchResults(self):
        """
           Removes the search results starting from last one

           Returns:
               void
        """
        for i in reversed(range(self.searchResultsVLayout.count())):
            self.searchResultsVLayout.itemAt(i).widget().setParent(None)

    def populateSearchResults(self, results):
        limit = int(self.resultLimitDropDown.currentText())
        startingIndex = (int(self.pageSelect.text()) - 1) * limit
        search_results = [
            self.SearchResult(ID=r['id'], lastName=r['lastName'], firstName=r['firstName'], description=' '.join(
                r['description'].split()), resultType=r['type']) for i, r in enumerate(results) if
            startingIndex <= i < (startingIndex + limit) and i < len(results)]
        for obj in search_results:
            self.searchResultsVLayout.addWidget(obj)

    def _getResults(self):
        """
                   Removes the search results starting from last one

                   Returns:
                       void
                """
        self.pageSelect.setText("1")  # stops pages from being out of bounds on new queries
        # and takes user to first page of results

        # text punctuation removed  here to avoid blank query (and any subsequent error resulting from it)
        query = str(self.searchBar.text())
        self._clearSearchResults()
        results = self.sEngine.search(query)
        self.savedResults = results
        self._updateResults()

    def _sortResults(self, order):
        self.resultOrder = order
        if self.savedResults is not None:
            self._updateResults()

    def _filterHelper(self):
        """
                Returns a list of result dictionaries if their type is in the filter list.

                Parameters:
                    n/a

                Returns:
                    List of dictionaries.
        """

        order = self.sortSelect.currentIndex()
        results = []
        if self.savedResults:
            if self.savedResults[0] is not None:
                if self.filterList:
                    results = [k for k in self.savedResults[order] if (k['type'] in self.filterList)]
                else:
                    results = [k for k in self.savedResults[order]]

                self.numOfResults = len(results)

        return results

    def _setFilterFlag(self, button):
        if button.isChecked():
            self.filterList.append(button.flag)
        else:
            self.filterList.remove(button.flag)

    class SearchResult(QFrame):
        """
                A frame inherited from QFrame that is used to populate
                search results

                Added Attributes:
                    idLabel (IdLabel): The clickable QLabel
                    id (str): The ID you want to show in the idLabel.

                Added Methods:
                    openInfoWindow(): opens window with more info on the search results

                *Note: If firstName is None, then only the lastName will show on the frame.
        """

        def __init__(self, parent=None, ID: str = None, resultType=None, lastName=None, firstName=None,
                     description=None):
            super().__init__()
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                               QtWidgets.QSizePolicy.Policy.Fixed)
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

            self._gridLayout = QGridLayout(parent)

            self.id = ID
            self._lastName = lastName
            self._firstName = firstName
            self._description = description
            self._type = resultType

            # allows for entities with only one name to use this class
            if firstName is not None:
                nameLabel = ElidedLabel(f'{self._lastName},  {self._firstName}')
            else:
                nameLabel = ElidedLabel(self._lastName)

            self.idLabel = IdLabel(self.id, self.openInfoWindow)

            self._gridLayout.addWidget(self.idLabel, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self._gridLayout.addWidget(nameLabel, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
            self._gridLayout.addWidget(ElidedLabel(self._description), 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

            self._gridLayout.setColumnStretch(0, 1)
            self._gridLayout.setColumnStretch(1, 20)
            self._gridLayout.setColumnStretch(2, 0)

            self.setLayout(self._gridLayout)
            self._window = None

        def openInfoWindow(self):
            if self._type == employeeType:
                self._window = EmployeeInfo(self.id)
                self._window.show()

