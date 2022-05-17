from UI.MainWindowUI import Ui_Game as GameUI
from Game import *

from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel, QColor
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, Qt
from veiw.SettingsWindow import SettingsWindow
from veiw.GameOverWindow import *

class MainWindow(QMainWindow, GameUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.game = Game(11, 8, 4, 2)
        self.game_resize(self.game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.game_field.setItemDelegate(MyDelegate(self))

        def new_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.game_field.indexAt(e.pos())
            self.on_item_clicked(idx, e)

        self.game_field.mousePressEvent = new_mouse_press_event

        self.actionExit.triggered.connect(lambda: self.close())
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionNew_game.triggered.connect(self.new_game)

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.row_count, game.col_count)
        self.game_field.setModel(model)
        self.level_number.setText(str(self.game.current_level))
        self.record_number.display(self.game.record)
        self.score_number.display(self.game.score)
        self.level_number.setText(str(self.game.current_level))
        self.resize(game.col_count * 50 + 20, game.row_count * 50 + 116)
        self.update_view()

    def open_settings(self):
        SettingsWindow(self).show()

    def new_game(self):
        self.game = Game(self.game.row_count, self.game.col_count, self.game.color_count, self.game._start_level)
        self.level_number.setText(str(self.game.current_level))
        self.record_number.display(self.game.record)
        self.score_number.display(self.game.score)
        self.level_progress.setValue(int(self.game.level_counter * 100 / 7))
        self.update_view()

    def update_view(self):
        self.game_field.viewport().update()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        cell = self.game.field[e.row()][e.column()]
        if not cell.block:
            painter.setBrush(Qt.gray)
        else:
            color = cell.color
            painter.setBrush(QColor(color.r, color.g, color.b))
        painter.drawRect(option.rect)

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton or me.button() == Qt.RightButton:
            self.game.on_button_click(e.row(), e.column())
            self.is_game_over()
            self.level_number.setText(str(self.game.current_level))
            self.record_number.display(self.game.record)
            self.score_number.display(self.game.score)
            self.level_progress.setValue(int(self.game.level_counter * 100 / 7))
        self.update_view()

    def is_game_over(self):
        if self.game.state is GameState.FAIL:
            GameOverWindow(self).show()


