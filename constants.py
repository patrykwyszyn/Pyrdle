from typing import List, Tuple


class Constants:
    """
    Class responsible for saving constants that are used in multiple places
    """
    BASIC_INDICATORS: List[str] = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    LETTERBOX_X_SPACING: int = 85
    LETTERBOX_Y_SPACING: int = 12
    LETTERBOX_SIZE: int = 75

    WIDTH: int = 650
    HEIGHT: int = 900
    HEIGHT_EXT: int = HEIGHT + 100  # For non-english locales that use extra letters, an additional line of keys is shown.

    BG_GRID_CENTER: Tuple[int, int] = (318, 333)

    EASY_DIFFICULTY_LETTERS: int = 5
    MEDIUM_DIFFICULTY_LETTERS: int = 6
    HARD_DIFFICULTY_LETTERS: int = 7

    EASY_DIFFICULTY_OFFSET: int = 110
    MEDIUM_DIFFICULTY_OFFSET: int = 67
    HARD_DIFFICULTY_OFFSET: int = 20

    EASY_DIFFICULTY_BACKGROUND_PATH: str = "resources/easy_mode.png"
    MEDIUM_DIFFICULTY_BACKGROUND_PATH: str = "resources/medium_mode.png"
    HARD_DIFFICULTY_BACKGROUND_PATH: str = "resources/hard_mode.png"
    ICON_PATH: str = "resources/Icon.png"

    WINDOW_TITLE: str = "Wordle!"

    FIRST_INDICATOR_POSITION_Y: int = 630
