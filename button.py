import pygame

class Button:
    def __init__(self, pos, image, rect, text):
        self.pos = pygame.Vector2(pos)
        self.image = image

        # If button doesnt have an image then create placeholder surf
        if self.image == None:
            img = pygame.Surface((250, 400))
            img.fill((25, 25, 50))
            self.image = img

        self.rect = self.image.get_rect()
        self.text = text
        self.is_hovered = False

    def check_if_hovered(self, mouse_pos):
        if mouse_pos:
            is_coliding = self.rect.collidepoint(mouse_pos)

            if is_coliding:
                self.is_hovered = True
            else:
                self.is_hovered = False

    def clicked(self):
        pass

    def update(self, mouse_pos):
        self.check_if_hovered(mouse_pos)

    def draw(self, surf):
        self.rect = self.image.get_rect()
        self.rect.center = round(self.pos.x), round(self.pos.y)

        surf.blit(self.image, self.rect)
        if self.is_hovered:
            copy = self.image.copy()
            copy.fill((10, 10, 10), special_flags=pygame.BLEND_RGB_ADD)
            surf.blit(copy, self.rect)



