import pygame

class Button:
    def __init__(self, description, pos):
        self.pos = pygame.Vector2(pos)

        self.image = description["image"]
        self.rect = self.image.get_rect(center=self.pos)

    def check_if_hovered(self):
        pass

    def clicked(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
