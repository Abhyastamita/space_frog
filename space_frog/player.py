import random

import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        angle = random.randint(0, 360)
        self.image = pygame.image.load('space_frog/images/space_frog.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.world_rect = self.image.get_rect().move(x, y)
        self.size = 2

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))
        self.speed = 10
        self.fuel = 100.0
        self.last_collision = None
        self.distance_to_exit = None
        

    def update(self, delta, keys):
        if self.fuel > 0 and keys[pygame.K_UP]:
            self.speed += 5
            self.fuel -= 0.5
        if self.speed > 0 and keys[pygame.K_DOWN]:
            self.speed -= 5
        if self.fuel > 0 and keys[pygame.K_LEFT]:
            self.vector.rotate_ip(-5)
            self.fuel -= 0.25
            # self.image = pygame.transform.rotate(self.image, -5)
        if self.fuel > 0 and keys[pygame.K_RIGHT]:
            self.vector.rotate_ip(5)
            self.fuel -= 0.25
            # self.image = pygame.transform.rotate(self.image, 5)
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center

class Splat(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((25, 25))
        self.image.fill((0, 100, 25))
        self.world_rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.speed = 0

    def update(self, delta, *args):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center