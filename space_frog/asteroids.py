import random

import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, x, y, size = 1, scale_range = (2, 15), angle = None, speed = None, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('space_frog/images/asteroid1.png').convert_alpha()
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        if not angle:
            angle = random.randint(0,360)
        self.speed = speed
        if not self.speed:
            self.speed = random.randint(0, 60)
        self.image = pygame.transform.scale(self.image, (width / random.randint(scale_range[0], scale_range[1]), height / random.randint(scale_range[0], scale_range[1])))
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.world_rect = self.image.get_rect().move(x, y)
        self.size = size
        self.last_collision = None

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))


    def update(self, delta, group):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center

        if (collided_with := pygame.sprite.spritecollideany(self, group, pygame.sprite.collide_mask)):
            if collided_with != self.last_collision:
                v1 = self.speed
                v2 = collided_with.speed
                self.speed = (v1 * (self.size - collided_with.size) + 2 * collided_with.size * v2) / (self.size + collided_with.size)
                collided_with.speed = (v2 * (collided_with.size - self.size) + 2 * self.size * v1) / (self.size + collided_with.size)
                old_vector = self.vector
                self.vector.reflect_ip(collided_with.vector)
                collided_with.vector.reflect_ip(old_vector)
                self.last_collision = collided_with
        else:
            self.last_collision = None


class SmallAsteroid(Asteroid):
    def __init__(self, x, y, angle = None, speed = None, *groups):
        super().__init__(x, y, size = 1, scale_range = (15, 18), angle = angle, speed = speed, *groups)


class MediumAsteroid(Asteroid):
    def __init__(self, x, y, angle = None, speed = None, *groups):
        super().__init__(x, y, size = 3, scale_range = (6, 10), angle = angle, speed = speed, *groups)

class LargeAsteroid(Asteroid):
    def __init__(self, x, y, angle = None, speed = None, *groups):
        super().__init__(x, y, size = 4, scale_range = (3, 5), angle = angle, speed = speed, *groups)

class HugeAsteroid(Asteroid):
    def __init__(self, x, y, angle = None, speed = None, *groups):
        super().__init__(x, y, size = 5, scale_range = (1, 2), angle = angle, speed = speed, *groups)