import pygame
import random

class Enemy():
    def __init__(self, description, pos) -> None:
        self.pos = pygame.Vector2(pos)
        self.alive = True
        self.rect = pygame.rect.Rect(pos[0], pos[1], 30, 30)

        self.health = description["health"]
        self.damage = description["damage"]
        self.speed = description["speed"]


    def update(self, player, dt):
        if self.alive:
            if self.health <= 0:
                player.gain_exp(random.randint(5, 25))
                self.alive = False
            direction = (player.pos - self.pos).normalize()
            self.velocity = direction * self.speed

            self.pos += self.velocity * dt
            self.rect.center = self.pos
        else:
             self.pos = (0, 0)
    
    def draw(self, surf):
        pygame.draw.circle(surf, "red", self.rect.center, 30)