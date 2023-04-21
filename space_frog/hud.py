import pygame.freetype

pygame.freetype.init()

class HUD:
    def __init__(self, screen, player):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (250, 250, 250)
        self.font = pygame.freetype.SysFont('arial', 20)
        self.prep_info(player)

    def prep_info(self, player):
        player_speed = str(player.speed)
        player_fuel = str(player.fuel)
        self.player_info_image, self.player_info_rect = pygame.freetype.Font.render(self.font, f"Speed: {player_speed} | Fuel: {player_fuel}% full", self.text_color)
        self.player_info_image
        self.player_info_rect.left = self.screen_rect.left + 20
        self.player_info_rect.top = self.screen_rect.top + 20


    def show_info(self):
        self.screen.blit(self.player_info_image, self.player_info_rect)



