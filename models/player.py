class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.curent_gun = Weapon("Tep")
        self.image = playerImg
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 40
        self.mask = pygame.mask.from_surface(self.image)
        # pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, self.radius)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30
        self.last_shot = pygame.time.get_ticks()
        self.shield = 100
        self.xSpeed = 10
        self.first_shot = True
        self.lives = 3
        self.hidden = False
        self.hide_time = pygame.time.get_ticks()

    def move_left(self):
        self.rect.x -= self.xSpeed

    def move_right(self):
        self.rect.x += self.xSpeed

    def change_gun(self, gun):
        self.curent_gun = Weapon(gun)

    def fire(self):
        bullet = self.curent_gun.get_bullet(self.rect.centerx, self.rect.top)
        # print('pew')
        # print(bullet)

    def hide(self):
        self.hide_time = pygame.time.get_ticks()
        self.hidden = True
        self.rect.center = (WIDTH // 2, HEIGHT + 200)

    def update(self, player):
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 3000:
            self.hidden = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 30
