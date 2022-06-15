import pygame

from constants import Constants
from models.color import Color


class Letter:
    def __init__(self, text, bg_position, screen):
        # Initializes all the variables, including text, color, position, size, etc.
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, Constants.LETTER_SIZE, Constants.LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.screen = screen
        self.guessed_letter_font = pygame.font.Font("resources/FreeSansBold.otf", 50)
        self.text_surface = self.guessed_letter_font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(self.screen, self.bg_color, self.bg_rect)
        if self.bg_color == "white":
            pygame.draw.rect(self.screen, Color.FILLED_OUTLINE, self.bg_rect, 3)
        self.text_surface = self.guessed_letter_font.render(self.text, True, self.text_color)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        # Fills the letter's spot with the default square, emptying it.
        pygame.draw.rect(self.screen, "white", self.bg_rect)
        pygame.draw.rect(self.screen, Color.OUTLINE, self.bg_rect, 3)
        pygame.display.update()