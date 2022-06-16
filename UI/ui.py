import pygame

from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType
from constants import Constants
from models.color import Color


# Initialize pygame before loading assets.
pygame.init()

# Images/sprites.
ICON = pygame.image.load(Constants.ICON_PATH)

# Fonts.
GUESSED_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("resources/FreeSansBold.otf", 25)
PLAY_AGAIN_FONT = pygame.font.Font("resources/FreeSansBold.otf", 40)


class Ui:
    _screen: Surface | SurfaceType
    _background: Surface | SurfaceType
    _background_rect: Rect | RectType | None
    
    @classmethod
    def __init__(cls, window_height, background_path):
        cls._background = pygame.image.load(background_path)
        cls._background_rect = cls._background.get_rect(center=Constants.BG_RECT_CENTER)
        cls._screen = pygame.display.set_mode((Constants.WIDTH, window_height))
        cls._screen.fill("white")
        cls._screen.blit(cls._background, cls._background_rect)
        pygame.display.set_caption(Constants.WINDOW_TITLE)
        pygame.display.set_icon(ICON)
        pygame.display.update()

    @classmethod
    def update_background(cls, background_path):
        cls._background = pygame.image.load(background_path)
        cls._background_rect = cls._background.get_rect(center=Constants.BG_RECT_CENTER)

    @classmethod
    def reset_ui(cls):
        cls._screen.fill("white")
        cls._screen.blit(cls._background, cls._background_rect)

    @classmethod
    def force_display_update(cls):
        pygame.display.update()

    @classmethod
    def draw_indicator(cls, indicator):
        pygame.draw.rect(cls._screen, indicator.bg_color, indicator.rect)
        text_surface = AVAILABLE_LETTER_FONT.render(indicator.text, True, "white")
        text_rect = text_surface.get_rect(center=indicator.text_offset)
        cls._screen.blit(text_surface, text_rect)
        pygame.display.update()

    @classmethod
    def draw_letter_on_board(cls, letter):
        text_surface = GUESSED_LETTER_FONT.render(letter.character, True, letter.text_color)
        text_rect = text_surface.get_rect(center=letter.text_position)

        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(cls._screen, letter.bg_color, letter.bg_rect)
        if letter.bg_color == "white":
            pygame.draw.rect(cls._screen, Color.FILLED_OUTLINE, letter.bg_rect, 3)
        text_surface = GUESSED_LETTER_FONT.render(letter.character, True, letter.text_color)
        cls._screen.blit(text_surface, text_rect)
        pygame.display.update()

    @classmethod
    def delete_letter_from_board(cls, letter):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(cls._screen, "white", letter.bg_rect)
        pygame.draw.rect(cls._screen, Color.OUTLINE, letter.bg_rect, 3)
        pygame.display.update()

    @classmethod
    def display_game_over_frame(cls, popup_rect, play_again_str, word_info_str):
        pygame.draw.rect(cls._screen, "white", popup_rect)
        play_again_text = PLAY_AGAIN_FONT.render(play_again_str, True, "black")
        play_again_rect = play_again_text.get_rect(center=(Constants.WIDTH / 2, 700))
        word_info_text = PLAY_AGAIN_FONT.render(word_info_str, True, "black")
        word_info_rect = word_info_text.get_rect(center=(Constants.WIDTH / 2, 650))
        cls._screen.blit(word_info_text, word_info_rect)
        cls._screen.blit(play_again_text, play_again_rect)
        pygame.display.update()
