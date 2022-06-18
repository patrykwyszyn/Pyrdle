from typing import Tuple

from UI.button import Button
from UI.ui import Ui
from models.color import Color
from models.difficulty import Difficulty
from models.fonts_name import FontsName

BUTTON_HEIGHT = 30
TEXT_Y_OFFSET = 15


class ChooseModeButton(Button):
    """
    Button class responsible for displaying option for changing difficulty

    :param x: width of the rectangle which will serve as button
    :type x: float
    :param y: height of the rectangle which will serve as button
    :type y: float
    :param color: color background of the button
    :type color: Color(str, Enum)
    """
    def __init__(self, x: float, y: float, mode: Difficulty, color: Color = Color.OUTLINE):
        text_offset: Tuple[float, float] = (x - len(mode) * 0.5 + 100/2, y + TEXT_Y_OFFSET)
        rect: Tuple[float, float, float, float] = (x, y, 100, BUTTON_HEIGHT)
        super().__init__(x, y, mode, text_offset, rect, color)
        self.draw()

    def draw(self) -> None:
        Ui.draw_button(self, FontsName.CHOOSE_MODE)
