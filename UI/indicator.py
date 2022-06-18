from typing import Tuple

from UI.button import Button
from UI.ui import Ui
from models.color import Color
from models.fonts_name import FontsName

INDICATOR_WIDTH: float = 57
INDICATOR_HEIGHT: float = 75
TEXT_Y_OFFSET: float = 38


class Indicator(Button):
    """
    Button class responsible for displaying keyboard.

    :param x: width of the rectangle which will serve as button
    :type x: float
    :param y: height of the rectangle which will serve as button
    :type y: float
    :param letter: letter for which instance will responsible for
    :type letter: letter
    :param x: width of the indicator box
    :type x: float
    """
    def __init__(self, x: float, y: float, letter: str, width: float = INDICATOR_WIDTH):
        text_offset: Tuple[float, float] = (x - len(letter) * 0.5 + width/2, y + TEXT_Y_OFFSET)
        rect: Tuple[float, float, float, float] = (x, y, width, INDICATOR_HEIGHT)
        super().__init__(x, y, letter, text_offset, rect, Color.OUTLINE)
        self.draw()

    def draw(self) -> None:
        Ui.draw_button(self, FontsName.INDICATOR)
