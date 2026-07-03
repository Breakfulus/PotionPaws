import pygame

class Enemy():
    def __init__(self, description, pos) -> None:
        self.pos = pygame.Vector2(pos)
        self.alive = True

        self.health = description["health"]
        self.damage = description["damage"]
        self.speed = description["speed"]


    def update(self, player, dt):
        if self.alive:
            direction = (player.pos - self.pos).normalize()
            self.velocity = direction * self.speed

            self.pos += self.velocity * dt
        else:
             pass
    
    def draw(self, surf):
        pygame.draw.circle(surf, "red", self.pos, 30)