from bulk.login_screen import authenticate
from bulk.fsea_database_options import database_options
from PyQt5.QtWidgets import QApplication

app = QApplication([])
options = database_options()
login = authenticate(options.show)
login.show()
app.exec()

