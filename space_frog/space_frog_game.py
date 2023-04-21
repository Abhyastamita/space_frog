import random
import sys

import pygame
from pygame import key
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, GroupSingle

import space_frog.settings as S

class Player(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((25, 25))
        # width = self.image.get_rect().width
        # height = self.image.get_rect().height
        angle = random.randint(0, 360)
        self.image.fill((0, 200, 50))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))
        self.speed = 100
        

    def update(self, delta, keys):
        if keys[pygame.K_UP]:
            self.speed += 5
        if keys[pygame.K_DOWN]:
            self.speed -= 5
        if keys[pygame.K_LEFT]:
            self.vector.rotate_ip(-5)
            pygame.transform.rotate(self.image, -5)
        if keys[pygame.K_RIGHT]:
            self.vector.rotate_ip(5)
            pygame.transform.rotate(self.image, 5)
        self.center += self.vector * delta * self.speed
        self.rect.center = self.center

class Splat(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = Surface((25, 25))
        self.image.fill((0, 100, 25))
        self.rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.speed = 0

    def update(self, delta, *args):
        self.center += self.vector * delta * self.speed
        self.rect.center = self.center

class Asteroid(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('space_frog/images/asteroid1.png').convert_alpha()
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        angle = random.randint(0, 360)
        self.image = pygame.transform.scale(self.image, (width / random.randint(2, 10), height / random.randint(2, 10)))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))
        self.speed = random.randint(0, 60)

    def update(self, delta, group):
        self.center += self.vector * delta * self.speed
        self.rect.center = self.center

        if (collided_with := pygame.sprite.spritecollideany(self, group)):
            old_vector = self.vector
            self.vector.reflect_ip(collided_with.vector)
            collided_with.vector.reflect_ip(old_vector)

        

class Game:
    def __init__(self):
        pygame.display.init()
        # for m in pygame.display.list_modes():
        #     print(m)
        self.screen = pygame.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Frog!")
        self.player = Player(500, 500)
        self.player_group = GroupSingle()
        self.player_group.add(self.player)
        self.asteroids = Group()
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.fps = S.FPS
        for i in range(16):
            self.asteroids.add(Asteroid(random.randrange(0, S.SCREEN_WIDTH), random.randrange(0, S.SCREEN_HEIGHT)))

    def game_loop(self):
        while True:
            self.handle_events()      
            self.draw()
            self.update()
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps) * 0.001


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and event.mod == pygame.KMOD_CTRL:
                    pass # debug
                elif event.key == pygame.K_r:
                    Game().game_loop()
                

    def update(self):
        self.player_group.update(self.delta, key.get_pressed())
        self.asteroids.update(self.delta, self.asteroids)
        if self.player.alive() and (collided_with := pygame.sprite.spritecollideany(self.player, self.asteroids)):
            if self.player.speed > 70:
                self.player.kill()
                splat = Splat(self.player.rect.left, self.player.rect.top)
                splat.vector = collided_with.vector
                splat.speed = collided_with.speed
                self.player_group.add(splat)
            old_vector = self.player.vector
            self.player.vector.reflect_ip(collided_with.vector)
            collided_with.vector.reflect_ip(old_vector)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player_group.draw(self.screen)
        self.asteroids.draw(self.screen)


if __name__ == "__main__":
    Game().game_loop()