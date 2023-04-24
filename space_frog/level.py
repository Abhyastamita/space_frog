import random

import pygame
from pygame.sprite import Group, GroupSingle

import space_frog.settings as S
from space_frog.player import Player
from space_frog.asteroids import SmallAsteroid, MediumAsteroid, LargeAsteroid, HugeAsteroid, Asteroid
from space_frog.background import Background
from space_frog.gate import Gate

class Level:
    def __init__(self, title, background_images, map):
        self.background_images = background_images
        self.title = title
        self.map = map

    def load_level(self, game):
        self.game = game
        self.read_map()
        self.add_background()
        return game
    
    def read_map(self):
        self.game.gates = Group()
        self.asteroids_special = Group()
        self.game.asteroids = Group()
        self.game.player_group = GroupSingle()
        for row, tiles in enumerate(self.map):
            start_y = row * S.TILE_SIZE
            for col, tile in enumerate(tiles):
                start_x = col * S.TILE_SIZE
                dice_roll = random.randint(1, 6)
                if tile == "s": # start gate
                    self.game.entry = Gate(start_x, start_y, False, self.game.gates)
                    self.game.player = Player(start_x, start_y, self.game.player_group)
                elif tile == "e": # exit gate
                    self.game.exit = Gate(start_x, start_y, True, self.game.gates)
                elif tile == "a": # asteroids going towards exit
                    if dice_roll == 6:
                        self.asteroids_special.add(HugeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), speed=50, angle=-45))
                    elif dice_roll < 3:
                         for i in range(0, 2):
                            self.asteroids_special.add(LargeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), speed=52, angle=-45))
                    elif dice_roll < 1:
                        for i in range(0, 3):
                            self.asteroids_special.add(MediumAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), speed=51, angle=-45))
                    else:
                        for i in range(0, 5):
                            self.asteroids_special.add(SmallAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), speed=51, angle=45))
                elif tile == "r": # asteroids going right
                    if dice_roll > 5:
                        for i in range(0,1):
                            self.game.asteroids.add(LargeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), angle=3, speed = 80))
                    else:
                        self.game.asteroids.add(MediumAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                        random.randrange(start_y, start_y + S.TILE_SIZE), angle=0, speed = 80))
                        for i in range(0, 3):
                            self.game.asteroids.add(SmallAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), angle=0, speed = 82))
                elif tile == "H":
                    orbit_center = HugeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), speed=0, angle=-0)
                    self.game.asteroids.add(orbit_center)
                elif tile == "o":
                    for i in range(0, 3):
                            self.asteroids_special.add(MediumAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE)))
                else:
                    pass
        self.game.calculate_exit()
        if self.title == "Level 2":
            for asteroid in self.asteroids_special:
                asteroid.set_orbit(orbit_center, 1000)
            self.game.exit.set_orbit(orbit_center)
        self.game.asteroids.add(iter(self.asteroids_special.sprites()))




    def add_background(self):
        self.game.background = Background(self.background_images[0], self.background_images[1], self.background_images[2])
        self.game.bg_group = Group()
        self.game.bg_group.add(self.game.background)
        