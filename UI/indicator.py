from UI.button import Button
from models.color import Color

INDICATOR_WIDTH = 57
INDICATOR_HEIGHT = 75
TEXT_X_OFFSET = 28
TEXT_Y_OFFSET = 38


class Indicator(Button):
    def __init__(self, x, y, letter, width=INDICATOR_WIDTH):
        text_offset = (x - len(letter) * 0.5 + width/2, y + TEXT_Y_OFFSET)
        rect = (x, y, width, INDICATOR_HEIGHT)
        super().__init__(x, y, letter, text_offset, rect, Color.OUTLINE)

