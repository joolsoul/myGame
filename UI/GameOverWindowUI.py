
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameOverWindow(object):
    def setupUi(self, GameOverWindow):
        GameOverWindow.setObjectName("GameOverWindow")
        GameOverWindow.resize(264, 108)
        GameOverWindow.setStyleSheet("background-color: rgb(0, 170, 127);")
        self.centralwidget = QtWidgets.QWidget(GameOverWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.new_game_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_game_button.setObjectName("new_game_button")
        self.horizontalLayout.addWidget(self.new_game_button)
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout.addWidget(self.exit_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        GameOverWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(GameOverWindow)
        QtCore.QMetaObject.connectSlotsByName(GameOverWindow)

    def retranslateUi(self, GameOverWindow):
        _translate = QtCore.QCoreApplication.translate
        GameOverWindow.setWindowTitle(_translate("GameOverWindow", "Game Over"))
        self.label.setText(_translate("GameOverWindow", "Game Over!"))
        self.new_game_button.setText(_translate("GameOverWindow", "New game"))
        self.exit_button.setText(_translate("GameOverWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GameOverWindow = QtWidgets.QMainWindow()
    ui = Ui_GameOverWindow()
    ui.setupUi(GameOverWindow)
    GameOverWindow.show()
    sys.exit(app.exec_())
