import pygame

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen
    screen.fill("purple")

    # RENDER GAME HERE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
