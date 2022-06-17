from typing import List


class Constants:
    BASIC_INDICATORS: List[str] = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    LETTERBOX_X_SPACING = 85
    LETTERBOX_Y_SPACING = 12
    LETTERBOX_SIZE = 75

    WIDTH = 650
    HEIGHT = 900
    HEIGHT_EXT = HEIGHT + 100  # For non-english locales that use extra letters, an additional line of keys is shown.

    BG_GRID_CENTER = (318, 333)

    EASY_DIFFICULTY_LETTERS = 5
    MEDIUM_DIFFICULTY_LETTERS = 6
    HARD_DIFFICULTY_LETTERS = 7

    EASY_DIFFICULTY_OFFSET = 110
    MEDIUM_DIFFICULTY_OFFSET = 67
    HARD_DIFFICULTY_OFFSET = 20

    EASY_DIFFICULTY_BACKGROUND_PATH = "resources/easy_mode.png"
    MEDIUM_DIFFICULTY_BACKGROUND_PATH = "resources/medium_mode.png"
    HARD_DIFFICULTY_BACKGROUND_PATH = "resources/hard_mode.png"
    ICON_PATH = "resources/Icon.png"

    WINDOW_TITLE = "Wordle!"

    FIRST_INDICATOR_POSITION_Y = 630
