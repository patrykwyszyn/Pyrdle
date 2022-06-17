import threading
import time

import pygame
from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType
from UI.button import Button
from constants import Constants
from models.color import Color
from models.fonts_name import FontsName

# Initialize pygame before loading assets.
pygame.init()

# Images/sprites.
ICON = pygame.image.load(Constants.ICON_PATH)

# Fonts.
GUESSED_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 50)
INDICATOR_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 25)
PLAY_AGAIN_FONT = pygame.font.Font("resources/FreeSansBold.otf", 40)
CHOOSE_MODE_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 15)
MESSAGE_BOX_FONT = pygame.font.Font("resources/FreeSansBold.otf", 18)

# Other constants.
FONT_SCALE_FACTOR = 80

class Ui:
    _screen: Surface | SurfaceType
    _background: Surface | SurfaceType
    _background_rect: Rect | RectType | None

    @classmethod
    def __init__(cls, window_height, background_path):
        cls._background = pygame.image.load(background_path)
        cls._background_rect = cls._background.get_rect(center=Constants.BG_GRID_CENTER)
        cls._screen = pygame.display.set_mode((Constants.WIDTH, window_height))
        cls._screen.fill(Color.WHITE)
        cls._screen.blit(cls._background, cls._background_rect)
        pygame.display.set_caption(Constants.WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        pygame.display.update()

    @classmethod
    def update_background(cls, background_path):
        cls._background = pygame.image.load(background_path)
        cls._background_rect = cls._background.get_rect(center=Constants.BG_GRID_CENTER)

    @classmethod
    def reset_ui(cls):
        cls._screen.fill(Color.WHITE)
        cls._screen.blit(cls._background, cls._background_rect)

    @classmethod
    def force_display_update(cls):
        pygame.display.update()

    @classmethod
    def draw_button(cls, button: Button, font: FontsName):
        fonts = {
            FontsName.INDICATOR: INDICATOR_LETTER_FONT,
            FontsName.CHOOSE_MODE: CHOOSE_MODE_LETTER_FONT
        }
        pygame.draw.rect(cls._screen, button.bg_color, button.rect, border_radius=7)
        text_surface = fonts[font].render(button.text, True, Color.WHITE)
        text_rect = text_surface.get_rect(center=button.text_offset)
        cls._screen.blit(text_surface, text_rect)
        pygame.display.update()

    @classmethod
    def draw_letter_on_board(cls, letter):
        # If animating, draw a rectangle with bigger margins first to cover the background grid.
        if letter.is_flip_playing:
            bg_grid_cover = (letter.bg_rect_copy[0] - 2,
                             letter.bg_rect_copy[1] - 2,
                             letter.bg_rect_copy[2] + 4,
                             letter.bg_rect_copy[3] + 4)
            pygame.draw.rect(cls._screen, Color.WHITE, bg_grid_cover)

        # Draw the box surface of the letter.
        pygame.draw.rect(cls._screen, letter.bg_color, letter.bg_rect)
        if letter.bg_color == Color.WHITE:
            pygame.draw.rect(cls._screen, Color.FILLED_OUTLINE, letter.bg_rect, 3)

        # Draw the letter itself and scale with its containing box.
        text_surface = GUESSED_LETTER_FONT.render(letter.character, True, letter.text_color)
        scaled_text_surface = pygame.transform.scale(text_surface,                # Surface.
                                                     (text_surface.get_width(),   # New scaled size (x, y).
                                                      abs(text_surface.get_height() * (letter.bg_rect[3] / FONT_SCALE_FACTOR))))
        text_rect = scaled_text_surface.get_rect(center=letter.text_position)
        cls._screen.blit(scaled_text_surface, text_rect)

        pygame.display.update()

    @classmethod
    def delete_letter_from_board(cls, letter):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(cls._screen, Color.WHITE, letter.bg_rect)
        pygame.draw.rect(cls._screen, Color.OUTLINE, letter.bg_rect, 3)
        pygame.display.update()

    @classmethod
    def display_game_over_frame(cls, frame_rect, play_again_str, word_info_str):
        pygame.draw.rect(cls._screen, Color.WHITE, frame_rect)

        text_center_y = frame_rect[1] + (frame_rect[3] / 2)  # Y coord of the center of the box
        text_center_offset = 20  # Offset text by this much up or down to split strings.

        play_again_text = PLAY_AGAIN_FONT.render(play_again_str, True, Color.BLACK)
        play_again_rect = play_again_text.get_rect(center=(Constants.WIDTH / 2, text_center_y - text_center_offset))
        word_info_text = PLAY_AGAIN_FONT.render(word_info_str, True, Color.BLACK)
        word_info_rect = word_info_text.get_rect(center=(Constants.WIDTH / 2, text_center_y + text_center_offset))
        cls._screen.blit(word_info_text, word_info_rect)
        cls._screen.blit(play_again_text, play_again_rect)
        pygame.display.update()

    @classmethod
    def display_popup(cls, message, indicators):
        width = len(message) * 10 + 20
        height = 50
        x = Constants.WIDTH / 2 - (width / 2) - 8
        y = Constants.HEIGHT - 170

        # Draw box
        popup_rect = (x, y, width, height)
        pygame.draw.rect(cls._screen, Color.BLACK, popup_rect, border_radius=10)

        # Draw text
        message_text = MESSAGE_BOX_FONT.render(message, True, Color.WHITE)
        message_rect = message_text.get_rect(center=(x + (width / 2), y + (height / 2)))
        cls._screen.blit(message_text, message_rect)

        pygame.display.update()

        # Disappear after n seconds
        t = threading.Thread(target=cls._hide_popup, kwargs={'hide_time': 1.0, 'indicators': indicators})
        t.start()

    @classmethod
    def _hide_popup(cls, hide_time, indicators):
        time.sleep(hide_time)

        pygame.draw.rect(cls._screen, Color.WHITE, (30, 700, 500, 100))
        pygame.display.update()
        for indicator in indicators:
            indicator.draw()
