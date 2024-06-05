# pygame template
import math
import os
import random

import pygame

from options import *
from Space import ParticleSystem
from spriteProc import SpriteSheet
from weapon import WEAPONS as PWS
from weapon import WEAPONS as WEAP


def printLabel(
    surface, text, x, y, fontSize=36, fontName="monospace", colour=(255, 255, 255)
):
    font = pygame.font.SysFont(fontName, fontSize)
    text_geometry = font.render(str(text), True, colour)
    text_rect = text_geometry.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_geometry, text_rect)


def spawn_mob(quantity):
    mob_list = []
    for mob in range(quantity):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        mob_list.append(m)
    return mob_list


def drawShield(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 300
    BAR_HEIGHT = 12
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(int(x), int(y), BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(int(x), int(y), int(fill), BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 150, 255), fill_rect)
    pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2)


def show_fps(screen, clock):
    font = pygame.font.SysFont("monospace", 42)
    fps_overlay = font.render(str(round(clock.get_fps())), True, (255, 255, 255))
    screen.blit(fps_overlay, (0, 0))


def draw_lives(surf, lives, x, y, img):
    for life in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * life
        img_rect.y = y
        surf.blit(img, img_rect)


def randomly(function, chance, *args):
    randomNumber = random.randrange(chance)
    # print(randomNumber, '\t', chance)
    if randomNumber == random.randrange(chance):
        function(*args)


def spawnPowerup(type, coords):
    powerup = Powerup(type, coords)
    all_sprites.add(powerup)
    powerups.add(powerup)


def spawn_enemy(quantity, type="Ranger"):
    enemies_list = []
    for e in range(quantity):
        enemy = Ranger(
            (random.randrange(WIDTH), random.randrange(100)), 5, (150, 150), 350
        )
        all_sprites.add(enemy)
        enemies.add(enemy)
        enemies_list.append(enemy)
    return enemies_list


def resize(picture, **kwargs):
    rect = picture.get_rect()
    scale = 1
    width = rect.width
    height = rect.height
    for key, value in kwargs.items():
        if key == "width":
            width = value

        if key == "height":
            height = value

        if key == "scalex":
            scale = value

    width = rect.width // scale
    height = rect.height // scale
    image = pygame.transform.scale(picture, (width, height))
    return image


