class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteorsImg)
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.size = random.randint(40, 50)
        # self.rect.width = self.size
        # self.rect.height = self.size

        self.radius = self.rect.width // 2
        # pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedY = random.randrange(1, 8)
        self.speedX = random.randrange(-3, 3)
        self.rot = 0
        self.rotSpeed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
        self.health = (self.radius**2) / 8
        self.max_helth = self.health

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rotSpeed) % 360
            self.new_image = pygame.transform.rotate(self.image_orig, self.rot)
            self.old_center = self.rect.center
            self.image = self.new_image
            self.rect = self.image.get_rect()
            self.rect.center = self.old_center

    def update(self, player):
        self.rotate()
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        if self.rect.top > HEIGHT + 10:
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 8)

        if self.health <= self.max_helth // 2:
            # self.image.set_opacity(50)
            pass
