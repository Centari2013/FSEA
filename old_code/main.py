import sys
from old_code.src.loginScreen import authWindow
from old_code.src.fseaDatabaseOptions import database_options
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
options = database_options()
#options.show()
# launch login window; options is passed as the window to unlock
login = authWindow(options.show)
login.show()
login.username.setFocus()
app.exec()

