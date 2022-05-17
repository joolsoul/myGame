import copy
from enum import Enum
import random as rnd
from typing import List, Any

RECORD_RATH = "resources/Record"


class GameState(Enum):
    PLAYING = 0
    FAIL = 1


class Color:
    def __init__(self, r: int, g: int, b: int):
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b


class GameCell:
    def __init__(self, color: Color = None, block: bool = False):
        self._color = color
        self._block = block

    @property
    def color(self):
        return self._color

    @property
    def block(self) -> bool:
        return self._block

    def __str__(self):
        return self._block


class Game:
    def __init__(self, row_count: int, col_count: int, color_count: int, start_level: int):
        self._state = None
        self._row_count = row_count
        self._col_count = col_count
        self._color_count = color_count
        self._colors = []
        self._field = []
        self._level_counter = 0
        self._start_level = start_level
        self._current_level = start_level
        self._record = self.get_record()
        self._score = 0
        self.new_game()

    def new_game(self) -> None:
        self.init_game_field()
        self._state = GameState.PLAYING

    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count

    @property
    def field(self) -> list:
        return self._field

    @property
    def colors(self) -> list:
        return self._colors

    @property
    def color_count(self):
        return self._color_count

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def current_level(self) -> int:
        return self._current_level

    @property
    def level_counter(self) -> int:
        return self._level_counter

    @property
    def score(self) -> int:
        return self._score

    @property
    def record(self) -> int:
        return self._record

    @property
    def level_counter(self) -> int:
        return self._level_counter

    def get_record(self):
        with open(RECORD_RATH) as file:
            record = file.read()
        return int(record)

    def update_level(self):
        self._level_counter += 1
        if self._level_counter == 7:
            self._current_level += 1
            self._level_counter = 0

    def update_score(self, deleted_blocks: list):
        self._score += len(deleted_blocks) ** 2
        if self._score > self._record:
            self._record = self._score
            self.update_record()

    def update_record(self):
        with open(RECORD_RATH, 'w') as file:
            file.write(str(self._record))

    def init_game_field(self):
        self._field = [
            copy.deepcopy([GameCell() for c in range(self.col_count)])
            for r in range(self.row_count)
        ]
        for i in range(self._color_count):
            r = rnd.randint(0, 255)
            g = rnd.randint(0, 255)
            b = rnd.randint(0, 255)
            self._colors.append(Color(r, g, b))

        for row in range(self.row_count):
            for column in range(self.col_count):
                self.add_block(row, column)

    def add_block(self, row, column):
        self.field[row][column]._block = True
        self.field[row][column]._color = rnd.choice(self._colors)

    def update_field(self):
        for row in range(self.row_count):
            for column in range(self.col_count):
                if self.field[row][column].block is False:
                    self.add_block(row, column)

    def get_blocks(self, row, column):
        color = self.field[row][column].color
        blocks = []
        checked = [[False for c in range(self.col_count)] for r in range(self.row_count)]
        self.find_neighbors(row, column, blocks, color, checked)
        return blocks

    def find_neighbors(self, row, column, blocks: list, color: Color, checked: list):
        if row < 0 or row >= len(self.field) or column < 0 or column >= len(self.field[row]) or checked[row][column]:
            return blocks
        else:
            checked[row][column] = True
            if self._field[row][column].block is True and self._field[row][column].color == color:
                blocks.append(self._field[row][column])
                self.find_neighbors(row - 1, column, blocks, color, checked)
                self.find_neighbors(row + 1, column, blocks, color, checked)
                self.find_neighbors(row, column + 1, blocks, color, checked)
                self.find_neighbors(row, column - 1, blocks, color, checked)
                return blocks
            else:
                return blocks

    def remove_blocks(self, blocks_to_remove: list):
        for row in range(len(self.field)):
            for column in range(len(self.field[row])):
                if self.field[row][column] in blocks_to_remove:
                    self.field[row][column] = GameCell()

        for column in range(len(self.field[0])):
            for row in range(len(self.field) - 1, 0, -1):
                if self.field[row][column].block is False:
                    for current_row in range(row - 1, -1, -1):
                        if self.field[current_row][column].block is True:
                            self.field[row][column] = self.field[current_row][column]
                            self.field[current_row][column] = GameCell()
                            break

    def update_playing_state(self):
        if self.is_game_over():
            self._state = GameState.FAIL

    def is_game_over(self):
        for row in range(self.row_count):
            for column in range(self.col_count):
                if len(self.get_blocks(row, column)) > 1:
                    return False
        return True

    def on_button_click(self, row: int, col: int):
        if self.state != GameState.PLAYING:
            return
        cell = self.field[row][col]
        blocks = self.get_blocks(row, col)
        block_level = len(blocks)
        if not cell.block or block_level == 1:
            return
        else:
            self.remove_blocks(blocks)
            self.update_score(blocks)
            if block_level >= self._current_level:
                self.update_level()
                self.update_field()
        self.update_playing_state()
