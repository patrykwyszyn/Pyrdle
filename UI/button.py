from abc import abstractmethod
from typing import Tuple


class Button:
    def __init__(self, x: float, y: float, text: str, text_offset: Tuple[float, float], rect: Tuple[float, float, float, float], bg_color: str):
        self.x: float = x
        self.y: float = y
        self.text: str = text
        self.text_offset: Tuple[float, float] = text_offset
        self.rect: Tuple[float, float, float, float] = rect
        self.bg_color: str = bg_color

    @abstractmethod
    def draw(self) -> None:
        pass

    def is_point_colliding(self, mouse_position: Tuple[int, int]) -> bool:
        x, y, width, height = self.rect
        mouse_position_x, mouse_position_y = mouse_position
        return x <= mouse_position_x <= x + width and y <= mouse_position_y <= y + height
