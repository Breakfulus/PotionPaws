import pygame

class Player():
    def __init__(self, pos, preset) -> None:
        self.preset = preset
        self.pos = pygame.Vector2(pos)
        self.speed = self.preset["speed"]
        self.damage = self.preset["damage"]
        self.health = self.preset["health"]
        self.alive = True
        self.rect = pygame.rect.Rect(pos[0], pos[1], 30, 30)
        self.last_hit = 0
    
    def apply_damage(self, damage):

        now = pygame.time.get_ticks()

        if (
            now - self.last_hit >= 0.5 * 1000
        ):  # Invincibility time; prevents entities from getting hit by same proj twice
            self.health -= damage

            self.last_hit = (
                now  # Updates to ost recent time entity was damaged
            )

    def update(self, dt):
        if self.alive:

            if self.health <= 0:
                self.alive = False

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
            
            self.rect.center = round(self.pos.x), round(self.pos.y)

    def draw(self, surf):
        pygame.draw.circle(surf, "green", self.pos, 30)