#!/usr/bin/env python3

import curses
import json
import time


class Window:
    def __init__(self, width, height, x_pos, y_pos):
        self.width = width
        self.height = height
        self.xPos = x_pos
        self.yPos = y_pos
        self.image = None
        self.window = curses.newwin(self.height, self.width, self.yPos, self.xPos)
        self.window.border(0)
        self.window.refresh()

    def render(self):
        if self.image is None:
            return 1

        if len(self.image) > self.height or len(self.image[0]) > self.width:
            return 2

        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                self.window.addch(i + 1, j + 1, self.image[i][j])
                self.window.refresh()

class ImageWindow(Window):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

        self.images = {}
        self.load_json('assets/images.json')

    def load_json(self, filename):
        with open(filename) as f:
            self.images = json.load(f)['images']

class WordBankWindow(Window):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

class GameWindow(Window):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

class Game():
    def __init__(self, screen):
        curses.use_default_colors()
        curses.curs_set(False)
        screen.refresh()

        image_x_pos = int(curses.COLS / 2 - 66)
        image_y_pos = int(curses.LINES / 2 - 17)

        image_width = 66
        image_height = 34

        self.image_window = ImageWindow(image_width, image_height, image_x_pos, image_y_pos)

        word_bank_x_pos = int(curses.COLS / 2)
        word_bank_y_pos = int(curses.LINES / 2 - 17)

        word_bank_width = 66
        word_bank_height = 10

        self.word_bank_window = WordBankWindow(word_bank_width, word_bank_height, word_bank_x_pos, word_bank_y_pos)

        game_x_pos = int(curses.COLS / 2)
        game_y_pos = int(curses.LINES / 2 - 17 + word_bank_height)

        game_width = word_bank_width
        game_height = image_height - word_bank_height

        self.game_window = GameWindow(game_width, game_height, game_x_pos, game_y_pos)

def main(screen):
    if curses.COLS < 150 or curses.LINES < 50:
        return 1

    game = Game(screen)

    i = 1
    while i < 11:
        game.image_window.image = game.image_window.images[str(i)]
        game.image_window.render()
        screen.getch()
        i = i + 1

if __name__ == '__main__':
    curses.wrapper(main)