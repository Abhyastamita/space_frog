import random

from pygame.sprite import Group, GroupSingle

import space_frog.settings as S
from space_frog.player import Player
from space_frog.asteroids import SmallAsteroid, MediumAsteroid, LargeAsteroid, HugeAsteroid
from space_frog.background import Background
from space_frog.gate import Gate

class Level:
    def __init__(self, title, background_images):
        self.background_images = background_images
        self.title = title

    def load_level(self, game):
        self.game = game
        self.create_player()
        self.add_asteroids() 
        self.set_up_gates()
        self.add_background()
        return game

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
        