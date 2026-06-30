import pygame

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = list(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
bullets = {}
bullet_count = 0
timer_list = []

while running:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(bullet_count)
            timer_list.append(1 * 1000)
            current_pos = (player_pos[0], player_pos[1])
            bullets[bullet_count] = current_pos
            bullet_count += 1


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

    bullet_list = bullets.copy().items()
    v_x, v_y = 1, 1
    for bullet, pos in bullet_list:
        pos = list(pos)
        if timer_list[bullet] == 0:
            bullets.pop(bullet)
        else:
            timer_list[bullet] -= 1
        
        pos[0] += v_x
        pos[1] += v_y
        bullets[bullet] = pos
        pygame.draw.circle(screen, "red", pos, 15)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
