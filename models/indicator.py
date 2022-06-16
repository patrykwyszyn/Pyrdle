from UI.ui import Ui
from models.color import Color

INDICATOR_WIDTH = 57
INDICATOR_HEIGHT = 75
TEXT_X_OFFSET = 28
TEXT_Y_OFFSET = 38


class Indicator:
    def __init__(self, x, y, letter):
        self.x = x
        self.y = y
        self.text = letter
        self.text_offset = (x + TEXT_X_OFFSET, y + TEXT_Y_OFFSET)
        self.rect = (self.x, self.y, INDICATOR_WIDTH, INDICATOR_HEIGHT)
        self.bg_color = Color.OUTLINE
        self.draw()

    def draw(self):
        Ui.draw_indicator(self)
