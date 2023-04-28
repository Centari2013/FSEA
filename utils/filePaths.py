import os

project_root = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(project_root, 'FSEA.db')

icons = {
    "EXIT_BUTTON": os.path.join(project_root, "bulk\\assets\\exit.png"),
    "RESTORE_BUTTON": os.path.join(project_root, "bulk\\assets\\restore.png"),
    "MINIMIZE_BUTTON": os.path.join(project_root, "bulk\\assets\\minimize.png"),
    "FSEA_LOGO": os.path.join(project_root, "bulk\\assets\\FSEAlogo.png")
}

