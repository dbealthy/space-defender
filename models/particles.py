import random

import pygame as pg

from constants import *


class Particle:
    def __init__(self, origin, acc, colour):
        self.origin = origin
        self.colour = colour
        self.position = pg.Vector2(self.origin)
        self.velocity = pg.Vector2()
        self.acceleration = pg.Vector2(acc)

        self.radius = random.randint(1, 4)
        self.surface = pg.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.surface.get_rect()
        self.surface.set_colorkey(BLACK)
        self.life_time = 255
        self.live_speed = self.life_time / HEIGHT * self.radius

    def update(self):
        self.velocity += self.acceleration * self.radius
        self.position += self.velocity

        self.life_time -= self.live_speed

    def draw(self, surf):
        self.surface.set_alpha(self.life_time)
        surf.blit(self.surface, (int(self.position.x), int(self.position.y)))
        pg.draw.circle(
            self.surface,
            self.colour,
            (int(self.rect.center[0]), int(self.rect.center[1])),
            self.radius,
        )


class ParticleSystem:
    def __init__(self):
        # self.origin = origin
        self.all_particles = []
        self.quntity = 0
        self.colours = (CYAN, GOLD, WHITE, PALERED, DARKGREEN)

    def spawn(self, quntity):
        for i in range(quntity):
            rand_x = random.randrange(0, WIDTH)
            particle_origin = (rand_x, -25)
            acceleration = (0, random.uniform(0.001, 0.02))
            colour = random.choice(self.colours)
            p = Particle(particle_origin, acceleration, colour)
            self.all_particles.append(p)

    def update(self):
        for p in self.all_particles:
            p.update()

            if p.life_time <= 0:
                self.all_particles.remove(p)

    def draw(self, surf):
        for p in self.all_particles:
            p.draw(surf)
