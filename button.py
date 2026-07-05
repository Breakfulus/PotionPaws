import pygame

class Button:
    def __init__(self, pos, rect, text):
        self.pos = pygame.Vector2(pos)
        self.rect = rect
        self.text = text

    def check_if_hovered(self):
        pass

    def clicked(self):
        pass

    def update(self):
        pass

    def draw(self, surf):
        pass
