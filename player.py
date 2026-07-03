import pygame

class Player():
    def __init__(self, pos, preset) -> None:
        self.pos = pygame.Vector2(pos)
        self.speed = preset["speed"]
        self.damage = preset["damage"]
        self.health = preset["health"]

    def update(self, dt):
        # Listen for pressed keys; Move if movement keys are pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.pos[1] -= self.speed * dt
        if keys[pygame.K_s]:
            self.pos[1] += self.speed * dt
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed * dt
        if keys[pygame.K_d]:
            self.pos[0] += self.speed * dt

    def draw(self, surf):
        pygame.draw.circle(surf, "green", self.pos, 30)