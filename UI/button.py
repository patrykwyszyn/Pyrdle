from abc import abstractmethod
from typing import Tuple


class Button:
    def __init__(self, x, y, text, text_offset, rect, bg_color):
        self.x = x
        self.y = y
        self.text = text
        self.text_offset = text_offset
        self.rect = rect
        self.bg_color = bg_color

    @abstractmethod
    def draw(self):
        pass

    def is_point_colliding(self, mouse_position: Tuple[int, int]):
        x, y, width, height = self.rect
        mouse_position_x, mouse_position_y = mouse_position
        return x <= mouse_position_x <= x + width and y <= mouse_position_y <= y + height
