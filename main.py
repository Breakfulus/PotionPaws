import pygame
import pygame.freetype
import consts as c
import random
from enemy_spawning import get_next_spawn_point
from projectile import Projectile
from enemy import Enemy
from player import Player
from button import Button

# pygame setup
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

# Game setup
run_start = pygame.time.get_ticks()
running = True
STATE = 0
timer = 2 * 60

# Enemy, player, proj setup
TEMP_ENEMY = {
    "image": None,
    "health": 50,
    "damage": 10,
    "speed": 150
}

TEMP_PLAYER = {
    "image": None,
    "health": 100,
    "damage": 10,
    "speed": 170
}

TEMP = {
    "image": None,
    "lifetime": 1,
    "damage": 10,
    "speed": 8
}

enemies = []
bullets = []
buttons = [
    Button((screen.get_width() / 2, screen.get_height() / 2), None, None, "Test"),
    Button((screen.get_width() / 2 - 300, screen.get_height() / 2), None, None, "Test"),
    Button((screen.get_width() / 2 + 300, screen.get_height() / 2), None, None, "Test")
]

SPAWN_ENEMY = pygame.USEREVENT + 1
spawn_enemy_event = pygame.event.Event(SPAWN_ENEMY)
pygame.time.set_timer(spawn_enemy_event, 1000)

player = Player((screen.get_width() / 2, screen.get_height() / 2), TEMP_PLAYER)

while running:
    if STATE == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    STATE = 1
            

        # Fill the screen
        screen.fill((50, 50, 150))

        for button in buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    if STATE == 1:
        # Events loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                direction = (mouse_pos - player.pos).normalize()
                projectile = Projectile(TEMP, player.pos, direction, "player")
                bullets.append(projectile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    STATE = 0
            
            if event.type == SPAWN_ENEMY:
                new_enemy = Enemy(TEMP_ENEMY, get_next_spawn_point())
                enemies.append(new_enemy)
                pygame.time.set_timer(spawn_enemy_event, 1000 * random.randint(1, 5))
            
        # Fill the screen
        screen.fill((26, 27, 33))

        for proj in bullets[:]:
            for enemy in enemies:
                if proj.rect.colliderect(enemy.rect):
                    enemy.health -= proj.damage
                    proj.alive = False

            if proj.alive:
                proj.update()
                proj.draw(screen)
            else:
                bullets.remove(proj)
        
        if player.alive:
            player.update(dt)
            player.draw(screen)
        else:
            player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            enemies = []
            bullets = []
            STATE = 2

        for enemy in enemies[:]:
            if enemy.alive and player.alive:
                if enemy.rect.colliderect(player.rect):
                    player.apply_damage(enemy.damage)
                enemy.update(player, dt)
                enemy.draw(screen)
            else:
                enemies.remove(enemy)
        
        time_left = timer
        elapsed = (pygame.time.get_ticks() - run_start) // 1000
        time_left = timer - elapsed

        c.GAME_FONT.render_to(screen, (0, 0), f"Time: {time_left}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 30), f"Health: {player.health}", (255, 0, 0))

        if time_left <= 0:
            player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            enemies = []
            bullets = []
            STATE = 3
            
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    if STATE == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.alive = True
                    player.health = player.preset["health"]
                    run_start = pygame.time.get_ticks()
                    STATE = 1
        
        # Fill the screen
        screen.fill((255, 0, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    if STATE == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_start = pygame.time.get_ticks()
                    STATE = 1
        
        # Fill the screen
        screen.fill((0, 255, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()
