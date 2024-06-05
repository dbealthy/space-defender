import math
import os
import random

import pygame

from options import *
from particles import ParticleSystem
from sprite_loader import SpriteSheet
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


# initialization pygame sounds and creat a windows
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

score = 0


# Sprites container
space_bg = ParticleSystem()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "assets/sprites")
snd_folder = os.path.join(os.path.dirname(__file__), "assets/sounds")


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
explosion_playerImg = pygame.image.load(os.path.join(img_folder, "explosion 4.png"))
explosionImg = spritesheet = pygame.image.load(os.path.join(img_folder, "booms.png"))
life_img = pygame.image.load(os.path.join(img_folder, "hit2.png"))

for img in meteor_list:
    meteorsImg.append(pygame.image.load(os.path.join(img_folder, img)).convert())


shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laser_Shoot.wav"))
shoot_sound.set_volume(0.05)

explosion_sound = pygame.mixer.Sound(os.path.join(snd_folder, "explosion.wav"))
explosion_sound.set_volume(0.1)

laserExpl_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laserExpl.wav"))
laserExpl_sound.set_volume(0.1)

pygame.mixer.music.load(os.path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.05)


shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laser_Shoot.wav"))
shoot_sound.set_volume(0.05)

explosion_sound = pygame.mixer.Sound(os.path.join(snd_folder, "explosion.wav"))
explosion_sound.set_volume(0.1)

laserExpl_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laserExpl.wav"))
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
