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
        self.image = self.images['0']

        self.render_image()

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

        self.render_bank()

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
        self.guessed_letters: set[str] = set()
        self.incorrect_guesses: int = 0
        self.screen = screen

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

    def process_input(self, key: int) -> None:
        if key == 10: # Key code for ENTER
            if self.input_buffer is None:
                return

            elif self.input_buffer in self.guessed_letters:
                return

            elif self.input_buffer in self.word:
                self.guessed_letters.add(self.input_buffer)
                self.word_bank_window.guessed_letters.add(self.input_buffer)
                self.game_window.guessed_letters.add(self.input_buffer)
                self.input_buffer = None

            else:
                self.guessed_letters.add(self.input_buffer)
                self.word_bank_window.guessed_letters.add(self.input_buffer)
                self.game_window.guessed_letters.add(self.input_buffer)
                self.input_buffer = None
                self.incorrect_guesses += 1

            self.image_window.image = self.image_window.images[str(self.incorrect_guesses)]
            self.image_window.render_image()
            self.word_bank_window.render_bank()
            self.game_window.render_text()
        else:
            key_char: chr = chr(key)

            letter: re.Match[str] | None = re.search(r'^[a-z]$', key_char)

            if letter is None:
                return

            else:
                self.input_buffer = key_char
                return

    def game_loop(self) -> None:
        while True:
            key: int = self.screen.getch()
            self.process_input(key)


def main(screen) -> int:
    if curses.COLS < 150 or curses.LINES < 50:
        return 1

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    screen.bkgd(' ', curses.color_pair(1))

    game = Game(screen)

    game.word_bank_window.render_bank()
    game.game_loop()

    # i = 1
    # while i < 11:
    #     game.image_window.image = game.image_window.images[str(i)]
    #     game.image_window.render_image()
    #     key: int = screen.getch()
    #     if key == 10:
    #         return 1
    #
    #     print(chr(key))
    #     i = i + 1

    return 0

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except Exception as e:
        print(e)