import pygame
import pygame.freetype
import data.scripts.consts as c
import data.scripts.upgrades as up
import random
from data.scripts.enemy_spawning import get_next_spawn_point
from data.scripts.projectile import Projectile
from data.scripts.enemy import Enemy
from data.scripts.player import Player
from data.scripts.button import Button

# pygame setup
pygame.init()
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pygame.display.set_caption("PotionPaws PROTOTYPE v0.1.0")
clock = pygame.time.Clock()
dt = 0

# Game setup
running = True
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

def start_game():
    print("Game Starting...")
    player.reset_player()
    c.STATE = 1

main_menu_buttons = [
    Button((screen.get_width() / 2, screen.get_height() / 2), None, "Start Game", callback=lambda: start_game(), size=(300, 100))
]

upgrade_buttons = [
    Button((screen.get_width() / 2 - 300, screen.get_height() / 2), None, "Speed", callback=lambda: player.apply_upgrade(up.UPGRADES["Swift Brew"]), size=(250, 400)),
    Button((screen.get_width() / 2, screen.get_height() / 2), None, "Damage", callback=lambda: player.apply_upgrade(up.UPGRADES["Damage Elixer"]), size=(250, 400)),
    Button((screen.get_width() / 2 + 300, screen.get_height() / 2), None, "Health", callback=lambda: player.apply_upgrade(up.UPGRADES["Health Potion"]), size=(250, 400)),
]

while running:

    # Main Menu
    if c.STATE == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons:
                    if button.is_hovered:
                        button.clicked()
            
        # Fill the screen
        screen.fill((50, 50, 150))

        for button in main_menu_buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Upgrade Screen
    if c.STATE == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    run_start = pygame.time.get_ticks()
                    c.STATE = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in upgrade_buttons:
                    if button.is_hovered:
                        button.clicked()
                        player.needs_upgrade = False
                        c.STATE = 2
            
        # Fill the screen
        screen.fill((50, 50, 150))

        for button in upgrade_buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Game Screen
    if c.STATE == 2:
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
                c.STATE = 1
            
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
            c.STATE = 3

        for enemy in enemies[:]:
            if enemy.alive and player.alive:
                if enemy.rect.colliderect(player.rect):
                    player.apply_damage(enemy.damage)
                enemy.update(player, dt)
                enemy.draw(screen)
            else:
                enemies.remove(enemy)
        
        if c.STATE == 2:
            if seconds >= 0:
                seconds -= 1 * dt

        c.GAME_FONT.render_to(screen, (0, 0), f"Time: {round(seconds)}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 30), f"Health: {player.health}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 60), f"Level: {player.level}", (255, 0, 0))
        c.GAME_FONT.render_to(screen, (0, 90), f"EXP: {player.exp}/{player.exp_til_level_up}", (255, 0, 0))

        if seconds <= 0:
            player.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
            enemies = []
            bullets = []
            c.STATE = 4
            
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Loss Screen
    if c.STATE == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.reset_player()
                    seconds = total_seconds
                    c.STATE = 0
        
        # Fill the screen
        screen.fill((26, 27, 33))
        text = f"You lost. Space to return to menu."
        text_rect = c.GAME_FONT.get_rect(text)
        text_rect.center = (c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2)
        c.GAME_FONT.render_to(screen, text_rect, text, (255, 0, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    # Win Screen
    if c.STATE == 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    seconds = total_seconds
                    c.STATE = 0
        
        # Fill the screen
        screen.fill((26, 27, 33))

        text = f"You Won. Space to return to menu."
        text_rect = c.GAME_FONT.get_rect(text)
        text_rect.center = (c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2)
        c.GAME_FONT.render_to(screen, text_rect, text, (255, 0, 0))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

pygame.quit()
