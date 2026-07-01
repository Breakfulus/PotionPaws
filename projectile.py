import pygame

class Projectile:
    def __init__(self, description, pos, direction, team):

        # Movement Init
        self.pos = pygame.Vector2(pos)
        self.velocity = direction * description["speed"]
        # Projectile Properties
        self.timer = description["lifetime"] * 1000
        self.damage = description["damage"]
        self.alive = True
        self.team = team
        # Rendering
        # self.image = description["image"]
        # self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.pos += self.velocity
        if self.timer > 0:
            self.timer -= 1
        else:
            self.alive = False


    def draw(self, surf):
        pygame.draw.circle(surf, "red", self.pos, 15)