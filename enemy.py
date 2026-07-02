import pygame

class Enemy():
    def __init__(self, description, pos) -> None:
        self.pos = pos

        self.health = description["health"]
        self.damage = description["damage"]
        self.speed = description["speed"]
    
    def draw(self, surf):
        pygame.draw.circle(surf, "red", self.pos, 30)