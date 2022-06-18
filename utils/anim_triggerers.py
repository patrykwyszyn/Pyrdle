import time

import pygame

SWOOSH_SFX = pygame.mixer.Sound("resources/sounds/letter_swoosh.ogg")


def flip_anim_triggerer(trigger_time, letterbox):
    time.sleep(trigger_time/1000)  # time.sleep() requires seconds.
    pygame.mixer.Sound.play(SWOOSH_SFX)
    letterbox.start_flip_animation()


def shake_anim_triggerer(letterbox):
    letterbox.start_shake_animation()
