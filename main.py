import pygame
from projectile import Projectile
from enemy import Enemy
from player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

bullets = []
bullet_count = 0
timer_list = []

TEMP_ENEMY = {
    "image": None,
    "health": 10,
    "damage": 10,
    "speed": 150
}

TEMP_PLAYER = {
    "image": None,
    "health": 10,
    "damage": 10,
    "speed": 300
}

TEMP = {
    "image": None,
    "lifetime": 1,
    "damage": 10,
    "speed": 8
}


player = Player((screen.get_width() / 2, screen.get_height() / 2), TEMP_PLAYER)

new_enemy = Enemy(TEMP_ENEMY, (1, 1))

while running:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - player.pos).normalize()
            projectile = Projectile(TEMP, player.pos, direction, "player")
            bullets.append(projectile)
        
    # fill the screen
    screen.fill((26, 27, 33))

    for proj in bullets:
        if proj.alive:
            proj.update()
            proj.draw(screen)
        else:
            bullets.remove(proj)
    
    player.update(dt)
    new_enemy.update(player, dt)

    player.draw(screen)
    new_enemy.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
