import pygame
import consts as c

class Button:
    def __init__(self, pos, image, rect, text, context):
        self.context = context
        self.pos = pygame.Vector2(pos)
        self.image = image
        self.text = text

        # If button doesnt have an image then create placeholder surf
        if self.image == None:
            img = pygame.Surface((250, 400))
            img.fill((25, 25, 50))
            self.image = img

        self.rect = self.image.get_rect()
        self.text = text
        self.is_hovered = False

    def clicked(self):
        click_func = self.context["clicked_effect"]
        click_func()

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)


    def draw(self, surf):
        self.rect = self.image.get_rect()
        self.rect.center = round(self.pos.x), round(self.pos.y)

        surf.blit(self.image, self.rect)

        if self.is_hovered:
            copy = self.image.copy()
            copy.fill((10, 10, 10), special_flags=pygame.BLEND_RGB_ADD)
            surf.blit(copy, self.rect)
        
        if self.text:
            text_rect = pygame.rect.Rect(self.image.get_width() // 2, self.image.get_height() // 2, 30, 30)
            text_rect.center = (self.image.get_width() // 2, self.image.get_height() // 2)
            c.GAME_FONT.render_to(self.image, text_rect, self.text, "red")



