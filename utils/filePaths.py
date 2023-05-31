import os

project_root = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(project_root, 'FSEA.db')

icons = {
    "EXIT_BUTTON": os.path.join(project_root, "app\\assets\\exit.png"),
    "RESTORE_BUTTON": os.path.join(project_root, "app\\assets\\restore.png"),
    "MINIMIZE_BUTTON": os.path.join(project_root, "app\\assets\\minimize.png"),
    "FSEA_LOGO": os.path.join(project_root, "app\\assets\\FSEAlogo.png")
}

