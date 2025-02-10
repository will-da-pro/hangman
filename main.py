#!/usr/bin/env python3
import curses
import json

class Window:
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int) -> None:
        self.width: int = width
        self.height: int = height
        self.xPos: int = x_pos
        self.yPos: int = y_pos
        self.image = None
        self.window = curses.newwin(self.height, self.width, self.yPos, self.xPos)
        self.window.bkgd(' ', curses.color_pair(2))
        self.window.border(0)
        self.window.refresh()

    def render_image(self) -> int:
        if self.image is None:
            return 1

        if len(self.image) > self.height or len(self.image[0]) > self.width:
            return 2

        for i in range(len(self.image)):
            self.window.addstr(i + 1, 1, self.image[i], curses.color_pair(1))
            self.window.refresh()

        return 0

class ImageWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int) -> None:
        super().__init__(width, height, x_pos, y_pos)

        self.images = {}
        self.load_json('assets/images.json')

    def load_json(self, filename) -> None:
        with open(filename) as f:
            self.images = json.load(f)['images']

class WordBankWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int, word: str) -> None:
        super().__init__(width, height, x_pos, y_pos)

        self.word: str = word

class GameWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int, word: str) -> None:
        super().__init__(width, height, x_pos, y_pos)
        self.word: str = word

    def process_input(self, key):
        pass

class Game:
    def __init__(self, screen) -> None:
        word: str = "landon"
        curses.curs_set(False)
        screen.refresh()

        image_x_pos: int = int(curses.COLS / 2 - 66)
        image_y_pos: int = int(curses.LINES / 2 - 17)

        image_width: int = 66
        image_height: int = 34

        self.image_window: ImageWindow = ImageWindow(image_width, image_height, image_x_pos, image_y_pos)

        word_bank_x_pos: int = int(curses.COLS / 2)
        word_bank_y_pos: int = int(curses.LINES / 2 - 17)

        word_bank_width: int = 66
        word_bank_height: int = 10

        self.word_bank_window: WordBankWindow = WordBankWindow(word_bank_width, word_bank_height, word_bank_x_pos, word_bank_y_pos, word)

        game_x_pos: int = int(curses.COLS / 2)
        game_y_pos: int = int(curses.LINES / 2 - 17 + word_bank_height)

        game_width: int = word_bank_width
        game_height: int = image_height - word_bank_height

        self.game_window: GameWindow = GameWindow(game_width, game_height, game_x_pos, game_y_pos, word)

def main(screen) -> int:
    if curses.COLS < 150 or curses.LINES < 50:
        return 1

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    screen.bkgd(' ', curses.color_pair(1))

    game = Game(screen)

    i = 1
    while i < 11:
        game.image_window.image = game.image_window.images[str(i)]
        game.image_window.render_image()
        screen.getch()
        i = i + 1

    return 0

if __name__ == '__main__':
    curses.wrapper(main)