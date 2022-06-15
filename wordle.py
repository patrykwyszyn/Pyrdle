import collections
import random
import sys
from typing import List

import pygame

from constants import Constants
from indicator import Indicator
from letter import Letter
from models.color import Color
from file_reader import FileReader

pygame.init()

ICON = pygame.image.load(Constants.ICON_PATH)

GUESSED_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 25)


class Wordle:
    word: str
    words: List[str]
    file_reader: FileReader
    starting_offset_for_letter: int
    number_of_letters: int
    words: List[str]

    def __init__(self, chosen_mode="EASY", chosen_language="english"):
        self.file_reader = FileReader(chosen_language)

        background_path = self.set_mode_configuration(chosen_mode)

        self.BACKGROUND = pygame.image.load(background_path)
        self.BACKGROUND_RECT = self.BACKGROUND.get_rect(center=(318, 323))
        self.SCREEN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
        self.SCREEN.fill("white")
        self.SCREEN.blit(self.BACKGROUND, self.BACKGROUND_RECT)
        pygame.display.set_caption(Constants.WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        pygame.display.update()

        self.draw_new_word()
        self.indicators = []
        self.guesses = [[]] * 6
        self.guesses_count: int = 0
        self.game_result = ""
        self.game_decided = False
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter
        self.indicator_x = 20
        self.indicator_y = 630
        self.alphabet = self.file_reader.get_alphabet_in_parts() if self.file_reader else []

        self.initialize_keyboard()

    def set_mode_configuration(self, chosen_mode: str):
        if chosen_mode == "EASY":
            self.starting_offset_for_letter = Constants.HARD_MODE_OFFSET
            self.number_of_letters = Constants.HARD_MODE_LETTERS
            self.words = self.file_reader.hard_mode_words
            return Constants.HARD_MODE_BACKGROUND_PATH
        elif chosen_mode == "MEDIUM":
            self.starting_offset_for_letter = Constants.MEDIUM_MODE_OFFSET
            self.number_of_letters = Constants.MEDIUM_MODE_LETTERS
            self.words = self.file_reader.medium_mode_words
            return Constants.MEDIUM_MODE_BACKGROUND_PATH
        else:
            self.starting_offset_for_letter = Constants.EASY_MODE_OFFSET
            self.number_of_letters = Constants.EASY_MODE_LETTERS
            self.words = self.file_reader.easy_mode_words
            return Constants.EASY_MODE_BACKGROUND_PATH

    def update_configuration(self, chosen_mode):
        background_path = self.set_mode_configuration(chosen_mode)
        self.current_letter_bg_x = self.starting_offset_for_letter
        self.BACKGROUND = pygame.image.load(background_path)
        self.BACKGROUND_RECT = self.BACKGROUND.get_rect(center=(318, 323))

    def initialize_keyboard(self):
        for i in range(3):
            for letter in self.alphabet[i]:
                new_indicator = Indicator(self.indicator_x, self.indicator_y, letter, self.SCREEN)
                self.indicators.append(new_indicator)
                new_indicator.draw()
                self.indicator_x += 60
            self.indicator_y += 100
            self.indicator_x = 20
        # maybe add logic to center each indicator

    def draw_new_word(self):
        self.word = random.choice(self.words)
        counter = collections.Counter(self.word)
        if any(value > 1 for value in counter.values()):
            return self.draw_new_word()
        return

    def valid_word(self, word: str):
        return word in self.words

    def reset(self):
        self.SCREEN.fill("white")
        self.update_configuration("MEDIUM") #just checkin if changing mode after game works (it did)
        self.SCREEN.blit(self.BACKGROUND, self.BACKGROUND_RECT)
        self.guesses_count = 0
        self.draw_new_word()
        self.guesses: List[List[Letter]] = [[]] * 6
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = ""
        pygame.display.update()
        for indicator in self.indicators:
            indicator.bg_color = Color.OUTLINE
            indicator.draw()

    def create_new_letter(self, key_pressed):
        self.current_guess_string += key_pressed
        new_letter = Letter(key_pressed, (self.current_letter_bg_x, self.guesses_count * 100 + Constants.LETTER_X_SPACING - 50), self.SCREEN)
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
            lowercase_letter = guess_to_check[i].text.lower()
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
            pygame.display.update()

        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter

        if self.guesses_count == 6 and self.game_result == "":
            self.game_result = "L"

    def play_again(self):

        pygame.draw.rect(self.SCREEN, "white", (10, 600, 1000, 600))
        play_again_font = pygame.font.Font("resources/FreeSansBold.otf", 40)
        play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
        play_again_rect = play_again_text.get_rect(center=(Constants.WIDTH / 2, 700))
        word_was_text = play_again_font.render(f"The word was {self.word}!", True, "black")
        word_was_rect = word_was_text.get_rect(center=(Constants.WIDTH / 2, 650))
        self.SCREEN.blit(word_was_text, word_was_rect)
        self.SCREEN.blit(play_again_text, play_again_rect)
        pygame.display.update()

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