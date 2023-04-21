import random
import sys

import pygame
from pygame import key
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, GroupSingle

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



class Player(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        angle = random.randint(0, 360)
        self.image = pygame.image.load('space_frog/images/frog_frame.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.world_rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))
        self.speed = 10
        

    def update(self, delta, keys):
        if keys[pygame.K_UP]:
            self.speed += 5
        if keys[pygame.K_DOWN]:
            self.speed -= 5
        if keys[pygame.K_LEFT]:
            self.vector.rotate_ip(-5)
            # self.image = pygame.transform.rotate(self.image, -5)
        if keys[pygame.K_RIGHT]:
            self.vector.rotate_ip(5)
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

class Asteroid(Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('space_frog/images/asteroid1.png').convert_alpha()
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        angle = random.randint(0, 360)
        self.image = pygame.transform.scale(self.image, (width / random.randint(2, 15), height / random.randint(2, 15)))
        self.image = pygame.transform.rotate(self.image, angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.world_rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.vector.from_polar((1, angle))
        self.speed = random.randint(0, 60)


    def update(self, delta, group):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center

        if (collided_with := pygame.sprite.spritecollideany(self, group, pygame.sprite.collide_mask)):
            old_vector = self.vector
            self.vector.reflect_ip(collided_with.vector)
            collided_with.vector.reflect_ip(old_vector)


class Viewport:
    def __init__(self):
        self.left = 0
        self.top = 0

    def update(self, sprite):
        self.left = sprite.world_rect.left - (S.SCREEN_WIDTH / 2)
        self.top = sprite.world_rect.top - (S.SCREEN_HEIGHT / 2)

    def update_rect(self, group):
         for sprite in group:
             sprite.rect = sprite.world_rect.move(-self.left, -self.top)       

class Game:
    def __init__(self):
        pygame.display.init()
        # for m in pygame.display.list_modes():
        #     print(m)
        self.screen = pygame.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Frog!")
        self.player = Player(S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 2)
        self.player_group = GroupSingle()
        self.player_group.add(self.player)
        self.asteroids = Group()
        self.background = Background("blue_nebula", "small_stars_1", "big_stars_1")
        self.bg_group = Group()
        self.bg_group.add(self.background)
        self.viewport = Viewport()
        self.viewport.update(self.player)

        self.clock = pygame.time.Clock()
        self.delta = 0
        self.fps = S.FPS

        for i in range(50):
            self.asteroids.add(Asteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        

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
        self.viewport.update(self.player)
        self.check_player_collisions()

    def check_player_collisions(self):
        if self.player.alive() and (collided_with := pygame.sprite.spritecollideany(self.player, self.asteroids, pygame.sprite.collide_mask)):
            if self.player.speed <= 30:
                # Moving slowly? Land on the asteroid
                self.player.vector = collided_with.vector
                self.player.speed = collided_with.speed
            elif self.player.speed > 100:
                # Too fast? Go splat on the asteroid
                self.player.kill()
                splat = Splat(self.player.rect.left, self.player.rect.top)
                splat.vector = collided_with.vector
                splat.speed = collided_with.speed
                self.player_group.add(splat)
            else:
            #Otherwise bounce off the asteroid.
                old_vector = self.player.vector
                self.player.vector.reflect_ip(collided_with.vector)
                collided_with.vector.reflect_ip(old_vector)



    def draw(self):
        self.viewport.update_rect(self.bg_group)
        self.viewport.update_rect(self.player_group)
        self.viewport.update_rect(self.asteroids)
        self.background.draw(self.screen)
        self.player_group.draw(self.screen)
        self.asteroids.draw(self.screen) 


if __name__ == "__main__":
    Game().game_loop()