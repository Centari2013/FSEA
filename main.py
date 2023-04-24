import sys
from bulk.loginScreen import authenticate
from bulk.fseaDatabaseOptions import database_options
from PyQt6.QtWidgets import QApplication
from bulk.baseWindows import windowWithToolbar

app = QApplication(sys.argv)
options = database_options()
#options.show()
# launch login window; options is passed as the window to unlock
login = authenticate(options.show)
login.show()
app.exec()

