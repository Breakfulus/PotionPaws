import pygame
import pygame.freetype
import consts as c
import upgrades as up
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
STATE = 1
total_seconds = 5 * 60
seconds = total_seconds

# Enemy, player, proj setup
TEMP_ENEMY = {
    "image": None,
    "health": 50,
    "damage": 10,
    "speed": 150
}

TEMP_PLAYER = {
    "image": None,
    "health": 50,
    "damage": 10,
    "speed": 125
}

TEMP = {
    "image": None,
    "lifetime": 1,
    "damage": 10,
    "speed": 8
}

SPAWN_ENEMY = pygame.USEREVENT + 1
spawn_enemy_event = pygame.event.Event(SPAWN_ENEMY)
pygame.time.set_timer(spawn_enemy_event, 1000)

player = Player((screen.get_width() / 2, screen.get_height() / 2), TEMP_PLAYER)

enemies = []
bullets = []
buttons = [
    Button((screen.get_width() / 2 - 300, screen.get_height() / 2), None, "Speed", callback=lambda: player.apply_upgrade(up.UPGRADES["Swift Brew"]), size=(250, 400)),
    Button((screen.get_width() / 2, screen.get_height() / 2), None, "Damage", callback=lambda: player.apply_upgrade(up.UPGRADES["Damage Elixer"]), size=(250, 400)),
    Button((screen.get_width() / 2 + 300, screen.get_height() / 2), None, "Health", callback=lambda: player.apply_upgrade(up.UPGRADES["Health Potion"]), size=(250, 400)),
]


while running:
    # Upgrade Screen
    if STATE == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    run_start = pygame.time.get_ticks()
                    STATE = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered:
                        button.clicked()
                        player.needs_upgrade = False
                        STATE = 1
            
        # Fill the screen
        screen.fill((50, 50, 150))

        for button in buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Game Screen
    if STATE == 1:
        # Events loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                direction = (mouse_pos - player.pos).normalize()
                projectile = Projectile(TEMP, player.pos, direction, "player")
                projectile.damage = player.damage
                bullets.append(projectile)
            
            if event.type == SPAWN_ENEMY:
                new_enemy = Enemy(TEMP_ENEMY, get_next_spawn_point())
                enemies.append(new_enemy)
                pygame.time.set_timer(spawn_enemy_event, 1000 * random.randint(1, 5))
            
            if player.needs_upgrade:
                STATE = 0
            
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
            player.reset_player()
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
        
        if STATE == 1:
            if seconds >= 1:
                seconds -= 1 * dt

        c.GAME_FONT.render_to(screen, (0, 0), f"Time: {round(seconds)}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 30), f"Health: {player.health}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 60), f"Level: {player.level}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 90), f"EXP: {player.exp}/{player.exp_til_level_up}", (255, 0, 0))

        if seconds <= 0:
            player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            enemies = []
            bullets = []
            STATE = 3
            
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Loss Screen
    if STATE == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.reset_player()
                    seconds = total_seconds
                    STATE = 1
        
        # Fill the screen
        screen.fill((255, 0, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Win Screen
    if STATE == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    seconds = total_seconds
                    STATE = 1
        
        # Fill the screen
        screen.fill((0, 255, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()
