import pygame


# this class present a button on the window
class Button:
    def __init__(self, rect: pygame.Rect, text: str, color, func=None):
        self.rect = rect
        self.text = text
        self.color = color
        self.func = func
        self.is_pressed = False


    def pressed(self):
        self.is_pressed = not self.is_pressed
