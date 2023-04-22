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
        player_speed = str(round(player.speed, 2))
        player_fuel = str(player.fuel)
        player_distance = str(round(player.distance_to_exit, 2))
        self.text_lines = []
        speed_image_rect = pygame.freetype.Font.render(self.font, f"Speed: {player_speed} m/s", self.text_color)
        speed_image_rect[1].left = self.screen_rect.left + 20
        speed_image_rect[1].top = self.screen_rect.top + 20
        self.text_lines.append(speed_image_rect)
        fuel_image_rect = pygame.freetype.Font.render(self.font, f"Fuel: {player_fuel}% full", self.text_color)
        fuel_image_rect[1].left = self.screen_rect.left + 20
        fuel_image_rect[1].top = self.screen_rect.top + 45
        self.text_lines.append(fuel_image_rect)
        exit_image_rect = pygame.freetype.Font.render(self.font, f"Distance to exit: {player_distance} m", self.text_color)
        exit_image_rect[1].left = self.screen_rect.left + 20
        exit_image_rect[1].top = self.screen_rect.top + 70
        self.text_lines.append(exit_image_rect)


    def show_info(self):
        for line in self.text_lines:
            self.screen.blit(line[0], line[1])



