class Explosion(pygame.sprite.Sprite):
    def __init__(self, img, center, size, raws, columns):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.newsprite = SpriteSheet(img, raws, columns)
        self.curentspritePos = self.newsprite.calcSame()
        self.image = self.newsprite.get_image(next(self.curentspritePos))
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.size * 4, self.size * 4))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.framerate = 0

    def update(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.framerate:
            self.last_update = now
            self.frame += 1
            try:
                center = self.rect.center
                self.image = self.newsprite.get_image(next(self.curentspritePos))
                self.image = pygame.transform.scale(
                    self.image, (self.size * 4, self.size * 4)
                )
                self.image.set_colorkey((0, 0, 0))
                self.rect = self.image.get_rect()
                self.rect.center = center

            except:
                self.kill()
