import os


def getPath(relative_dir):
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, relative_dir)


DB_PATH = getPath('FSEA.db')
icons = {
    "EXIT_BUTTON": getPath("app\\assets\\exit.png"),
    "RESTORE_BUTTON": getPath("app\\assets\\restore.png"),
    "MINIMIZE_BUTTON": getPath("app\\assets\\minimize.png"),
    "FSEA_LOGO": getPath("app\\assets\\FSEAlogo.png"),
    "COLLAPSED_ARROW": getPath("app\\assets\\arrow_right.png"),
    "EXPANDED_ARROW": getPath("app\\assets\\arrow_drop_down.png")
}
