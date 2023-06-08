import sys
from app.loginScreen import authWindow
from app.fseaDatabaseOptions import database_options
from PyQt6.QtWidgets import QApplication
from app.baseWindows import windowWithTitleBar

app = QApplication(sys.argv)
options = database_options()
#options.show()
# launch login window; options is passed as the window to unlock
login = authWindow(options.show)
login.show()
login.username.setFocus()
app.exec()

