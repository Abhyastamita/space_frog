import pygame
from pygame.sprite import Sprite

import space_frog.settings as S

class Background(Sprite):
    def __init__(self, base, star1, star2, *groups):
        super().__init__(*groups)
        self.bg_images = self.load_background_images(base, star1, star2)
        self.width = self.bg_images[0].get_width()
        assert self.width == S.WORLD_WIDTH
        self.world_rect = self.bg_images[0].get_rect().move(0, 0)

    def load_background_images(self, base, star1, star2):
        bg_images = []
        bg_images.append(pygame.image.load(f"space_frog/images/background/{base}.png").convert())
        bg_images.append(pygame.image.load(f"space_frog/images/background/{star1}.png").convert_alpha())
        bg_images.append(pygame.image.load(f"space_frog/images/background/{star2}.png").convert_alpha())
        return bg_images

    def draw(self, screen):
        speed = 1
        for i in self.bg_images:
            screen.blit(i, (self.rect.x * speed, self.rect.y * speed))
            speed += 0.5