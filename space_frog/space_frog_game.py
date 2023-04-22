import sys
import copy

import pygame
from pygame import key
from pygame.surface import Surface
from pygame.sprite import Sprite

import space_frog.settings as S
from space_frog.player import Splat
from space_frog.hud import HUD
from space_frog.level import Level

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
        
        level_list = []
        level_list.append(Level("Level 1", ("blue_nebula", "small_stars_1", "big_stars_1")))
        level_list.append(Level("Level 2", ("pink_nebula", "small_stars_2", "big_stars_2")))
        self.levels = iter(level_list)
        self.load_next_level()
        self.start_game_level()

    def start_game_level(self):
        self.win = False
        self.viewport = Viewport()
        self.viewport.update(self.player)
        self.hud = HUD(self.screen, self.player)
        self.get_ready()
        self.set_clock()
        self.game_loop()

    def get_ready(self):
        self.hud.ready_screen(self.level)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    return
                
    def show_victory_screen(self):
        self.hud.end_screen()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    return


    def load_next_level(self):
        try:
            self.level = next(self.levels)
            self = self.level.load_level(self)
        except StopIteration:
            self.show_victory_screen()
            sys.exit(0)

    def reload_level(self):
        self = self.level.load_level(self)

    def set_clock(self):
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.fps = S.FPS    

    def game_loop(self):
        while True:
            self.handle_events()      
            self.draw()
            self.update()
            pygame.display.flip()
            self.delta = self.clock.tick(self.fps) * 0.001
            if self.win:
                break
        self.load_next_level()
        self.start_game_level()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and event.mod == pygame.KMOD_CTRL:
                    pass # debug
                elif event.key == pygame.K_r:
                    self.reload_level()
                    self.start_game_level()
                

    def update(self):
        self.player_group.update(self.delta, key.get_pressed())
        self.asteroids.update(self.delta, self.asteroids)
        self.gates.update(self.delta)
        self.viewport.update(self.player)
        if self.check_for_win():
            self.win = True
            return
        self.calculate_exit()
        self.hud.prep_info(self.player)
        self.hud.show_info()
        self.check_player_collisions()

    def check_for_win(self):
        if self.player.alive() and pygame.sprite.spritecollideany(self.exit, self.player_group, pygame.sprite.collide_mask):
            return True

    def check_player_collisions(self):
        if self.player.alive() and (collided_with := pygame.sprite.spritecollideany(self.player, self.asteroids, pygame.sprite.collide_mask)):
            if self.player.last_collision != collided_with:
                if self.player.speed <= S.DOCKING_SPEED:
                    # Moving slowly? Land on the asteroid
                    self.player.vector = copy.copy(collided_with.vector)
                    self.player.speed = collided_with.speed
                    self.player.last_collision = collided_with
                if self.player.speed > S.MAX_COLLISION_SPEED:
                    # Too fast? Go splat on the asteroid
                    self.player.kill()
                    splat = Splat(self.player.world_rect.left, self.player.world_rect.top)
                    if self.player.size >= collided_with.size:
                        collided_with.speed += self.player.speed
                    splat.vector = self.player.vector.reflect(collided_with.vector)
                    splat.speed = collided_with.speed
                    self.player_group.add(splat)
                else:
                    #Otherwise bounce off the asteroid.
                    v1 = self.player.speed
                    v2 = collided_with.speed
                    self.player.speed = abs((v1 * (self.player.size - collided_with.size) + 2 * collided_with.size * v2) 
                                            / (self.player.size + collided_with.size))
                    collided_with.speed = abs((v2 * (collided_with.size - self.player.size) + 2 * self.player.size * v1) 
                                              / (self.player.size + collided_with.size))
                    old_vector = self.player.vector
                    self.player.vector.reflect_ip(collided_with.vector)
                    collided_with.vector.reflect_ip(old_vector)
                    self.player.last_collision = collided_with
        else:
            self.player.last_collision = None

    def calculate_exit(self):
        self.player.distance_to_exit = self.player.center.distance_to(self.exit.center)

    def draw(self):
        self.viewport.update_rect(self.bg_group)
        self.viewport.update_rect(self.player_group)
        self.viewport.update_rect(self.asteroids)
        self.viewport.update_rect(self.gates)
        self.screen.fill((1, 13, 30))
        self.background.draw(self.screen)
        self.player_group.draw(self.screen)
        self.asteroids.draw(self.screen) 
        self.gates.draw(self.screen)


if __name__ == "__main__":
    Game().game_loop()