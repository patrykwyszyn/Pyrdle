import collections
import random
import sys

import pygame

from UI.choose_mode_button import ChooseModeButton
from UI.indicator import Indicator
from UI.letter import Letter
from typing import List, Dict

from constants import Constants
from file_reader import FileReader
from models.color import Color
from models.game_result import GameResult
from models.letter_in_word import LetterInWord
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
    running: bool  # For main game loop.
    is_locked: bool  # Whether the inputs are locked. This happens during animations.
    anim_events: Dict[int, Letter]  # Stores event id with its corresponding letter.
    chosen_mode: Mode

    def __init__(self, chosen_language="english", chosen_mode: Mode = Mode.EASY):
        self.file_reader = FileReader(chosen_language)
        self.running = True

        background_path = self.set_mode_configuration(chosen_mode)
        window_height: int = Constants.HEIGHT if self.file_reader.language_specific_letters == "" else Constants.HEIGHT_EXT

        Ui(window_height, background_path)

        self.draw_new_word()
        self.indicators = []
        self.choose_mode_buttons = []
        self.guesses = [[]] * 6
        self.guesses_count: int = 0
        self.game_result = GameResult.NOT_DECIDED
        self.is_locked = False
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter
        self.anim_events = {}
        self.unlock_event = 0

        self.initialize_keyboard()

    def set_mode_configuration(self, chosen_mode: Mode):
        self.chosen_mode = chosen_mode
        self.words = self.file_reader.get_words(chosen_mode)
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

    def initialize_choose_mode_buttons(self):
        mode_colors = {Mode.EASY: Color.OUTLINE, Mode.MEDIUM: Color.OUTLINE, Mode.HARD: Color.OUTLINE, self.chosen_mode: Color.GREEN}
        self.choose_mode_buttons.append(ChooseModeButton(Constants.WIDTH - 105, 5, Mode.EASY, mode_colors[Mode.EASY]))
        self.choose_mode_buttons.append(ChooseModeButton(Constants.WIDTH - 215, 5, Mode.MEDIUM, mode_colors[Mode.MEDIUM]))
        self.choose_mode_buttons.append(ChooseModeButton(Constants.WIDTH - 325, 5, Mode.HARD, mode_colors[Mode.HARD]))

    def initialize_keyboard(self):
        indicator_position_y = Constants.FIRST_INDICATOR_POSITION_Y
        x_offset = 0
        for i in range(3):
            x_offset = (Constants.WIDTH - len(BASIC_INDICATORS[i]) * 60)/2
            if i == 2:
                enter = Indicator(x_offset - 91, indicator_position_y, "Enter", 100 - Constants.LETTER_Y_SPACING)
                self.indicators.append(enter)

            for letter in BASIC_INDICATORS[i]:
                new_indicator = Indicator(x_offset, indicator_position_y, letter)
                self.indicators.append(new_indicator)
                x_offset += 60
            indicator_position_y += 90

        enter = Indicator(x_offset, indicator_position_y-90, "BckSp", 100)
        self.indicators.append(enter)

        x_offset = (Constants.WIDTH - len(self.file_reader.language_specific_letters) * 60)/2
        for letter in self.file_reader.language_specific_letters:
            new_indicator = Indicator(x_offset, indicator_position_y, letter)
            self.indicators.append(new_indicator)
            x_offset += 60

    def draw_new_word(self):
        self.word = random.choice(self.words)

    def is_valid_word(self, word: str):
        return word in self.words

    def reset(self):
        Ui.reset_ui()
        self.guesses_count = 0
        self.draw_new_word()
        self.guesses: List[List[Letter]] = [[]] * 6
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = GameResult.NOT_DECIDED
        Ui.force_display_update()
        for indicator in self.indicators:
            indicator.bg_color = Color.OUTLINE
            indicator.draw()

    def create_new_letter(self, key_pressed):
        self.current_guess_string += key_pressed
        new_letter = Letter(key_pressed, (self.current_letter_bg_x, self.guesses_count * 100 + Constants.LETTER_X_SPACING - 40))
        self.current_letter_bg_x += Constants.LETTER_X_SPACING
        self.guesses[self.guesses_count].append(new_letter)
        self.current_guess.append(new_letter)
        for guess in self.guesses:
            for letter in guess:
                letter.draw()

    def delete_letter(self):
        if len(self.current_guess_string) <= 0:
            return
        self.guesses[self.guesses_count][-1].delete()
        self.guesses[self.guesses_count].pop()
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.current_letter_bg_x -= Constants.LETTER_X_SPACING

    @staticmethod
    def get_frequency_of_letters_in_guessed_word(guess_to_check: List[Letter]) -> Dict[str, int]:
        letters = [x.character for x in guess_to_check]
        return collections.Counter(letters)

    def get_frequency_of_letters_in_correct_word(self):
        return collections.Counter(self.word.upper())

    def update_indicator(self, letter: str, color: Color):
        for indicator in self.indicators:
            if indicator.text == letter and indicator.bg_color == Color.OUTLINE:
                indicator.bg_color = color
                indicator.draw()

    def update_letter(self, letter: Letter, color: Color):
        self.update_indicator(letter.character, color)
        letter.schedule_params(color, Color.WHITE)

        letter.draw()
        Ui.force_display_update()

    def prepare_for_the_next_guess(self):
        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter

    @staticmethod
    def get_letters_with_position(guess_to_check: List[Letter]) -> List[LetterInWord]:
        guess_letters: List[LetterInWord] = []
        for i in range(len(guess_to_check)):
            guess_letters.append(LetterInWord(guess_to_check[i], i))
        return guess_letters

    def check_guess(self, guess_word: List[Letter]):
        self.is_locked = True
        frequency_of_letters_in_correct_word = self.get_frequency_of_letters_in_correct_word()
        frequency_of_letters_in_guessed_word = self.get_frequency_of_letters_in_guessed_word(guess_word)
        guess_letters: List[LetterInWord] = self.get_letters_with_position(guess_word)
        guess_word_copy = guess_word.copy()

        for guess_letter in guess_letters.copy():
            if guess_letter.letter.character.lower() == self.word[guess_letter.index]:
                self.update_letter(guess_letter.letter, Color.GREEN)
                self.game_result = GameResult.WIN

                guess_letters.remove(guess_letter)
                frequency_of_letters_in_correct_word[guess_letter.letter.character] -= 1
                frequency_of_letters_in_guessed_word[guess_letter.letter.character] -= 1

        for guess_letter in guess_letters.copy():
            if guess_letter.letter.character.lower() in self.word and frequency_of_letters_in_correct_word[guess_letter.letter.character] > 0:
                self.update_letter(guess_letter.letter, Color.YELLOW)
                self.game_result = GameResult.NOT_DECIDED

                frequency_of_letters_in_correct_word[guess_letter.letter.character] -= 1
                frequency_of_letters_in_guessed_word[guess_letter.letter.character] -= 1
                guess_letters.remove(guess_letter)

        for guess_letter in guess_letters:
            self.update_letter(guess_letter.letter, Color.GREY)
            self.game_result = GameResult.NOT_DECIDED

        if self.guesses_count == 5 and self.game_result == GameResult.NOT_DECIDED:
            self.game_result = GameResult.LOSE
        self.prepare_for_the_next_guess()

        # After all the letters have been processed, prepare their animation.
        self.anim_events = {}
        for i in range(self.number_of_letters):
            letter_event = pygame.event.Event(pygame.event.custom_type())
            pygame.time.set_timer(letter_event, i * 300 + 1)  # +1 so that the timer doesn't get disabled on 0.
            self.anim_events[letter_event.type] = guess_word_copy[i]

            # If this is the last letter, create another event which will unlock inputs.
            if i == self.number_of_letters - 1:
                # unlock_event = pygame.event.Event(pygame.USEREVENT + i + 2)
                unlock_event = pygame.event.Event(pygame.event.custom_type())
                pygame.time.set_timer(unlock_event, i * 300 + 300)
                self.unlock_event = unlock_event.type


    def play_again(self):
        frame_x = 10
        frame_y = 620
        frame_width = 1000
        frame_height = 600

        frame_rect = (frame_x, frame_y, frame_width, frame_height)
        Ui.display_game_over_frame(frame_rect, "Press ENTER to play again!", f"The word was {self.word.upper()}!")

    def handle_keyboard_pressed_event(self, event):
        if event.key == pygame.K_RETURN:
            self.check_word()
        elif event.key == pygame.K_BACKSPACE:
            self.delete_letter()
        else:
            self.insert_letter(event.unicode.upper())

    def handle_mouse_clicked_event(self, event):
        key_pressed = ""
        for choose_mode in self.choose_mode_buttons:
            if choose_mode.is_point_colliding(event.pos):
                self.update_configuration(choose_mode.text)
                self.reset()
                return
        for indicator in self.indicators:
            if indicator.is_point_colliding(event.pos):
                key_pressed = indicator.text
        if key_pressed == "Enter":
            self.check_word()
        elif key_pressed == "BckSp":
            self.delete_letter()
        else:
            self.insert_letter(key_pressed)

    def check_word(self):
        if self.game_result != GameResult.NOT_DECIDED:
            self.reset()
        else:
            if len(self.current_guess_string) == self.number_of_letters and self.current_guess_string.lower() in self.words:
                self.check_guess(self.current_guess)

    def insert_letter(self, key_pressed):
        if key_pressed in self.file_reader.alphabet and key_pressed != "":
            if len(self.current_guess_string) < self.number_of_letters:
                self.create_new_letter(key_pressed)

    def check_game_complete(self):
        if self.game_result != GameResult.NOT_DECIDED:
            self.play_again()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_clicked_event(event)
                return
            if event.type == pygame.KEYDOWN and not self.is_locked:
                self.handle_keyboard_pressed_event(event)
                return
            if event.type == self.unlock_event:
                self.is_locked = False
                return
            if event.type in self.anim_events.keys():
                if isinstance(self.anim_events[event.type], Letter):
                    self.anim_events[event.type].start_animation()
                    pygame.time.set_timer(event.type, 0)  # Disable the timer.

    def update(self, delta_time):
        for guess in self.guesses:
            for letter in guess:
                letter.update(delta_time)

    def play(self):
        clock = pygame.time.Clock()
        fps = 144
        self.running = True
        while self.running:
            self.initialize_choose_mode_buttons()  # Move out of here after test.
            delta_time = clock.tick(fps) / 1000
            self.check_game_complete()
            self.handle_events()
            self.update(delta_time)
            pygame.display.update()

        pygame.quit()
        sys.exit()
