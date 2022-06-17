from UI.button import Button
from UI.ui import Ui
from models.color import Color
from models.fonts_name import FontsName
from models.difficulty import Difficulty

INDICATOR_WIDTH = 47
INDICATOR_HEIGHT = 30
TEXT_X_OFFSET = 23
TEXT_Y_OFFSET = 15


class ChooseModeButton(Button):
    def __init__(self, x: float, y: float, mode: Difficulty, color: Color = Color.OUTLINE):
        text_offset = (x - len(mode) * 0.5 + 100/2, y + TEXT_Y_OFFSET)
        rect = (x, y, 100, INDICATOR_HEIGHT)
        super().__init__(x, y, mode, text_offset, rect, color)
        self.draw()

    def draw(self):
        Ui.draw_button(self, FontsName.CHOOSE_MODE)
