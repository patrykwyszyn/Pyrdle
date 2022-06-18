import collections
import sys
import threading
import time
from typing import List, Dict, Tuple

import pygame
from pygame.event import Event

from UI.letterbox import LetterBox
from UI.ui import Ui
from configuration import Configuration
from constants import Constants
from models.color import Color
from models.difficulty import Difficulty
from models.game_result import GameResult
from models.letter_in_word import LetterInWord

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
    configuration: Configuration
    running: bool
    guesses: List[List[LetterBox]]
    current_guess: List[LetterBox]
    guesses_count: int
    current_guess_string: str
    game_result: GameResult
    is_showing_results: bool

    def __init__(self, chosen_language: str = "english", chosen_difficulty: Difficulty = Difficulty.EASY):
        self.configuration = Configuration(chosen_language, chosen_difficulty)

        self.is_locked: bool = False  # Whether the inputs are locked. This happens during animations.
        self.set_default_game_statistic()
        self.configuration.initialize_keyboard()

    def reset(self) -> None:
        Ui.reset_ui()
        self.set_default_game_statistic()
        Ui.force_display_update()
        for indicator in self.configuration.indicators:
            indicator.bg_color = Color.OUTLINE
            indicator.draw()

    def set_default_game_statistic(self) -> None:
        # Generate new word.
        self.configuration.draw_new_word()
        # Initialize variables.
        self.guesses_count = 0
        self.guesses: List[List[LetterBox]] = [[]]
        self.current_guess = []
        self.current_guess_string = ""
        self.game_result = GameResult.NOT_DECIDED
        self.is_showing_results = False

    def is_valid_word(self, word: str) -> bool:
        return word in self.configuration.words

    def create_new_letterbox(self, key_pressed: str) -> None:
        self.current_guess_string += key_pressed
        new_letterbox = LetterBox(key_pressed, (self.configuration.current_letter_bg_x, self.guesses_count * 100 + Constants.LETTERBOX_X_SPACING - 40))
        self.configuration.current_letter_bg_x += Constants.LETTERBOX_X_SPACING
        if not self.guesses_count + 1 == len(self.guesses):
            self.guesses.append([])
        self.guesses[self.guesses_count].append(new_letterbox)
        self.current_guess.append(new_letterbox)
        new_letterbox.draw()

    def delete_letterbox(self) -> None:
        if len(self.current_guess_string) <= 0:
            return
        self.guesses[self.guesses_count][-1].delete_from_board()
        self.guesses[self.guesses_count].pop()
        self.current_guess_string = self.current_guess_string[:-1]
        self.current_guess.pop()
        self.configuration.current_letter_bg_x -= Constants.LETTERBOX_X_SPACING

    @staticmethod
    def get_frequency_of_letters_in_guessed_word(guess_to_check: List[LetterBox]) -> Dict[str, int]:
        letters = [x.character for x in guess_to_check]
        return collections.Counter(letters)

    def get_frequency_of_letters_in_correct_word(self) -> Dict[str, int]:
        return collections.Counter(self.configuration.word.upper())

    def update_indicator(self, letter: str, color: Color) -> None:
        for indicator in self.configuration.indicators:
            if indicator.text == letter and indicator.bg_color == Color.OUTLINE:
                indicator.bg_color = color
                indicator.draw()

    def update_letter(self, letter: LetterBox, color: Color) -> None:
        self.update_indicator(letter.character, color)
        letter.schedule_params(color, Color.WHITE)

        letter.draw()
        Ui.force_display_update()

    def prepare_for_the_next_guess(self) -> None:
        self.guesses_count += 1
        self.current_guess = []
        self.current_guess_string = ""
        self.configuration.current_letter_bg_x = self.configuration.starting_offset_for_letter

    @staticmethod
    def get_letters_with_position(guess_to_check: List[LetterBox]) -> List[LetterInWord]:
        guess_letters: List[LetterInWord] = []
        for i in range(len(guess_to_check)):
            guess_letters.append(LetterInWord(guess_to_check[i], i))
        return guess_letters

    def check_guess(self, guess_word: List[LetterBox]) -> None:
        self.is_locked = True
        frequency_of_letters_in_correct_word: Dict[str, int] = self.get_frequency_of_letters_in_correct_word()
        frequency_of_letters_in_guessed_word: Dict[str, int] = self.get_frequency_of_letters_in_guessed_word(guess_word)
        guess_letters: List[LetterInWord] = self.get_letters_with_position(guess_word)
        guess_word_copy: List[LetterBox] = guess_word.copy()

        for guess_letter in guess_letters.copy():
            if guess_letter.letter.character.lower() == self.configuration.word[guess_letter.index]:
                self.update_letter(guess_letter.letter, Color.GREEN)
                self.game_result = GameResult.WIN

                guess_letters.remove(guess_letter)
                frequency_of_letters_in_correct_word[guess_letter.letter.character] -= 1
                frequency_of_letters_in_guessed_word[guess_letter.letter.character] -= 1

        for guess_letter in guess_letters.copy():
            if guess_letter.letter.character.lower() in self.configuration.word and frequency_of_letters_in_correct_word[guess_letter.letter.character] > 0:
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
        for i in range(self.configuration.number_of_letters):
            thread_kwargs = {'trigger_time': i * LETTERBOX_ANIM_FREQ + 1, 'letterbox': guess_word_copy[i]}
            t = threading.Thread(target=flip_anim_triggerer, kwargs=thread_kwargs)
            t.start()

            # If this is the last letter, create another event which will unlock inputs.
            if i == self.configuration.number_of_letters - 1:
                t = threading.Thread(target=self.input_unlocker, kwargs={'trigger_time': i * 300 + 300})
                t.start()

    def display_results(self):
        frame_x: float = 10
        frame_y: float = 625
        frame_width: float = Constants.WIDTH - (frame_x * 2)  # Equal margin.
        frame_height: float = Constants.HEIGHT - frame_y - frame_x
        result_text: Dict[GameResult, Tuple[str, Color]] = {
            GameResult.WIN: ("Congratulations, you WIN!", Color.GREEN),
            GameResult.LOSE: ("You lose, try again!", Color.RED)
        }
        self.is_showing_results = True
        frame_rect: Tuple[float, float, float, float] = (frame_x, frame_y, frame_width, frame_height)
        Ui.display_game_over_frame(frame_rect, "Press ENTER to play again!", f"The word was {self.configuration.word.upper()}!", result_text[self.game_result])

    def handle_keyboard_pressed_event(self, event):
        if event.key == pygame.K_RETURN:
            self.check_word()
        elif event.key == pygame.K_BACKSPACE:
            self.delete_letterbox()
        else:
            self.insert_letter(event.unicode.upper())

    def handle_mouse_clicked_event(self, event: Event) -> None:
        if self.is_showing_results:
            self.reset()
        else:
            key_pressed: str = ""
            for choose_mode in self.configuration.choose_difficulty_buttons:
                if choose_mode.is_point_colliding(event.pos):
                    self.configuration.update_configuration(choose_mode.text)
                    self.reset()
                    return
            for indicator in self.configuration.indicators:
                if indicator.is_point_colliding(event.pos):
                    key_pressed = indicator.text
            if key_pressed == "Enter":
                self.check_word()
            elif key_pressed == "BckSp":
                self.delete_letterbox()
            else:
                self.insert_letter(key_pressed)

    def check_word(self) -> None:
        if self.game_result != GameResult.NOT_DECIDED:
            self.reset()
        else:
            if len(self.current_guess_string) != self.configuration.number_of_letters:
                Ui.display_popup("Not enough letters!", self.configuration.indicators)
                self.shake_letters(self.current_guess)
            elif self.current_guess_string.lower() not in self.configuration.words:
                Ui.display_popup("Not in word list!", self.configuration.indicators)
                self.shake_letters(self.current_guess)
            else:
                self.check_guess(self.current_guess)

    @staticmethod
    def shake_letters(letters) -> None:
        for letter in letters:
            t = threading.Thread(target=shake_anim_triggerer, kwargs={'letterbox': letter})
            t.start()

    def insert_letter(self, key_pressed) -> None:
        if key_pressed in self.configuration.file_reader.alphabet and key_pressed != "":
            if len(self.current_guess_string) < self.configuration.number_of_letters:
                self.create_new_letterbox(key_pressed)

    def check_game_complete(self) -> None:
        if self.game_result != GameResult.NOT_DECIDED:
            self.display_results()

    def handle_events(self) -> None:
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

    def update(self, delta_time: float) -> None:
        for guess in self.guesses:
            for letter in guess:
                letter.update(delta_time)

    def play(self) -> None:
        clock = pygame.time.Clock()
        fps: int = 60
        self.running = True
        pygame.mixer.music.load(AMBIENCE_OST)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.7)

        while self.running:
            self.configuration.setup_difficulty_buttons()  # Move out of here after test.
            delta_time: float = clock.tick(fps) / 1000
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
