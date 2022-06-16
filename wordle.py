import collections
import random
import sys
import pygame

from typing import List
from constants import Constants
from indicator import Indicator
from letter import Letter
from models.color import Color
from file_reader import FileReader
from models.mode import Mode
from UI.ui import Ui

BASIC_INDICATORS: List[str] = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]


class Wordle:
    word: str
    words: List[str]
    file_reader: FileReader
    starting_offset_for_letter: int
    number_of_letters: int
    words: List[str]

    def __init__(self, chosen_language="english", chosen_mode: Mode = Mode.EASY):
        self.file_reader = FileReader(chosen_language)

        background_path = self.set_mode_configuration(chosen_mode)
        window_height: int = Constants.HEIGHT if self.file_reader.language_specific_letters == "" else Constants.HEIGHT_EXT

        Ui(window_height, background_path)

        self.draw_new_word()
        self.indicators = []
        self.guesses = [[]] * 6
        self.guesses_count: int = 0
        self.game_result = ""
        self.game_decided = False
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter

        self.initialize_keyboard()

    def set_mode_configuration(self, chosen_mode: Mode):
        self.words = self.file_reader.get_words(chosen_mode)
        print(self.words)
        if chosen_mode == Mode.EASY:
            self.starting_offset_for_letter = Constants.EASY_MODE_OFFSET
            self.number_of_letters = Constants.EASY_MODE_LETTERS
            return Constants.EASY_MODE_BACKGROUND_PATH
        elif chosen_mode == Mode.MEDIUM:
            self.starting_offset_for_letter = Constants.MEDIUM_MODE_OFFSET
            self.number_of_letters = Constants.MEDIUM_MODE_LETTERS
            return Constants.MEDIUM_MODE_BACKGROUND_PATH
        else:
            self.starting_offset_for_letter = Constants.HARD_MODE_OFFSET
            self.number_of_letters = Constants.HARD_MODE_LETTERS
            return Constants.HARD_MODE_BACKGROUND_PATH

    def update_configuration(self, chosen_mode):
        background_path = self.set_mode_configuration(chosen_mode)
        self.current_letter_bg_x = self.starting_offset_for_letter
        Ui.update_background(background_path)

    def initialize_keyboard(self):
        indicator_position_y = Constants.FIRST_INDICATOR_POSITION_Y
        for i in range(3):
            x_offset = (Constants.WIDTH - len(BASIC_INDICATORS[i]) * 60)/2
            for letter in BASIC_INDICATORS[i]:
                new_indicator = Indicator(x_offset, indicator_position_y, letter)
                self.indicators.append(new_indicator)
                x_offset += 60
            indicator_position_y += 100

        x_offset = (Constants.WIDTH - len(self.file_reader.language_specific_letters) * 60)/2
        for letter in self.file_reader.language_specific_letters:
            new_indicator = Indicator(x_offset, indicator_position_y, letter)
            self.indicators.append(new_indicator)
            x_offset += 60

    def draw_new_word(self):
        self.word = random.choice(self.words)
        counter = collections.Counter(self.word)
        if any(value > 1 for value in counter.values()):
            return self.draw_new_word()
        return

    def is_valid_word(self, word: str):
        return word in self.words

    def reset(self):
        self.update_configuration(Mode.MEDIUM)  # just checkin if changing mode after game works (it did)
        Ui.reset_ui()
        self.guesses_count = 0
        self.draw_new_word()
        self.guesses: List[List[Letter]] = [[]] * 6
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        Ui.force_display_update()
        for indicator in self.indicators:
            indicator.bg_color = Color.OUTLINE
            indicator.draw()

    def create_new_letter(self, key_pressed):
        self.current_guess_string += key_pressed
        new_letter = Letter(key_pressed, (self.current_letter_bg_x, self.guesses_count * 100 + Constants.LETTER_X_SPACING - 50))
        self.current_letter_bg_x += Constants.LETTER_X_SPACING
        self.guesses[self.guesses_count].append(new_letter)
        self.current_guess.append(new_letter)
        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        self.guesses[self.guesses_count][-1].delete()
        self.guesses[self.guesses_count].pop()
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.current_letter_bg_x -= Constants.LETTER_X_SPACING

    def check_guess(self, guess_to_check):
        self.game_decided = False
        for i in range(self.number_of_letters):
            lowercase_letter = guess_to_check[i].character.lower()
            if lowercase_letter in self.word:
                if lowercase_letter == self.word[i]:
                    guess_to_check[i].bg_color = Color.GREEN
                    for indicator in self.indicators:
                        if indicator.text == lowercase_letter.upper():
                            indicator.bg_color = Color.GREEN
                            indicator.draw()
                    guess_to_check[i].text_color = "white"
                    if not self.game_decided:
                        self.game_result = "W"
                else:
                    guess_to_check[i].bg_color = Color.YELLOW
                    for indicator in self.indicators:
                        if indicator.text == lowercase_letter.upper():
                            indicator.bg_color = Color.YELLOW
                            indicator.draw()
                    guess_to_check[i].text_color = "white"
                    self.game_result = ""
                    self.game_decided = True
            else:
                guess_to_check[i].bg_color = Color.GREY
                for indicator in self.indicators:
                    if indicator.text == lowercase_letter.upper():
                        indicator.bg_color = Color.GREY
                        indicator.draw()
                guess_to_check[i].text_color = "white"
                self.game_result = ""
                self.game_decided = True
            guess_to_check[i].draw()
            Ui.force_display_update()

        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter

        if self.guesses_count == 6 and self.game_result == "":
            self.game_result = "L"

    def play_again(self):
        frame_x = 10
        frame_y = 600
        frame_width = 1000
        frame_height = 600

        frame_rect = (frame_x, frame_y, frame_width, frame_height)
        Ui.display_game_over_frame(frame_rect, "Press ENTER to play again!", f"The word was {self.word}!")

    def play(self):
        while True:
            if self.game_result != "":
                self.play_again()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_result != "":
                            self.reset()
                        else:
                            if len(self.current_guess_string) == self.number_of_letters and self.current_guess_string.lower() in self.words:
                                self.check_guess(self.current_guess)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.current_guess_string) > 0:
                            self.delete_letter()
                    else:
                        key_pressed = event.unicode.upper()
                        if key_pressed in self.file_reader.alphabet and key_pressed != "":
                            if len(self.current_guess_string) < self.number_of_letters:
                                self.create_new_letter(key_pressed)

    # add button to change mode
    # https://pythonprogramming.altervista.org/buttons-in-pygame/?doing_wp_cron=1655241290.0790948867797851562500
