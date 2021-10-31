import random
import pygame
from Settings import *

# initialzing font for score
pygame.font.init()
font_type = pygame.font.match_font('arial')


# function which draws score on screen
def draw_score(surface, text, size, x, y):
    font = pygame.font.Font(font_type, size)
    output = "Score: " + text
    text_surface = font.render(output, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


# function which draws number of lives on screen
def draw_lives(surface, lives, x, y, img):
    for i in range(1, lives+1):
        img_rect = img.get_rect()
        img_rect.x = x - 25*i
        img_rect.y = y
        surface.blit(img, img_rect)