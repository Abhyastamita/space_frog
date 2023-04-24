import random

import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite

import space_frog.settings as S
from space_frog.sprite_sheet import SpriteSheet

class Player(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.angle = 0 # random.randint(0, 360)
        self.sheet = SpriteSheet(72, "space_frog/images/space_frog_full_sheet_72.png")
        self.image, self.mask = self.sheet.get_image(0, 0)
        self.world_rect = self.image.get_rect().move(x, y)
        self.size = 2

        self.up_anim = self.loop_rocket_animation("up")
        self.down_anim = self.loop_rocket_animation("down")
        self.left_anim = self.loop_rocket_animation("left")
        self.right_anim = self.loop_rocket_animation("right")

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, self.angle))
        self.speed = 100
        self.fuel = 100.0
        self.last_collision = None
        self.distance_to_exit = None
        self.off_screen = False
        self.docked = False
        self.docked_with = None
        self.sitting = self.sheet.get_image(0, 0)[0]
        self.jump_sequence = self.sheet.get_strip(0)[0][0:5]
        self.land_sequence = self.sheet.get_strip(0)[0][6:12]
        self.animation_list = [self.sitting, self.sitting, self.sitting, self.sitting]
        self.animation_list.extend(self.jump_sequence)
    

    def loop_rocket_animation(self, direction):
        if direction == "up":
            strip, mask = self.sheet.get_strip(1)
        elif direction == "down":
            strip, mask = self.sheet.get_strip(2)
        elif direction == "right":
            strip, mask = self.sheet.get_strip(3)
        elif direction == "left":
            strip, mask = self.sheet.get_strip(4)
        strip = strip[0:2] # Only two frames in rocket animation
        mask = mask[0:2]
        while True:
            for i in range (0, 2):
                yield strip[i], mask[i]

    def update(self, delta, keys):
        rocket = False
        if self.docked:
            self.animation_list.append(self.sitting)
            if keys[pygame.K_UP]:
                self.docked = False
                self.speed += 10
                self.docked_with = None
                self.animation_list.extend(self.jump_sequence)
        else:
            if self.fuel > 0 and keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.speed += 5
                self.fuel -= 0.5
                self.image, self.mask = next(self.up_anim)
                rocket = True
            if self.speed > 0 and keys[pygame.K_DOWN]:
                self.speed -= 5
                self.image, self.mask = next(self.down_anim)
                rocket = True
            if self.fuel > 0 and keys[pygame.K_LEFT]:
                self.vector.rotate_ip(-5)
                self.fuel -= 0.25
                self.image, self.mask = next(self.left_anim)
                rocket = True
                self.angle += 5
            if self.fuel > 0 and keys[pygame.K_RIGHT]:
                self.vector.rotate_ip(5)
                self.fuel -= 0.25
                self.image, self.mask = next(self.right_anim)
                rocket = True
                self.angle -= 5
        if not rocket:
            if self.animation_list:
                self.image = self.animation_list.pop(0)
            else:
                self.image, self.mask = self.sheet.get_image(0, 6)
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center
        self.mask = pygame.mask.from_surface(self.image)

        if self.world_rect.left > S.WORLD_WIDTH or self.world_rect.left < 0 \
            or self.world_rect.top > S.WORLD_HEIGHT or self.world_rect.top < 0:
            self.off_screen = True
        else:
            self.off_screen = False
            

class Splat(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((25, 25))
        self.image = pygame.image.load("space_frog/images/splat.png").convert_alpha()
        self.world_rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.speed = 0

    def update(self, delta, *args):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center