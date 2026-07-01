import pygame
from projectile import Projectile

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = list(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
bullets = []
bullet_count = 0
timer_list = []

TEMP = {
    "image": None,
    "lifetime": 1,
    "damage": 10,
    "speed": 8
}

while running:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - player_pos).normalize()
            projectile = Projectile(TEMP, player_pos, direction, "player")
            bullets.append(projectile)

    # Listen for pressed keys; Move if movement keys are pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos[1] -= 300 * dt
    if keys[pygame.K_s]:
        player_pos[1] += 300 * dt
    if keys[pygame.K_a]:
        player_pos[0] -= 300 * dt
    if keys[pygame.K_d]:
        player_pos[0] += 300 * dt
        

        
    # fill the screen
    screen.fill((26, 27, 33))

    # RENDER GAME HERE
    pygame.draw.circle(screen, "green", player_pos, 30)

    for proj in bullets:
        if proj.alive:
            proj.update()
            proj.draw(screen)
        else:
            bullets.remove(proj)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
