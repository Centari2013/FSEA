from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from utils.authUtils import authenticate as auth


def authentication(username, password):
    try:
        if auth(username, password):
            print("AUTHENTICATION SUCCESSFUL")
            return True
        else:
            print("AUTHENTICATION UNSUCCESSFUL")
            return False

    except:
        return False


class authenticate(QMainWindow):
    def __init__(self, unlock_this, *args):
        super().__init__()
        self.setFixedSize(QSize(300, 375))
        self.setStyleSheet("background-color: #31353D;")
        self.setWindowTitle("F-SEA Authentication")

        # make window borderless
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.85)

        class login_text_entry(QLineEdit):
            def __init__(self):
                super().__init__()
                self.setFixedWidth(150)
                self.setFixedHeight(20)
                self.setAlignment(Qt.AlignVCenter)
                self.setStyleSheet("QLineEdit {border-radius: 10px;"
                                   "border-left: 5px;"
                                   "border-right: 5px;"
                                   "border-top: 3px;"
                                   "border-bottom: 3px;"
                                   "border-color: white;"
                                   "border-style: outset;"
                                   "background-color: white;}")

        class login_text(QLabel):
            def __init__(self, name):
                super().__init__()
                self.setStyleSheet("color: white")
                self.setText(name)
        # make error message label
        errorMsg = QLabel("Credentials not recognized.")
        errorMsg.setStyleSheet("color: #E85D04;")
        errorMsg.hide()

        def auth(user, pswd):
            good = authentication(user, pswd)
            if not good:
                errorMsg.show()
            else:
                self.close()
                unlock_this(*args)

        # make text entry for username and password / add functionality
        username = login_text_entry()
        username.returnPressed.connect(lambda: auth(username.text(), password.text()))
        password = login_text_entry()
        password.setEchoMode(2)
        password.returnPressed.connect(lambda: auth(username.text(), password.text()))

        # make text labels for username / login text entry
        username_text = login_text("User")
        password_text = login_text("Passkey")

        # make label to hold logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('bulk/assets/F-SEAlogo.png')
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # make window close button (because window is borderless)
        exit_button = QPushButton()
        exit_button.clicked.connect(QCoreApplication.instance().quit)
        exit_button.setFixedSize(18, 18)
        exit_button.setStyleSheet("QPushButton { border-image: url(bulk/assets/closeButton.png);"
                                  "background-repeat: no-repeat; }"
                                  "QPushButton::pressed { background-color: #242830; }")
        exit_button.setFlat(True)

        # make submit button
        submit_button = QPushButton("Authenticate")
        submit_button.setFixedWidth(80)
        submit_button.setFixedHeight(25)
        submit_button.clicked.connect(lambda: auth(username.text(), password.text()))
        submit_button.setStyleSheet("QPushButton { color: white;"
                                    "background-color: #262829;"
                                    "border: none; }"
                                    "QPushButton::pressed { background-color: #111314; }")

        # make main_layout grid container to hold other layouts
        main_layout = QGridLayout()
        # make exit button container and add exit button to upper right
        exit_container = QVBoxLayout()
        exit_container.addWidget(exit_button, alignment=(Qt.AlignRight | Qt.AlignTop))
        # make form container to hold login widgets
        form_container = QVBoxLayout()

        # holds exit button container
        main_layout.addLayout(exit_container, 0, 2, 3, 3)
        # holds login form
        main_layout.addLayout(form_container, 1, 1, alignment=Qt.AlignCenter)
        # empty container for space on left
        main_layout.addLayout(QVBoxLayout(), 0, 0, 3, 3)

        # make first column equal to width of third column to center login form horizontally
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(2, 1)
        # make first row equal to width of third row to center login form vertically
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(2, 1)

        # add form widgets to form container
        form_container.addWidget(logo_label, alignment=Qt.AlignCenter)
        form_container.addWidget(username_text)
        form_container.addSpacing(2)
        form_container.addWidget(username)
        form_container.addWidget(password_text)
        form_container.addSpacing(2)
        form_container.addWidget(password)
        form_container.addSpacing(2)
        form_container.addWidget(errorMsg, alignment=Qt.AlignCenter)
        form_container.addWidget(submit_button, alignment=Qt.AlignCenter)

        # make main window and set the main layout
        main_window = QWidget()
        main_window.setLayout(main_layout)

        self.setCentralWidget(main_window)
        self.prevPos = self.pos()

    def mousePressEvent(self, event):
        self.prevPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.prevPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.prevPos = event.globalPos()



