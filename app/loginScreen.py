from PyQt6.QtCore import QSize, Qt, QCoreApplication, QPoint
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QGridLayout, QVBoxLayout, QWidget
from app.stylePresets import colors
from utils.filePaths import icons
from utils.authUtils import authenticate


class authWindow(QMainWindow):
    def __init__(self, unlock_this, *args):
        super().__init__()
        self.setFixedSize(QSize(300, 375))
        self.setStyleSheet("background-color: %s;" % (colors["FRAME_COLOR"]))
        self.setWindowTitle("F-SEA Authentication")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.prevPos = None

        # make window borderless
        self.setWindowOpacity(0.9)

        class login_text_entry(QLineEdit):
            def __init__(self):
                super().__init__()
                self.setFixedWidth(150)
                self.setFixedHeight(25)
                self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
                self.setStyleSheet("QLineEdit {border-radius: 10px;"
                                   "border-left: 5px;"
                                   "border-right: 5px;"
                                   "border-top: 3px;"
                                   "border-bottom: 3px;"
                                   "border-color: white;"
                                   "border-style: outset;"
                                   "background-color: white;"
                                   "color: black;}")

        class login_text(QLabel):
            def __init__(self, name):
                super().__init__()
                self.setStyleSheet("color: white")
                self.setText(name)

        # make error message label
        self.errorMsg = QLabel("Credentials not recognized.")
        self.errorMsg.setStyleSheet("color: %s;" % colors["ERROR_MSG"])
        self.errorMsg.hide()

        self.lockoutMsg = QLabel("Account locked.")
        self.lockoutMsg.setStyleSheet("color: %s;" % colors["ERROR_MSG"])
        self.lockoutMsg.hide()

        def auth(user, pswd):
            val = authenticate(user, pswd)

            if val == True:
                self.close()
                unlock_this(*args)

            elif val == False:
                self.lockoutMsg.hide()
                self.errorMsg.show()
            else:
                self.errorMsg.hide()
                self.lockoutMsg.show()

        # make text entry for username and password / add functionality
        self.username = login_text_entry()
        self.username.returnPressed.connect(lambda: auth(self.username.text(), self.password.text()))
        self.password = login_text_entry()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(lambda: auth(self.username.text(), self.password.text()))

        # make text labels for username / login text entry
        self.username_text = login_text("User")
        self.password_text = login_text("Passkey")

        # make label to hold logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap(icons["FSEA_LOGO"])
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # make window close button (because window is borderless)
        self.exit_button = QPushButton()
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)
        self.exit_button.setFixedSize(18, 18)
        self.exit_button.setIcon(QIcon(icons["EXIT_BUTTON"]))
        self.exit_button.setStyleSheet("QPushButton { background-repeat: no-repeat; }"
                                       "QPushButton::pressed { background-color: %s; }" % colors["PUSH_BUTTON_PRESSED_COLOR"])
        self.exit_button.setFlat(True)

        # make submit button
        self.submit_button = QPushButton("Authenticate")
        self.submit_button.setFixedWidth(80)
        self.submit_button.setFixedHeight(25)
        self.submit_button.clicked.connect(lambda: auth(self.username.text(), self.password.text()))
        self.submit_button.setStyleSheet("QPushButton { color: %s;"
                                         "background-color: %s;"
                                         "border: none; }"
                                         "QPushButton::pressed { background-color: %s; }" % (colors["PUSH_BUTTON_TEXT_COLOR"], colors["PUSH_BUTTON_COLOR"], colors["PUSH_BUTTON_PRESSED_COLOR"]))

        # make main_layout grid container to hold other layouts
        self.main_layout = QGridLayout()
        # make exit button container and add exit button to upper right
        self.exit_container = QVBoxLayout()
        self.exit_container.addWidget(self.exit_button,
                                      alignment=(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop))
        # make form container to hold login widgets
        self.form_container = QVBoxLayout()

        # holds exit button container
        self.main_layout.addLayout(self.exit_container, 0, 2, 3, 3)
        # holds login form
        self.main_layout.addLayout(self.form_container, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        # empty container for space on left
        self.main_layout.addLayout(QVBoxLayout(), 0, 0, 3, 3)

        # make first column equal to width of third column to center login form horizontally
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(2, 1)
        # make first row equal to width of third row to center login form vertically
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(2, 1)

        # add form widgets to form container
        self.form_container.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.form_container.addWidget(self.username_text)
        self.form_container.addSpacing(2)
        self.form_container.addWidget(self.username)
        self.form_container.addWidget(self.password_text)
        self.form_container.addSpacing(2)
        self.form_container.addWidget(self.password)
        self.form_container.addSpacing(2)
        self.form_container.addWidget(self.lockoutMsg, alignment=Qt.AlignmentFlag.AlignCenter)
        self.form_container.addWidget(self.errorMsg, alignment=Qt.AlignmentFlag.AlignCenter)
        self.form_container.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # make main window and set the main layout
        self.main_window = QWidget()
        self.main_window.setLayout(self.main_layout)

        self.setCentralWidget(self.main_window)

    def mousePressEvent(self, event):
        if self.exit_button.underMouse():
            pass
        elif self.submit_button.underMouse():
            pass
        else:
            self.prevPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.exit_button.underMouse():
            pass
        elif self.submit_button.underMouse():
            pass
        else:
            delta = QPoint(event.globalPosition().toPoint() - self.prevPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prevPos = event.globalPosition().toPoint()
