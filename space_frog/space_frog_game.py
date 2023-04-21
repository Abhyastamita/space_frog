import random
import sys

import pygame
from pygame import key
from pygame.surface import Surface
from pygame.sprite import Sprite, Group, GroupSingle

import space_frog.settings as S
from space_frog.player import Player, Splat
from space_frog.asteroids import SmallAsteroid, MediumAsteroid, LargeAsteroid, HugeAsteroid
from space_frog.background import Background
from space_frog.hud import HUD


class Gate(Sprite):
    def __init__(self, x, y, exit, *groups):
        super().__init__(*groups)
        self.image = Surface((75, 75))
        if exit:
            self.image.fill((0, 255, 0))
        else:
            self.image.fill((255, 0, 0))
        self.world_rect = self.image.get_rect().move(x, y)

        self.center = pygame.Vector2(self.world_rect.center)
        self.vector = pygame.Vector2()
        self.speed = 0

    def update(self, delta, *args):
        self.center += self.vector * delta * self.speed
        self.world_rect.center = self.center


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
        self.create_player()
        self.add_asteroids() 
        self.add_gates()
        self.add_background()
        self.viewport = Viewport()
        self.viewport.update(self.player)
        self.hud = HUD(self.screen, self.player)
        self.set_clock()

    def set_clock(self):
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.fps = S.FPS

    def add_background(self):
        self.background = Background("blue_nebula", "small_stars_1", "big_stars_1")
        self.bg_group = Group()
        self.bg_group.add(self.background)

    def add_gates(self):
        self.gates = Group()
        self.entry_gate = Gate(S.SCREEN_WIDTH / 2 - 5, S.SCREEN_HEIGHT / 2, False, self.gates)
        self.exit_gate = Gate(3000, 3000, self.gates)

    def create_player(self):
        self.player = Player(S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 2)
        self.player_group = GroupSingle()
        self.player_group.add(self.player)

        

    def add_asteroids(self):
        self.asteroids = Group()
        for i in range(5):
            self.asteroids.add(HugeAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(25):
            self.asteroids.add(SmallAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(10):
            self.asteroids.add(MediumAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(10):
            self.asteroids.add(LargeAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT)))
        

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
        self.hud.prep_info(self.player)
        self.asteroids.update(self.delta, self.asteroids)
        self.gates.update(self.delta)
        self.viewport.update(self.player)
        self.hud.show_info()
        self.check_player_collisions()

    def check_player_collisions(self):
        if self.player.alive() and (collided_with := pygame.sprite.spritecollideany(self.player, self.asteroids, pygame.sprite.collide_mask)):
            if self.player.last_collision != collided_with:
                if self.player.speed <= 30:
                    # Moving slowly? Land on the asteroid
                    self.player.vector = collided_with.vector
                    self.player.speed = collided_with.speed
                    self.player.last_collision = collided_with
                if self.player.speed > 120:
                    # Too fast? Go splat on the asteroid
                    self.player.kill()
                    splat = Splat(self.player.world_rect.left, self.player.world_rect.top)
                    if self.player.size >= collided_with.size:
                        collided_with.speed += self.player.speed
                    splat.vector = collided_with.vector
                    splat.speed = collided_with.speed
                    self.player_group.add(splat)
                else:
                    #Otherwise bounce off the asteroid.
                    v1 = self.player.speed
                    v2 = collided_with.speed
                    self.player.speed = (v1 * (self.player.size - collided_with.size) + 2 * collided_with.size * v2) / (self.player.size + collided_with.size)
                    collided_with.speed = (v2 * (collided_with.size - self.player.size) + 2 * self.player.size * v1) / (self.player.size + collided_with.size)
                    old_vector = self.player.vector
                    self.player.vector.reflect_ip(collided_with.vector)
                    collided_with.vector.reflect_ip(old_vector)
                    self.player.last_collision = collided_with
        else:
            self.player.last_collision = None



    def draw(self):
        self.viewport.update_rect(self.bg_group)
        self.viewport.update_rect(self.player_group)
        self.viewport.update_rect(self.asteroids)
        self.viewport.update_rect(self.gates)
        self.background.draw(self.screen)
        self.player_group.draw(self.screen)
        self.asteroids.draw(self.screen) 
        self.gates.draw(self.screen)


if __name__ == "__main__":
    Game().game_loop()