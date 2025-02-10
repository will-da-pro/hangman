#!/usr/bin/env python3
import curses
import json
import re

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

    @staticmethod
    def load_json(filename) -> dict:
        with open(filename) as f:
            return json.load(f)

class ImageWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int) -> None:
        super().__init__(width, height, x_pos, y_pos)

        self.images = self.load_json('assets/images.json')["images"]

    def render_image(self) -> int:
        if self.image is None:
            return 1

        if len(self.image) > self.height or len(self.image[0]) > self.width:
            return 2

        for i in range(len(self.image)):
            self.window.addstr(i + 1, 1, self.image[i], curses.color_pair(1))

        self.window.refresh()

        return 0

class WordBankWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int, word: str, guessed_letters: set[str]) -> None:
        super().__init__(width, height, x_pos, y_pos)

        self.word: str = word
        self.guessed_letters: set[str] = guessed_letters

    def render_bank(self):
        for index, letter in enumerate(self.guessed_letters):
            self.window.addch(1, 2 * index + 1, letter, curses.color_pair(1))

        self.window.refresh()

class GameWindow(Window):
    def __init__(self, width: int, height: int, x_pos: int, y_pos: int, word: str, guessed_letters: set[str]) -> None:
        super().__init__(width, height, x_pos, y_pos)

        self.word: str = word
        self.guessed_letters: set[str] = guessed_letters

        self.render_text()

    def render_text(self) -> None:
        text: str = " "

        for letter in self.word.lower():
            if letter in self.guessed_letters:
                text += letter
            else:
                text += "_"

            text += " "

        length: int = len(text) # Should always be odd

        x_pos: int = int((self.width / 2) - (length / 2))
        y_pos: int = 3

        self.window.addstr(y_pos, x_pos, text, curses.color_pair(1))
        self.window.refresh()

class Game:
    def __init__(self, screen) -> None:
        self.word: str = "landon"
        self.input_buffer: str | None = None
        self.guessed_letters: set[str] = {"a", "l"}

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
        word_bank_height: int = 13

        self.word_bank_window: WordBankWindow = WordBankWindow(word_bank_width, word_bank_height, word_bank_x_pos, word_bank_y_pos, self.word, self.guessed_letters)

        game_x_pos: int = int(curses.COLS / 2)
        game_y_pos: int = int(curses.LINES / 2 - 17 + word_bank_height)

        game_width: int = word_bank_width
        game_height: int = image_height - word_bank_height

        self.game_window: GameWindow = GameWindow(game_width, game_height, game_x_pos, game_y_pos, self.word, self.guessed_letters)

    def process_input(self, key) -> None:
        if key == curses.KEY_ENTER:
            if self.input_buffer is None:
                return

            elif self.input_buffer in self.guessed_letters:
                return

            elif self.input_buffer in self.word:
                self.guessed_letters.add(self.input_buffer)
                self.word_bank_window.guessed_letters.add(self.input_buffer)
                self.game_window.guessed_letters.add(self.input_buffer)
                self.input_buffer = None
                return

            else:
                self.guessed_letters.add(self.input_buffer)
                self.word_bank_window.guessed_letters.add(self.input_buffer)
                self.game_window.guessed_letters.add(self.input_buffer)
                self.input_buffer = None
                return
        else:
            letter: str = re.search(r'^[a-z]$', key).group()

            if letter is None:
                return

            else:
                self.input_buffer = key
                return

def main(screen) -> int:
    if curses.COLS < 150 or curses.LINES < 50:
        return 1

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    screen.bkgd(' ', curses.color_pair(1))

    game = Game(screen)

    game.word_bank_window.render_bank()

    i = 1
    while i < 11:
        game.image_window.image = game.image_window.images[str(i)]
        game.image_window.render_image()
        screen.getch()
        i = i + 1

    return 0

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except Exception as e:
        print(e)