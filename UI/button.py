from abc import abstractmethod
from typing import Tuple


class Button:
    """
    Base class for every button class used in project

    :param x: width of the rectangle which will serve as button
    :type x: float
    :param y: height of the rectangle which will serve as button
    :type y: float
    :param text_offset: position of the button in the displayed window
    :type text_offset: Tuple[float, float]
    :param rect: settings needed for pygame.rect
    :type rect: Tuple[float, float, float, float]
    :param bg_color: background color of the button
    :type bg_color: str
    """
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
