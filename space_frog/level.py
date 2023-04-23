import random

import pygame
from pygame.sprite import Group, GroupSingle

import space_frog.settings as S
from space_frog.player import Player
from space_frog.asteroids import SmallAsteroid, MediumAsteroid, LargeAsteroid, HugeAsteroid
from space_frog.background import Background
from space_frog.gate import Gate

class Level:
    def __init__(self, title, background_images, map):
        self.background_images = background_images
        self.title = title
        self.map = map

    def load_level(self, game):
        self.game = game
        # self.create_player()
        # self.add_asteroids() 
        # self.set_up_gates()
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
                if tile == "s": # start gate
                    self.game.entry = Gate(start_x, start_y, False, self.game.gates)
                    print(f"Entry coordinates are {start_x}, {start_y}")
                    self.game.player = Player(start_x, start_y, self.game.player_group)
                elif tile == "e": # exit gate
                    self.game.exit = Gate(start_x, start_y, True, self.game.gates)
                    print(f"Exit coordinates are {start_x}, {start_y}")
                elif tile == "a": # asteroids going towards exit
                    for i in range(0, random.randint(0, 1)):
                        self.asteroids_special.add(HugeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), speed=50, angle=-45))
                    for i in range(0, random.randint(0, 1)):
                         self.asteroids_special.add(LargeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                            random.randrange(start_y, start_y + S.TILE_SIZE), speed=52, angle=-45))
                    for i in range(0, random.randint(0, 3)):
                        self.asteroids_special.add(MediumAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), speed=51, angle=-45))
                    # for i in range(0, random.randint(0, 4)):
                    #     self.asteroids_special.add(SmallAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                    #                                        random.randrange(start_y, start_y + S.TILE_SIZE), speed=51, angle=45))
                elif tile == "r": # asteroids going right
                    # for i in range(0,1):
                    #     self.game.asteroids.add(HugeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                    #                                        random.randrange(start_y, start_y + S.TILE_SIZE), 90))
                    # for i in range(0,1):
                    #     self.game.asteroids.add(LargeAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                    #                                        random.randrange(start_y, start_y + S.TILE_SIZE), 90))
                    for i in range(0, random.randint(0, 1)):
                        self.game.asteroids.add(MediumAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), angle=0))
                    for i in range(0, random.randint(0, 4)):
                        self.game.asteroids.add(SmallAsteroid(random.randrange(start_x, start_x + S.TILE_SIZE),
                                                           random.randrange(start_y, start_y + S.TILE_SIZE), angle=0))
                else:
                    pass
        self.game.calculate_exit()
        # distance = self.game.entry.center.distance_to(self.game.exit.center)
        # self.asteroids_special.vector = pygame.math.Vector2.move_towards(self.game.entry.center, self.game.exit.center, distance)
        self.game.asteroids.add(iter(self.asteroids_special.sprites()))




    def add_background(self):
        self.game.background = Background(self.background_images[0], self.background_images[1], self.background_images[2])
        self.game.bg_group = Group()
        self.game.bg_group.add(self.game.background)

    def set_up_gates(self):
        self.game.gates = Group()
        self.game.entry = Gate(S.SCREEN_WIDTH / 2 - 25, S.SCREEN_HEIGHT / 2, False, self.game.gates)
        self.game.exit = Gate(3000, 3000, True, self.game.gates)
        self.game.calculate_exit()


    def create_player(self):
        self.game.player = Player(S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 2)
        self.game.player_group = GroupSingle()
        self.game.player_group.add(self.game.player)

    def add_asteroids(self):
        self.game.asteroids = Group()
        for i in range(5):
            self.game.asteroids.add(HugeAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(25):
            self.game.asteroids.add(SmallAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(10):
            self.game.asteroids.add(MediumAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT))) 
        for i in range(10):
            self.game.asteroids.add(LargeAsteroid(random.randrange(0, S.WORLD_WIDTH), random.randrange(0, S.WORLD_HEIGHT)))
        