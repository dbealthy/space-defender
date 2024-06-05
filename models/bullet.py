class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.size = WEAP["Tep"]["SIZE"]
        self.velocity = WEAP["Tep"]["VELOCITY"]
        self.image = pygame.image.load(WEAP["Tep"]["IMAGE"])
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self, player):
        self.rect.bottom -= self.velocity
        if self.rect.bottom < 0:
            self.kill()


class BuckShot(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.size = WEAP["Buckshot"]["SIZE"]
        self.velocity = random.randrange(
            WEAP["Buckshot"]["VELOCITY"], WEAP["Buckshot"]["VELOCITY"] + 15
        )
        self.angle_between = angle
        self.image = pygame.image.load(WEAP["Buckshot"]["IMAGE"])
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.quantity = WEAP["Buckshot"]["QUANTITY"]
        self.clons = 0
        self.range = WEAP["Buckshot"]["RANGE"]

    def update(self, player):
        self.rect.bottom -= self.velocity
        self.rect.x += self.angle_between
        if self.rect.bottom < 0:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.size = WEAP["Laser"]["SIZE"]
        self.velocity = WEAP["Laser"]["VELOCITY"]
        self.duration = WEAP["Laser"]["DURATION"]
        self.image = pygame.image.load(WEAP["Laser"]["IMAGE"])
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        self.start = pygame.time.get_ticks()

    def update(self, player):
        now = pygame.time.get_ticks()
        self.rect.centerx = player.rect.centerx
        if now - self.start > self.duration:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 50
        super().__init__(x, y)

    def update(self, player):
        self.rect.y += self.velocity
        if self.rect.top > HEIGHT:
            self.kill()
