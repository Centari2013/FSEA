from bulk.login_screen import authenticate
from bulk.fsea_database_options import database_options
from PyQt6.QtWidgets import QApplication

app = QApplication([])
options = database_options()
options.show()
# launch login window; options is passed as the window to unlock
# login = authenticate(options.show)
# login.show()
app.exec()

