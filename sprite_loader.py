import pygame


class SpriteSheet:
    def __init__(self, name, raws, columns):
        self.spritesheet = name
        self.size = self.spritesheet.get_rect()
        self.height = self.size.height
        self.width = self.size.width
        self.raws = raws
        self.columns = columns
        self.cellwidth = self.width / self.columns
        self.cellheight = self.height / self.raws

    def get_image(self, coords):
        (x, y, width, height) = coords
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def calcSame(self):  # if all sprites are the same width and height
        x = 0
        y = 0
        for i in range(self.raws):
            y = i * self.cellheight
            for j in range(self.columns):
                x = j * self.cellwidth
                yield (x, y, self.cellwidth, self.cellheight)
