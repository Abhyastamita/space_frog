import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite

class Gate(Sprite):
    def __init__(self, x, y, exit, *groups):
        super().__init__(*groups)
        self.image = Surface((75, 75))
        if exit:
            self.image = pygame.image.load("space_frog/images/exit_gate.png").convert_alpha()
        else:
            self.image = pygame.image.load("space_frog/images/entry_gate.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.speed = 0

    def update(self, delta, *args):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center