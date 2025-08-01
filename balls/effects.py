# balls/effects.py

import pygame
import math

class HitEffect:
    def __init__(self, pos, max_radius=50, duration=15, color=(255, 220, 120)):
        self.pos = pos
        self.max_radius = max_radius
        self.duration = duration
        self.age = 0
        self.color = color

    def update(self):
        self.age += 1

    def draw(self, screen):
        if self.age >= self.duration:
            return
        progress = self.age / self.duration
        radius = int(self.max_radius * progress)
        alpha = int(255 * (1 - progress))

        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface,
            (*self.color, alpha),
            (radius, radius),
            radius
        )
        screen.blit(surface, (self.pos[0] - radius, self.pos[1] - radius))

    def is_done(self):
        return self.age >= self.duration
