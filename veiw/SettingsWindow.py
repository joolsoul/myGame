from PyQt5.QtWidgets import QMainWindow
from UI.SettingsWindowUI import *
from Game import *


class SettingsWindow(QMainWindow, Ui_Settings):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: self.close())
        self.pushButton_2.clicked.connect(self.create_new_game)

    def create_new_game(self):
        self.parent().game = Game(self.spinBox.value(), self.spinBox_2.value(), self.spinBox_3.value(),
                                  self.spinBox_4.value())
        self.parent().game_resize(self.parent().game)
        self.parent().update_view()
        self.close()
