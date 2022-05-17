from PyQt5.QtWidgets import QMainWindow
from UI.GameOverWindowUI import *
from Game import *


class GameOverWindow(QMainWindow, Ui_GameOverWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.exit_button.clicked.connect(self.close_all)
        self.new_game_button.clicked.connect(self.new_game)

    def new_game(self):
        self.parent().open_settings()
        self.close()

    def close_all(self):
        self.close()
        self.parent().close()
