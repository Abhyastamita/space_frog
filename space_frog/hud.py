import pygame.freetype
import space_frog.settings as S
from space_frog.sprite_sheet import SpriteSheet

pygame.freetype.init()

class HUD:
    def __init__(self, screen, player):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (250, 250, 250)
        self.font = pygame.freetype.SysFont('arial', 20)
        self.large_font = pygame.freetype.SysFont('arial', 40)
        self.prep_info(player)
        self.sheet = SpriteSheet(72, "space_frog/images/space_frog_full_sheet_72.png")

    def prep_info(self, player):
        player_speed = str(round(player.speed, 2))
        player_fuel = str(player.fuel)
        player_distance = str(round(player.distance_to_exit, 2))
        if player.speed > S.MAX_COLLISION_SPEED: 
            speed_message = "- WARNING: TOO FAST"
            speed_color = (250, 0, 0)
        elif player.speed < S.DOCKING_SPEED: 
            speed_message = "- Docking Speed"
            speed_color = (50, 250, 70)
        else:
            speed_message = ""
            speed_color = (250, 250, 250)
        if player.fuel < 15:
            fuel_color = (250, 0, 0)
        elif player.fuel < 35:
            fuel_color = (255, 191, 0)
        else:
            fuel_color = (250, 250, 250)
        self.text_lines = []
        text_image_rect = self.prepare_multiline((20, 20), self.font, f"Speed: {player_speed} {speed_message}", speed_color)
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((20, 45), self.font, f"Fuel: {player_fuel}% full", fuel_color)
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((20, 70), self.font, f"Distance to exit: {player_distance} m", self.text_color)
        self.text_lines.append(text_image_rect)
        if player.off_screen:
            text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 380, S.SCREEN_HEIGHT / 2 + 150), self.large_font, f"Entering deep space. There is nothing out here to see.", self.text_color)
            self.text_lines.append(text_image_rect)
        if player.fuel <= 0:
            text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 380, S.SCREEN_HEIGHT / 2 + 200), self.large_font, f"Out of fuel. Press R to restart.", self.text_color)
            self.text_lines.append(text_image_rect)
        if not player.alive():
            text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 380, S.SCREEN_HEIGHT / 2 + 100), self.large_font, f"You have died. Press R to restart.", self.text_color)
            self.text_lines.append(text_image_rect)

    def ready_screen(self, level):
        self.text_lines = []
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 100, S.SCREEN_HEIGHT / 2 - 50), self.large_font, f"SPACE FROG!", (0, 255, 0))
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 15, S.SCREEN_HEIGHT / 2 + 50), self.font, f"{level.title}", (0, 255, 0))
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 75, S.SCREEN_HEIGHT / 2 + 75), self.font, f"Press any key to begin", (0, +255, 0))
        self.text_lines.append(text_image_rect)
        self.screen.fill((0, 0, 0))
        if level.title == "Level 1":
            self.screen.blit(self.sheet.get_image(0, 0)[0], (S.SCREEN_WIDTH / 2 - 100, S.SCREEN_HEIGHT / 2 - 125))
        else:
            self.screen.blit(self.sheet.get_image(1, 0)[0], (S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 2 - 150))
        self.show_info()

    def end_screen(self):
        self.text_lines = []
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 100, S.SCREEN_HEIGHT / 2 - 50), self.large_font, f"SPACE FROG!", (0, 255, 0))
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 100, S.SCREEN_HEIGHT / 2 + 50), self.font, f"Congratulations! You have won!", (0, 255, 0))
        self.text_lines.append(text_image_rect)
        text_image_rect = self.prepare_multiline((S.SCREEN_WIDTH / 2 - 70, S.SCREEN_HEIGHT / 2 + 75), self.font, f"Press any key to exit", (0, +255, 0))
        self.text_lines.append(text_image_rect)
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.sheet.get_image(0, 0)[0], (S.SCREEN_WIDTH / 2 - 100, S.SCREEN_HEIGHT / 2 - 125))
        self.screen.blit(pygame.transform.flip(self.sheet.get_image(0, 0)[0], True, False), (S.SCREEN_WIDTH / 2 + 100, S.SCREEN_HEIGHT / 2 + 75))
        self.screen.blit(self.sheet.get_image(1, 0)[0], (S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 2 - 150))
        self.show_info()


    def prepare_multiline(self, location, font, text, color):
        text_image_rect = pygame.freetype.Font.render(font, text , color)
        text_image_rect[1].left = self.screen_rect.left + location[0]
        text_image_rect[1].top = self.screen_rect.top + location[1]
        return text_image_rect


    def show_info(self):
        for line in self.text_lines:
            self.screen.blit(line[0], line[1])



