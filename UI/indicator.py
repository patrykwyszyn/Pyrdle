from typing import Tuple

from UI.button import Button
from UI.ui import Ui
from models.color import Color
from models.fonts_name import FontsName

INDICATOR_WIDTH: float = 57
INDICATOR_HEIGHT: float = 75
TEXT_X_OFFSET: float = 28
TEXT_Y_OFFSET: float = 38


class Indicator(Button):
    def __init__(self, x: float, y: float, letter: str, width: float = INDICATOR_WIDTH):
        text_offset: Tuple[float, float] = (x - len(letter) * 0.5 + width/2, y + TEXT_Y_OFFSET)
        rect: Tuple[float, float, float, float] = (x, y, width, INDICATOR_HEIGHT)
        super().__init__(x, y, letter, text_offset, rect, Color.OUTLINE)
        self.draw()

    def draw(self) -> None:
        Ui.draw_button(self, FontsName.INDICATOR)
