import pygame

class Enemy():
    def __init__(self, description, pos, target) -> None:
        self.pos = pygame.Vector2(pos)
        self.alive = True
        self.target = target

        self.health = description["health"]
        self.damage = description["damage"]
        self.speed = description["speed"]

    def move_towards_player(self):
            direction = (self.target.position - self.pos).normalize()
            self.velocity = direction * self.speed

            self.pos += self.velocity

    def update(self):
        if self.alive:
            self.move_towards_player()
        else:
             pass
    
    def draw(self, surf):
        pygame.draw.circle(surf, "red", self.pos, 30)