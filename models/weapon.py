class Weapon:
    def __init__(self, type):
        self.type = type
        self.damage = WEAP[self.type]["DAMAGE"]
        self.duration = WEAP[self.type]["DURATION"]
        self.quantity = WEAP[self.type]["QUANTITY"]
        self.range = WEAP[self.type]["RANGE"]
        self.cooldown = WEAP[self.type]["COOLDOWN"]
        self.last_shot = pygame.time.get_ticks()

    def get_bullet(self, *args):
        now = pygame.time.get_ticks()
        if self.type == "Tep" and now - self.last_shot > self.cooldown:
            self.last_shot = now
            bul = Bullet(*args)
            all_sprites.add(bul)
            bullets.add(bul)
            return bul

        elif self.type == "Buckshot" and now - self.last_shot > self.cooldown:
            self.last_shot = now
            for buck in range(self.quantity):
                position_x = random.randrange(
                    args[0] - self.range, args[0] + self.range
                )
                position_y = random.randrange(
                    args[1] - WEAP["Buckshot"]["BETWEEN_Y"], args[1]
                )
                angle_between_x = random.randrange(-7, 7)
                bul = BuckShot(position_x, position_y, angle_between_x)
                all_sprites.add(bul)
                bullets.add(bul)
            return bul

        elif self.type == "Laser" and now - self.last_shot > self.cooldown:
            self.last_shot = now
            bul = Laser(*args)
            all_sprites.add(bul)
            laserG.add(bul)
            return bul
