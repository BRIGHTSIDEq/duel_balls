from .base_ball import Ball
import pygame
import math
from config import HEIGHT

class Laserry(Ball):
    def __init__(self, x, y, direction, hit_sound=None):
        super().__init__(x, y, radius=20, color=(255, 0, 0), name="Laserry", direction=direction, hit_sound=hit_sound)
        self.damage = 1
        self.laser_damage = 0
        self.laser_cooldown = 5
        self.laser_timer = 0
        self.angle = 0  # угол в градусах
        self.rotation_speed = 5  # скорость вращения лазера (градусы за кадр)

    def update(self, platforms, game_state, frame_count):
        super().update(platforms, game_state, frame_count)

        self.laser_timer += 1
        if self.laser_timer >= self.laser_cooldown:
            self.laser_damage += 1
            self.laser_timer = 0

            rad_angle = math.radians(self.angle)
            laser_length = 200

            laser_end_x = self.rect.centerx + laser_length * math.cos(rad_angle)
            laser_end_y = self.rect.centery - laser_length * math.sin(rad_angle)

            for platform in platforms:
                if self.line_rect_collision((self.rect.centerx, self.rect.centery), (laser_end_x, laser_end_y), platform.rect):
                    platform.take_damage(self.laser_damage)
                    game_state.hit_events.append(frame_count)

        self.angle = (self.angle + self.rotation_speed) % 360

    def draw(self, screen):
        super().draw(screen)

        rad_angle = math.radians(self.angle)
        laser_length = 200
        start_pos = self.rect.center
        end_pos = (
            int(self.rect.centerx + laser_length * math.cos(rad_angle)),
            int(self.rect.centery - laser_length * math.sin(rad_angle))
        )
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 3)

    def line_rect_collision(self, p1, p2, rect):
        return rect.clipline(p1, p2)
