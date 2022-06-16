import pygame


from models.color import Color


class Indicator:
    def __init__(self, x, y, letter, screen):

        self.x = x
        self.y = y
        self.text = letter
        self.rect = (self.x, self.y, 57, 75)
        self.bg_color = Color.OUTLINE
        self.screen = screen
        self.available_letter_font = pygame.font.Font("resources/FreeSansBold.otf", 25)

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        text_surface = self.available_letter_font.render(self.text, True, "white")
        text_rect = text_surface.get_rect(center=(self.x+27, self.y+30))
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()
