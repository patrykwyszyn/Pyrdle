from UI.ui import Ui
from constants import Constants


class Letter:
    def __init__(self, character, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, Constants.LETTER_SIZE, Constants.LETTER_SIZE)
        self.character = character
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)

    def draw(self):
        Ui.draw_letter_on_board(self)

    def delete(self):
        Ui.delete_letter_from_board(self)