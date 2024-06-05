class Powerup(pygame.sprite.Sprite):
    def __init__(self, type, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image = powerupImg[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = coords
        self.speed = 5

    def update(self, player):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
