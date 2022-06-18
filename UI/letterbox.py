from typing import Tuple

from UI.ui import Ui
from constants import Constants
from models.Theme import Theme
from models.color import Color

FLIP_VELOCITY = 280
SHAKE_VELOCITY = 1
SHAKE_MAX_OFFSET = 25
SHAKE_LIMIT = 100


class LetterBox:
    """
    Class responsible for displaying result of the guess made by user

    :param character: character which will be displayed
    :type character: str
    :param bg_position: box position in the window
    :type bg_position: Tuple[str, str]
    """
    def __init__(self, character: str, bg_position: Tuple[float, float], theme: Theme):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color: str = Color.WHITE if theme == Theme.LIGHT else Color.BLACK_BG
        self.text_color: str = Color.BLACK if theme == Theme.LIGHT else Color.WHITE
        self.bg_x: float = bg_position[0]
        self.bg_y: float = bg_position[1]
        self.bg_rect: Tuple[float, float, float, float] = (self.bg_x, self.bg_y, Constants.LETTERBOX_SIZE, Constants.LETTERBOX_SIZE)
        self.bg_rect_copy: Tuple[float, float, float, float] = self.bg_rect
        self.character: str = character
        self.text_position: Tuple[float, float] = (self.bg_x+36, self.bg_y+34)

        # Animation related variables.
        self.flip_velocity: int = 0
        self.shake_velocity: int = 0
        self.shake_counter: int = 0
        self.is_flip_playing: bool = False
        self.is_shake_playing: bool = False
        self.bg_color_scheduled: str = self.bg_color
        self.text_color_scheduled: str = self.text_color
        self.target_y: float = self.bg_rect[1] + (self.bg_rect[3] / 2)  # Target Y is the middle of the rectangle, so Y + (height/2)

    def draw(self) -> None:
        Ui.draw_letterbox_on_board(self)

    def schedule_params(self, new_bg_color: str, new_text_color: str) -> None:
        self.bg_color_scheduled = new_bg_color
        self.text_color_scheduled = new_text_color

    def start_flip_animation(self) -> None:
        self.flip_velocity = FLIP_VELOCITY
        self.is_flip_playing = True

    def start_shake_animation(self) -> None:
        self.shake_velocity = SHAKE_VELOCITY
        self.is_shake_playing = True

    def update(self, delta: float) -> None:
        # Animate if requested.
        if self.is_flip_playing:
            self._animate_flip(delta)
            self.draw()
        elif self.is_shake_playing:
            self._animate_shake(delta)
            self.draw()

    def delete_from_board(self) -> None:
        Ui.delete_letterbox_from_board(self)

    def _swap_scheduled_params(self) -> None:
        self.bg_color = self.bg_color_scheduled
        self.text_color = self.text_color_scheduled
        self.bg_color_scheduled = Color.WHITE
        self.text_color_scheduled = Color.BLACK

    def _animate_flip(self, delta) -> None:
        # Do the scaling towards the center OR back to normal.
        if self.bg_rect[1] < self.target_y or self.bg_rect[3] > 0:
            self.bg_rect = (self.bg_rect[0],
                            self.bg_rect[1] + ((self.flip_velocity * delta) / 2),
                            self.bg_rect[2],
                            self.bg_rect[3] - (self.flip_velocity * delta))
        # When the letter is flattened, update its state and negate velocity.
        else:
            self._swap_scheduled_params()
            self.bg_rect = (self.bg_rect[0], self.bg_rect[1] - 1, self.bg_rect[2], 1)
            self.flip_velocity = -FLIP_VELOCITY

        # Once the letter is scaled back to normal, stop the animation.
        if self.bg_rect[1] <= self.bg_rect_copy[1] \
                and self.bg_rect[3] >= self.bg_rect_copy[3] \
                and self.flip_velocity < 0:
            self.bg_rect = self.bg_rect_copy  # Make sure the dimensions have been restored to their original values.
            self.is_flip_playing = False

    def _animate_shake(self, delta) -> None:
        if self.bg_rect[0] < self.bg_rect_copy[0] - SHAKE_MAX_OFFSET or self.bg_rect[0] > self.bg_rect_copy[1] + SHAKE_MAX_OFFSET:
            self.shake_velocity = -self.shake_velocity

        self.shake_counter += 1

        # Stop animation.
        if self.shake_counter >= SHAKE_LIMIT:
            self.shake_counter = 0
            self.is_shake_playing = False
            self.bg_rect = self.bg_rect_copy
            return

        self.bg_rect = (self.bg_rect[0] + (self.shake_velocity * delta), self.bg_rect[1], self.bg_rect[2], self.bg_rect[3])

