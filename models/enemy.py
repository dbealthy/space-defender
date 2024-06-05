class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, velocity, size, view_range_value):
        pygame.sprite.Sprite.__init__(self)
        self.position = position  # position is a tuple
        self.velocity = velocity
        self.size = size
        self.view_range_value = view_range_value


class Ranger(Enemy):
    def __init__(self, position, velocity, size, view_range_value):
        super().__init__(position, velocity, size, view_range_value)
        self.image = pygame.image.load(os.path.join(img_folder, "enemy.png"))
        self.image = pygame.transform.scale(self.image, self.size)  # size is a tuple
        self.rect = self.image.get_rect()
        self.view_range_img = pygame.image.load(
            os.path.join(img_folder, "view_range.png")
        )
        self.view_range_img = pygame.transform.scale(
            self.view_range_img, (self.view_range_value, player.rect.top)
        )
        self.view_range_mask = pygame.mask.from_surface(self.view_range_img)
        self.view_range_rect = self.view_range_img.get_rect()
        self.last_shot = pygame.time.get_ticks()
        self.rect.centerx = self.position[0]
        self.rect.y = self.position[1]

        self.health = 500
        self.damage = 35
        self.cooldown = 500

        self.attacking = False
        self.moving = True
        self.found_coords = ()
        self.finding_time = 500
        self.stop_moment = pygame.time.get_ticks()
        self.distance_above_player = 100
        self.changed_rect = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now
            ebul = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(ebul)
            enemyBullets.add(ebul)

    def towards_object(self, player_rect):
        c = math.sqrt(
            (player_rect.centerx - self.rect.centerx) ** 2
            + (player_rect.centery - self.distance_above_player - self.rect.centery)
            ** 2
        )
        try:
            x = (player_rect.centerx - self.rect.centerx) / c
            y = ((player_rect.y + self.distance_above_player) - self.rect.y) / c
        except ZeroDivisionError:
            return False
        print(x, y)
        return (x, y)

    def update(self, player):
        now = pygame.time.get_ticks()
        normolized_vec = self.towards_object(player.rect)
        if not player.hidden:
            if normolized_vec and self.moving:
                self.rect.centerx = int(
                    (self.rect.centerx + normolized_vec[0] * self.velocity)
                )

            # elif not self.moving:
            # 	take_above = self.towards_object(self.rect)
            # 	if take_above:
            # 		self.rect.centerx, self.rect.y = (int((self.rect.centerx + take_above[0] * self.velocity)), int((self.rect.y + take_above[1] * self.velocity)))

            if player.rect.x in range(
                self.rect.x - self.view_range_value, self.rect.x + self.view_range_value
            ):
                self.shoot()

                # collisions = self.find_local_collisions()
                # for collision in collisions:
                # 	collision.moving = False
                # 	if self.rect.y >= collision.rect.top:
                # 		self.moving = True

            # iterate

            # for idx, another in enumerate(enemies):
            # 	if enemies[another].rect.x in range(an_enemy.rect.x - 10, an_enemy.rect.x + an_enemy.rect.width + 10):

            "if this_enemy in range(another):"
            "self.moving = False"


class Rounder(Enemy):
    def shoot(self):
        pass


class Milish(Enemy):
    def shoot(self):
        pass
