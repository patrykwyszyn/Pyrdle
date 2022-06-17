from UI.ui import Ui
from constants import Constants
from models.color import Color

FLIP_VELOCITY = 100
SHAKE_VELOCITY = 1
SHAKE_MAX_OFFSET = 25
SHAKE_LIMIT = 100

class LetterBox:
    def __init__(self, character, bg_position):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = Color.WHITE
        self.text_color = Color.BLACK
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, Constants.LETTERBOX_SIZE, Constants.LETTERBOX_SIZE)
        self.bg_rect_copy = self.bg_rect
        self.character = character
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)

        # Animation related variables.
        self.flip_velocity = 0
        self.shake_velocity = 0
        self.shake_counter = 0
        self.is_flip_playing = False
        self.is_shake_playing = False
        self.bg_color_scheduled = self.bg_color
        self.text_color_scheduled = self.text_color
        self.target_y = self.bg_rect[1] + (self.bg_rect[3] / 2)  # Target Y is the middle of the rectangle, so Y + (height/2)

    def draw(self):
        Ui.draw_letter_on_board(self)

    def schedule_params(self, new_bg_color, new_text_color):
        self.bg_color_scheduled = new_bg_color
        self.text_color_scheduled = new_text_color

    def start_flip_animation(self):
        self.flip_velocity = FLIP_VELOCITY
        self.is_flip_playing = True

    def start_shake_animation(self):
        self.shake_velocity = SHAKE_VELOCITY
        self.is_shake_playing = True

    def update(self, delta):
        # Animate if requested.
        if self.is_flip_playing:
            self._animate_flip(delta)
            self.draw()
        elif self.is_shake_playing:
            self._animate_shake(delta)
            self.draw()

    def delete(self):
        Ui.delete_letter_from_board(self)

    def _swap_scheduled_params(self):
        self.bg_color = self.bg_color_scheduled
        self.text_color = self.text_color_scheduled
        self.bg_color_scheduled = Color.WHITE
        self.text_color_scheduled = Color.BLACK

    def _animate_flip(self, delta):
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

    def _animate_shake(self, delta):
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

