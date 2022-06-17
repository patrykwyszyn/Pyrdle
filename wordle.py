import collections
import random
import sys
import threading
import time

import pygame

from UI.choose_mode_button import ChooseModeButton
from UI.indicator import Indicator
from UI.letterbox import LetterBox
from UI.ui import Ui
from models.color import Color
from models.game_result import GameResult
from models.letter_in_word import LetterInWord
from models.difficulty import Difficulty
from typing import List, Dict
from constants import Constants
from file_reader import FileReader

SWOOSH_SFX = pygame.mixer.Sound("resources/sounds/letter_swoosh.ogg")
AMBIENCE_OST = "resources/sounds/ambience.ogg"
LETTERBOX_ANIM_FREQ = 250


# Feel free to refactor this @Patryk Wyszynski. Another threaded method is inside the Wordle class.
def flip_anim_triggerer(trigger_time, letterbox):
    time.sleep(trigger_time/1000)  # time.sleep() requires seconds.
    pygame.mixer.Sound.play(SWOOSH_SFX)
    letterbox.start_flip_animation()


def shake_anim_triggerer(letterbox):
    letterbox.start_shake_animation()

class Wordle:
    word: str
    words: List[str]
    file_reader: FileReader
    starting_offset_for_letter: int
    number_of_letters: int
    words: List[str]
    running: bool
    chosen_difficulty: Difficulty

    def __init__(self, chosen_language="english", chosen_difficulty: Difficulty = Difficulty.EASY):
        # Setup window, difficulty and UI.
        self.file_reader = FileReader(chosen_language)
        background_path = self.set_mode_configuration(chosen_difficulty)
        window_height: int = Constants.HEIGHT if self.file_reader.language_specific_letters == "" else Constants.HEIGHT_EXT

        Ui(window_height, background_path)

        # Generate new word.
        self.draw_new_word()

        # Initialize variables.
        self.indicators = []
        self.choose_difficulty_buttons = []
        self.guesses = [[]] * 6
        self.guesses_count = 0
        self.game_result = GameResult.NOT_DECIDED
        self.is_locked = False  # Whether the inputs are locked. This happens during animations.
        self.current_guess = []
        self.current_guess_string = ""
        self.current_letter_bg_x = self.starting_offset_for_letter

        self.initialize_keyboard()

    def set_mode_configuration(self, chosen_difficulty: Difficulty):
        self.chosen_difficulty = chosen_difficulty
        self.words = self.file_reader.get_words(chosen_difficulty)
        if chosen_difficulty == Difficulty.EASY:
            self.starting_offset_for_letter = Constants.EASY_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.EASY_DIFFICULTY_LETTERS
            return Constants.EASY_DIFFICULTY_BACKGROUND_PATH
        elif chosen_difficulty == Difficulty.MEDIUM:
            self.starting_offset_for_letter = Constants.MEDIUM_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.MEDIUM_DIFFICULTY_LETTERS
            return Constants.MEDIUM_DIFFICULTY_BACKGROUND_PATH
        else:
            self.starting_offset_for_letter = Constants.HARD_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.HARD_DIFFICULTY_LETTERS
            return Constants.HARD_DIFFICULTY_BACKGROUND_PATH

    def update_configuration(self, chosen_difficulty):
        background_path = self.set_mode_configuration(chosen_difficulty)
        self.current_letter_bg_x = self.starting_offset_for_letter
        Ui.update_background(background_path)

    def setup_difficulty_buttons(self):
        difficulty_colors = {Difficulty.EASY: Color.OUTLINE, Difficulty.MEDIUM: Color.OUTLINE, Difficulty.HARD: Color.OUTLINE, self.chosen_difficulty: Color.GREEN}
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 105, 5, Difficulty.EASY, difficulty_colors[Difficulty.EASY]))
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 215, 5, Difficulty.MEDIUM, difficulty_colors[Difficulty.MEDIUM]))
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 325, 5, Difficulty.HARD, difficulty_colors[Difficulty.HARD]))

    def initialize_keyboard(self):
        indicator_position_y = Constants.FIRST_INDICATOR_POSITION_Y
        x_offset = 0
        for i in range(3):
            x_offset = (Constants.WIDTH - len(Constants.BASIC_INDICATORS[i]) * 60)/2
            if i == 2:
                enter = Indicator(x_offset - 91, indicator_position_y, "Enter", 100 - Constants.LETTERBOX_Y_SPACING)
                self.indicators.append(enter)

            for letter in Constants.BASIC_INDICATORS[i]:
                new_indicator = Indicator(x_offset, indicator_position_y, letter)
                self.indicators.append(new_indicator)
                x_offset += 60
            indicator_position_y += 90

        backspace = Indicator(x_offset, indicator_position_y-90, "BckSp", 100)
        self.indicators.append(backspace)

        x_offset = (Constants.WIDTH - len(self.file_reader.language_specific_letters) * 60)/2
        for letter in self.file_reader.language_specific_letters:
            new_indicator = Indicator(x_offset, indicator_position_y, letter)
            self.indicators.append(new_indicator)
            x_offset += 60

    def reset(self):
        Ui.reset_ui()
        self.guesses_count = 0
        self.draw_new_word()
        self.guesses: List[List[LetterBox]] = [[]] * 6
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = GameResult.NOT_DECIDED
        Ui.force_display_update()
        for indicator in self.indicators:
            indicator.bg_color = Color.OUTLINE
            indicator.draw()

    def draw_new_word(self):
        self.word = random.choice(self.words)

    def is_valid_word(self, word: str):
        return word in self.words

    def create_new_letterbox(self, key_pressed):
        self.current_guess_string += key_pressed
        new_letterbox = LetterBox(key_pressed, (self.current_letter_bg_x, self.guesses_count * 100 + Constants.LETTERBOX_X_SPACING - 40))
        self.current_letter_bg_x += Constants.LETTERBOX_X_SPACING
        self.guesses[self.guesses_count].append(new_letterbox)
        self.current_guess.append(new_letterbox)
        new_letterbox.draw()

    def delete_letterbox(self):
        if len(self.current_guess_string) <= 0:
            return
        self.guesses[self.guesses_count][-1].delete()
        self.guesses[self.guesses_count].pop()
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.current_letter_bg_x -= Constants.LETTERBOX_X_SPACING

    @staticmethod
    def get_frequency_of_letters_in_guessed_word(guess_to_check: List[LetterBox]) -> Dict[str, int]:
        letters = [x.character for x in guess_to_check]
        return collections.Counter(letters)

    def get_frequency_of_letters_in_correct_word(self):
        return collections.Counter(self.word.upper())

    def update_indicator(self, letter: str, color: Color):
        for indicator in self.indicators:
            if indicator.text == letter and indicator.bg_color == Color.OUTLINE:
                indicator.bg_color = color
                indicator.draw()

    def update_letter(self, letter: LetterBox, color: Color):
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
    def get_letters_with_position(guess_to_check: List[LetterBox]) -> List[LetterInWord]:
        guess_letters: List[LetterInWord] = []
        for i in range(len(guess_to_check)):
            guess_letters.append(LetterInWord(guess_to_check[i], i))
        return guess_letters

    def check_guess(self, guess_word: List[LetterBox]):
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
        for i in range(self.number_of_letters):
            thread_kwargs = {'trigger_time': i * LETTERBOX_ANIM_FREQ + 1, 'letterbox': guess_word_copy[i]}
            t = threading.Thread(target=flip_anim_triggerer, kwargs=thread_kwargs)
            t.start()

            # If this is the last letter, create another event which will unlock inputs.
            if i == self.number_of_letters - 1:
                t = threading.Thread(target=self.input_unlocker, kwargs={'trigger_time':i*300+300})
                t.start()

    def play_again(self):
        frame_x = 10
        frame_y = 625
        frame_width = Constants.WIDTH - (frame_x * 2)  # Equal margin.
        frame_height = Constants.HEIGHT - frame_y - frame_x

        frame_rect = (frame_x, frame_y, frame_width, frame_height)
        Ui.display_game_over_frame(frame_rect, "Press ENTER to play again!", f"The word was {self.word.upper()}!")

    def handle_keyboard_pressed_event(self, event):
        if event.key == pygame.K_RETURN:
            self.check_word()
        elif event.key == pygame.K_BACKSPACE:
            self.delete_letterbox()
        else:
            self.insert_letter(event.unicode.upper())

    def handle_mouse_clicked_event(self, event):
        key_pressed = ""
        for choose_mode in self.choose_difficulty_buttons:
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
            self.delete_letterbox()
        else:
            self.insert_letter(key_pressed)

    def check_word(self):
        if self.game_result != GameResult.NOT_DECIDED:
            self.reset()
        else:
            if len(self.current_guess_string) != self.number_of_letters:
                Ui.display_popup("Not enough letters!", self.indicators)
                self.shake_letters(self.current_guess)
            elif self.current_guess_string.lower() not in self.words:
                Ui.display_popup("Not in word list!", self.indicators)
                self.shake_letters(self.current_guess)
            else:
                self.check_guess(self.current_guess)

    def shake_letters(self, letters):
        for letter in letters:
            t = threading.Thread(target=shake_anim_triggerer, kwargs={'letterbox': letter})
            t.start()

    def insert_letter(self, key_pressed):
        if key_pressed in self.file_reader.alphabet and key_pressed != "":
            if len(self.current_guess_string) < self.number_of_letters:
                self.create_new_letterbox(key_pressed)

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

    def update(self, delta_time):
        for guess in self.guesses:
            for letter in guess:
                letter.update(delta_time)

    def play(self):
        clock = pygame.time.Clock()
        fps = 60
        self.running = True
        pygame.mixer.music.load(AMBIENCE_OST)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)

        while self.running:
            self.setup_difficulty_buttons()  # Move out of here after test.
            delta_time = clock.tick(fps) / 1000
            self.check_game_complete()
            self.handle_events()
            self.update(delta_time)
            pygame.display.update()

        pygame.quit()
        sys.exit()

    # Move this somewhere higher @Patryk Wyszynski.
    def input_unlocker(self, trigger_time):
        time.sleep(trigger_time / 1000)
        self.is_locked = False