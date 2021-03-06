import random
from typing import List, Dict

from UI.choose_mode_button import ChooseModeButton
from UI.indicator import Indicator
from UI.ui import Ui
from constants import Constants
from file_reader import FileReader
from models.Theme import Theme
from models.color import Color
from models.difficulty import Difficulty


class Configuration:
    """
    Class responsible for setting necessary components which will be displayed on screen

    :param chosen_language: specifies the word base, from which the words will be drawn
    :type chosen_language: str
    :param chosen_difficulty: difficulty as in a number of letters in words
    :type chosen_difficulty: Difficulty(str, Enum)
    """
    file_reader: FileReader
    words: List[str]
    word: str
    starting_offset_for_letter: int
    number_of_letters: int
    theme: Theme

    def __init__(self, chosen_language: str, chosen_difficulty: Difficulty, theme: Theme):
        # Setup window, difficulty and UI.
        self.theme = theme
        self.file_reader = FileReader(chosen_language)
        self.chosen_difficulty: Difficulty = chosen_difficulty
        background_path: str = self.set_mode_configuration(chosen_difficulty)
        self.window_height: int = Constants.HEIGHT if self.file_reader.language_specific_letters == "" else Constants.HEIGHT_EXT
        Ui(self.window_height, background_path, theme)

        self.indicators: List[Indicator] = []
        self.choose_difficulty_buttons: List[ChooseModeButton] = []
        self.current_letter_bg_x: int = self.starting_offset_for_letter

    def update_configuration(self, chosen_difficulty: str) -> None:
        background_path: str = self.set_mode_configuration(chosen_difficulty)
        self.current_letter_bg_x: int = self.starting_offset_for_letter
        Ui.update_background(background_path)

    def setup_difficulty_buttons(self) -> None:
        themed_color = Color.OUTLINE_DARK if self.theme == Theme.DARK else Color.OUTLINE
        difficulty_colors: Dict[Difficulty, Color] = {Difficulty.EASY: themed_color, Difficulty.MEDIUM: themed_color, Difficulty.HARD: themed_color, self.chosen_difficulty: Color.GREEN}
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 105, 5, Difficulty.EASY, difficulty_colors[Difficulty.EASY]))
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 215, 5, Difficulty.MEDIUM, difficulty_colors[Difficulty.MEDIUM]))
        self.choose_difficulty_buttons.append(ChooseModeButton(Constants.WIDTH - 325, 5, Difficulty.HARD, difficulty_colors[Difficulty.HARD]))

    def initialize_keyboard(self) -> None:
        indicator_position_y: int = Constants.FIRST_INDICATOR_POSITION_Y
        x_offset: float = 0
        for i in range(3):
            x_offset = (Constants.WIDTH - len(Constants.BASIC_INDICATORS[i]) * 60)/2
            if i == 2:
                enter = Indicator(x_offset - 91, indicator_position_y, "Enter", self.theme, 100 - Constants.LETTERBOX_Y_SPACING)
                self.indicators.append(enter)

            for letter in Constants.BASIC_INDICATORS[i]:
                new_indicator = Indicator(x_offset, indicator_position_y, letter, self.theme)
                self.indicators.append(new_indicator)
                x_offset += 60
            indicator_position_y += 90

        backspace = Indicator(x_offset, indicator_position_y-90, "BckSp", self.theme, 100)
        self.indicators.append(backspace)

        x_offset = (Constants.WIDTH - len(self.file_reader.language_specific_letters) * 60)/2
        for letter in self.file_reader.language_specific_letters:
            new_indicator = Indicator(x_offset, indicator_position_y, letter, self.theme)
            self.indicators.append(new_indicator)
            x_offset += 60

    def set_mode_configuration(self, chosen_difficulty: Difficulty | str):
        self.chosen_difficulty = chosen_difficulty
        self.words = self.file_reader.get_words(chosen_difficulty)
        if chosen_difficulty == Difficulty.EASY:
            self.starting_offset_for_letter = Constants.EASY_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.EASY_DIFFICULTY_LETTERS
            return Constants.EASY_DIFFICULTY_BACKGROUND_PATH if self.theme == Theme.LIGHT else Constants.EASY_DIFFICULTY_DARK_BACKGROUND_PATH
        elif chosen_difficulty == Difficulty.MEDIUM:
            self.starting_offset_for_letter = Constants.MEDIUM_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.MEDIUM_DIFFICULTY_LETTERS
            return Constants.MEDIUM_DIFFICULTY_BACKGROUND_PATH if self.theme == Theme.LIGHT else Constants.MEDIUM_DIFFICULTY_DARK_BACKGROUND_PATH
        else:
            self.starting_offset_for_letter = Constants.HARD_DIFFICULTY_OFFSET
            self.number_of_letters = Constants.HARD_DIFFICULTY_LETTERS
            return Constants.HARD_DIFFICULTY_BACKGROUND_PATH if self.theme == Theme.LIGHT else Constants.HARD_DIFFICULTY_DARK_BACKGROUND_PATH
    def draw_new_word(self):
        self.word = random.choice(self.words)
