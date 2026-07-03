import pygame
import consts as c
from enemy_spawning import get_next_spawn_point
from projectile import Projectile
from enemy import Enemy
from player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
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

enemies = []

SPAWN_ENEMY = pygame.USEREVENT + 1
spawn_enemy_event = pygame.time.set_timer(SPAWN_ENEMY, 1000)

player = Player((screen.get_width() / 2, screen.get_height() / 2), TEMP_PLAYER)



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
        
        if event.type == SPAWN_ENEMY:
            new_enemy = Enemy(TEMP_ENEMY, get_next_spawn_point())
            enemies.append(new_enemy)
        
    # fill the screen
    screen.fill((26, 27, 33))

    for proj in bullets:
        if proj.alive:
            proj.update()
            proj.draw(screen)
        else:
            bullets.remove(proj)
    
    player.update(dt)
    player.draw(screen)

    for enemy in enemies:
        enemy.update(player, dt)
        enemy.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
