import os


def getPath(relative_dir):
    project_root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(project_root, relative_dir)


DB_PATH = getPath('FSEA.db')
icons = {
    "EXIT_BUTTON": getPath("src\\assets\\exit.png"),
    "RESTORE_BUTTON": getPath("src\\assets\\restore.png"),
    "MINIMIZE_BUTTON": getPath("src\\assets\\minimize.png"),
    "FSEA_LOGO": getPath("src\\assets\\FSEAlogo.png"),
    "COLLAPSED_ARROW": getPath("src\\assets\\arrow_right.png"),
    "EXPANDED_ARROW": getPath("src\\assets\\arrow_drop_down.png")
}
