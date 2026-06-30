import pygame

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
bullets = {}
bullet_count = 0
timer_list = []

while running:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Listen for pressed keys; Move if movement keys are pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    if keys[pygame.K_SPACE]:
        print(bullet_count)
        timer_list.append(1 * 1000)
        current_pos = (pygame.rect.Rect(player_pos.x, player_pos.y, 15, 15).x, pygame.rect.Rect(player_pos.x, player_pos.y, 15, 15).y)
        bullets[bullet_count] = current_pos
        bullet_count += 1
        

    # fill the screen
    screen.fill((26, 27, 33))

    # RENDER GAME HERE
    pygame.draw.circle(screen, "green", player_pos, 30)

    bullet_list = bullets.copy().items()
    for bullet in bullet_list:
        if timer_list[bullet[0]] == 0:
            bullets.pop(bullet[0])
        else:
            timer_list[bullet[0]] -= 1
        
            
        pygame.draw.circle(screen, "red", bullet[1], 15)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
