import pygame

class SpriteSheet:
    def __init__(self, size, sprite_sheet_file):
        self.sprite_sheet = pygame.image.load(sprite_sheet_file).convert_alpha()
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.animation_count = self.sprite_sheet_rect.height // size
        self.frame_count = self.sprite_sheet_rect.width // size
        self.extract_animation_strips(size)

    def extract_animation_strips(self, size):
        self.animation_strips = []
        self.mask_strips = []
        for i in range(0, self.animation_count):
            image_list = []
            mask_list = []
            y = i * size
            for j in range(0, self.frame_count):
                x = j * size
                frame_image = pygame.Surface((size, size))
                frame_image.blit(self.sprite_sheet, (0, 0), (x, y, size, size))
                frame_image.set_colorkey((0, 0, 0))
                # self.image = pygame.transform.rotate(frame_image, -90)
                mask = pygame.mask.from_surface(frame_image)
                image_list.append(frame_image)
                mask_list.append(mask)
            self.animation_strips.append(image_list)
            self.mask_strips.append(mask_list)

    def get_image(self, strip_number, frame_number):
        return self.animation_strips[strip_number][frame_number], self.mask_strips[strip_number][frame_number]
    
    def get_strip(self, strip_number):
        return self.animation_strips[strip_number], self.mask_strips[strip_number]
    
    def loop_strip(self, strip_number):
        strip = self.animation_strips[strip_number]
        while True:
            for frame in strip:
                yield frame