def show_menue():
    screen.blit(background, (0, 0))
    printLabel(
        screen, "GAME OVER", WIDTH // 2, HEIGHT // 3, fontSize=48, colour=(255, 0, 22)
    )
    printLabel(screen, "press a key to continue", WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameOver = True
                died = False
                waiting = False

            if event.type == pygame.KEYUP:
                waiting = False
                died = False


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


class EnemyMap:
    def __init__(self, max_enemies):
        self.max_enemies = max_enemies
        self.all_enemies = []

    def add_enemy(self, enemy):
        if len(self.all_enemies) < self.max_enemies:
            self.all_enemies.append(enemy)
            return True
        return False

    def remove_enemy(self, index_enemy):
        try:
            self.all_enemies.pop(index_enemy)
            return True
        except:
            return False

    def implement(self):
        if len(self.all_enemies) == 0:
            return False
        for enemy in self.all_enemies:
            all_sprites.add(enemy)
            enemies.add(enemy)


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
        self.image = pygame.image.load("img/enemy.png")
        self.image = pygame.transform.scale(self.image, self.size)  # size is a tuple
        self.rect = self.image.get_rect()
        self.view_range_img = pygame.image.load("img/view_range.png")
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


class EnemyBullet(Bullet):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 50
        super().__init__(x, y)

    def update(self, player):
        self.rect.y += self.velocity
        if self.rect.top > HEIGHT:
            self.kill()


# initialization pygame sounds and creat a windows
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

score = 0


# Sprites container
space_bg = ParticleSystem()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
snd_folder = os.path.join(os.path.dirname(__file__), "sounds")


background = pygame.image.load(os.path.join(img_folder, "space_2.jpg")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

playerImg = pygame.image.load(os.path.join(img_folder, "spaceShip.png"))
playerImg = pygame.transform.scale(playerImg, PLAYER_SIZE)

bulletImg = pygame.image.load(os.path.join(img_folder, "bullet.png"))
bulletImg = pygame.transform.scale(bulletImg, (55, 75))

meteor_list = ["meteor.png", "meteor2.png", "meteor3.png"]
meteorsImg = []


powerupImg = {}
for key in PWS.keys():
    img = pygame.image.load(PWS[key]["IMAGE"])
    img = pygame.transform.scale(img, (50, 50))
    powerupImg.update({key: img})

# powerupImg = [pygame.image.load('img/shield.png')]
# powerupImg = [resize(powerupImg[0], scalex=100), 'hit2.png']
explosion_playerImg = pygame.image.load("img/explosion 4.png")
explosionImg = spritesheet = pygame.image.load("img/booms.png")
life_img = pygame.image.load(os.path.join(img_folder, "hit2.png"))

for img in meteor_list:
    meteorsImg.append(pygame.image.load(os.path.join(img_folder, img)).convert())


shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laser_Shoot.wav"))
shoot_sound.set_volume(0.05)

explosion_sound = pygame.mixer.Sound(os.path.join(snd_folder, "explosion.wav"))
explosion_sound.set_volume(0.1)

laserExpl_sound = pygame.mixer.Sound("sounds/laserExpl.wav")
laserExpl_sound.set_volume(0.1)

pygame.mixer.music.load(os.path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.05)


shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laser_Shoot.wav"))
shoot_sound.set_volume(0.05)

explosion_sound = pygame.mixer.Sound(os.path.join(snd_folder, "explosion.wav"))
explosion_sound.set_volume(0.1)

laserExpl_sound = pygame.mixer.Sound("sounds/laserExpl.wav")
laserExpl_sound.set_volume(0.1)

pygame.mixer.music.load(os.path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(loops=-1)


last_check = pygame.time.get_ticks()


GameOver = False
died = True

# Main loop
while not GameOver:
    # fps

    if died:
        died = False
        show_menue()
        score = 0
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        enemyBullets = pygame.sprite.Group()
        laserG = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        mob = spawn_mob(5)
        spawn_enemy(2)

    clock.tick(FPS)
    # Process input (EVENTS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOver = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                player.change_gun("Tep")

            if event.key == pygame.K_x:
                player.change_gun("Buckshot")

            if event.key == pygame.K_z:
                player.change_gun("Laser")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player.rect.left > 0:
        player.move_left()

    if keys[pygame.K_d] and player.rect.right < WIDTH:
        player.move_right()

    if keys[pygame.K_SPACE] and not player.hidden:
        player.fire()

    # Update
    all_sprites.update(player)
    now = pygame.time.get_ticks()

    if now - last_check > STAR_RATE:
        last_check = now
        space_bg.spawn(STAR_QUT)
    space_bg.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)

    for hit in hits:
        hit.health -= player.curent_gun.damage
        if hit.health <= 0:
            expl = Explosion(explosionImg, hit.rect.center, hit.radius, 6, 8)
            all_sprites.add(expl)
            hit.kill()
            score += 60 - round((hit.radius * 0.6))
            mob = spawn_mob(1)
            explosion_sound.play()
            # spawn powerup randomly
            powerupImg_keys = list(powerupImg.keys())
            randomly(
                spawnPowerup, 10, random.choice(powerupImg_keys), hit.rect.center
            )  # second argument means 1/n for ex  5 mean one of five if power up

    # check if mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)

    for hit in hits:
        player.shield -= hit.radius
        expl = Explosion(explosionImg, hit.rect.center, hit.radius, 6, 8)
        all_sprites.add(expl)
        current_pos = player.rect.x
        mob = spawn_mob(1)
        if player.shield <= 0:
            expl = Explosion(
                explosion_playerImg, player.rect.center, player.rect.width, 8, 8
            )
            all_sprites.add(expl)
            player.hide()
            player.lives -= 1
            player.shield = 50

    if player.lives == 0 and not expl.alive():
        died = True

    hits = pygame.sprite.groupcollide(mobs, laserG, False, False)

    for hit in hits:

        distance = player.rect.top - hit.rect.bottom
        if distance <= 0:
            distance = 1

        damage = (
            player.curent_gun.damage / distance
        )  # make it to depend on time aimed at  gunDamage**time / distance
        hit.health -= damage
        if hit.health <= 0:
            expl = Explosion(explosionImg, hit.rect.center, hit.radius, 6, 8)
            laserExpl_sound.play()
            all_sprites.add(expl)
            powerupImg_keys = list(powerupImg.keys())
            randomly(spawnPowerup, 10, random.choice(powerupImg_keys), hit.rect.center)
            score += 60 - round((hit.radius * 0.6))
            mob = spawn_mob(1)
            hit.kill()

    poweruphit = pygame.sprite.spritecollide(
        player, powerups, True, pygame.sprite.collide_circle
    )

    for hit in poweruphit:
        powertype = hit.type
        if powertype == "Shieldup":
            player.shield += 25
            if player.shield > 100:
                player.shield = 100
        elif powertype == "Extralife":
            player.lives += 1
            if player.lives > 5:
                player.lives = 5

        elif powertype == "Doubleshot":
            pass

    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)

    for hit in hits:
        hit.health -= player.curent_gun.damage
        if hit.health <= 0:
            hit.kill()

    hits = pygame.sprite.spritecollide(
        player, enemyBullets, True, pygame.sprite.collide_circle
    )
    for hit in hits:
        player.shield -= hit.damage
        current_pos = player.rect.x
        if player.shield <= 0:
            expl = Explosion(
                explosion_playerImg, player.rect.center, player.rect.width, 8, 8
            )
            all_sprites.add(expl)
            player.hide()
            player.lives -= 1
            player.shield = 50

    if player.lives == 0 and not expl.alive():
        died = True

    # Draw / render
    screen.fill(DARKBLUE)
    space_bg.draw(screen)
    rand_x = random.randrange(0, WIDTH)
    all_sprites.draw(screen)
    printLabel(screen, score, WIDTH // 2, 20)
    drawShield(
        screen,
        (player.rect.right + player.rect.left) / 2 - 150,
        player.rect.bottom + 10,
        player.shield,
    )
    # drawShield(screen, (enemy.rect.right + enemy.rect.left)/2 - 150, enemy.rect.bottom + 10, enemy.health)
    show_fps(screen, clock)
    draw_lives(screen, player.lives, 100, 150, life_img)

    # after all
    pygame.display.flip()


pygame.quit()
