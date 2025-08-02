# balls/base_fighter.py
import pygame
import os
import math
import random
from config import ASSETS_DIR, ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT

class FightingBall:
    def __init__(self, x, y, radius, color, name, weapon_type="sword"):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.name = name
        self.weapon_type = weapon_type

        # Физические параметры - ЭНЕРГИЧНАЯ ФИЗИКА
        self.vx = random.uniform(-6, 6)
        self.vy = random.uniform(-4, 4)
        self.gravity = 0.2
        self.bounce_energy = 1.105
        self.friction = 0.998
        self.min_speed = 2
        self.max_speed = 20  # Ограничение максимальной скорости

        # Вращение шарика
        self.angle = 0
        self.angular_velocity = 0

        # ОРУЖИЕ КАК ЧАСТЬ ШАРИКА
        self.weapon_angle = 0
        self.weapon_rotation_speed = 2
        self.weapon_rotation_direction = 1

        # Параметры оружия
        self.weapon_length = 800
        self.weapon_width = 200
        self.weapon_color = (150, 150, 150) if weapon_type == "sword" else (139, 69, 19)

        self.max_health = 30
        self.health = self.max_health

        # Система неуязвимости и атак
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 20

        self.attack_cooldown = 0
        self.attack_cooldown_duration = 15

        # Характеристики для UI
        self.stats = {'damage': 1, 'range': 1, 'speed': 1, 'radius': self.radius}

    def take_damage(self, amount):
        if self.is_invulnerable:
            return False

        self.health -= amount
        if self.health < 0:
            self.health = 0

        self.is_invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration
        self.weapon_rotation_direction *= -1

        knockback_force = 3
        if hasattr(self, 'last_attacker_pos'):
            dx = self.rect.centerx - self.last_attacker_pos[0]
            dy = self.rect.centery - self.last_attacker_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > 0:
                self.vx += (dx / distance) * knockback_force
                self.vy += (dy / distance) * knockback_force - 1

        return True

    def can_attack(self):
        return self.attack_cooldown <= 0 and not self.is_invulnerable

    def attack(self, target):
        if not self.can_attack():
            return False

        target.last_attacker_pos = self.rect.center
        success = target.take_damage(self.stats['damage'])
        if success:
            self.attack_cooldown = self.attack_cooldown_duration
            self.on_successful_attack(target)
        return success

    def on_successful_attack(self, target):
        pass

    def parry(self):
        center_x = ARENA_X + ARENA_WIDTH / 2
        center_y = ARENA_Y + ARENA_HEIGHT / 2
        dx = self.rect.centerx - center_x
        dy = self.rect.centery - center_y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            bounce_force = 5
            self.vx += (dx / distance) * bounce_force
            self.vy += (dy / distance) * bounce_force - 2

    def update(self):
        if self.is_invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.weapon_angle += self.weapon_rotation_speed * self.weapon_rotation_direction
        if self.weapon_angle >= 360:
            self.weapon_angle -= 360
        elif self.weapon_angle < 0:
            self.weapon_angle += 360

        self.vy += self.gravity
        self.vx *= self.friction
        self.vy *= self.friction

        # Ограничение максимальной скорости
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            factor = self.max_speed / speed
            self.vx *= factor
            self.vy *= factor

        total_speed = math.sqrt(self.vx**2 + self.vy**2)
        self.angular_velocity = total_speed * 1.1
        if self.vx < 0:
            self.angular_velocity = -self.angular_velocity

        self.angle += self.angular_velocity
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left <= ARENA_X:
            self.rect.left = ARENA_X
            self.vx = -self.vx * self.bounce_energy

        if self.rect.right >= ARENA_X + ARENA_WIDTH:
            self.rect.right = ARENA_X + ARENA_WIDTH
            self.vx = -self.vx * self.bounce_energy

        if self.rect.top <= ARENA_Y:
            self.rect.top = ARENA_Y
            self.vy = -self.vy * self.bounce_energy

        if self.rect.bottom >= ARENA_Y + ARENA_HEIGHT:
            self.rect.bottom = ARENA_Y + ARENA_HEIGHT
            self.vy = -self.vy * self.bounce_energy * 1.03

        total_speed = math.sqrt(self.vx**2 + self.vy**2)
        if total_speed < self.min_speed:
            factor = self.min_speed / total_speed
            self.vx *= factor * 1.05
            self.vy *= factor * 1.05

    def get_weapon_line(self):
        center_x = self.rect.centerx
        center_y = self.rect.centery
        start_x = center_x + self.radius * math.sin(math.radians(self.weapon_angle))
        start_y = center_y - self.radius * math.cos(math.radians(self.weapon_angle))
        end_x = center_x + (self.radius + self.weapon_length) * math.sin(math.radians(self.weapon_angle))
        end_y = center_y - (self.radius + self.weapon_length) * math.cos(math.radians(self.weapon_angle))
        return (start_x, start_y), (end_x, end_y)

    def get_weapon_rect(self):
        start_pos, end_pos = self.get_weapon_line()
        min_x = min(start_pos[0], end_pos[0]) - self.weapon_width // 2
        max_x = max(start_pos[0], end_pos[0]) + self.weapon_width // 2
        min_y = min(start_pos[1], end_pos[1]) - self.weapon_width // 2
        max_y = max(start_pos[1], end_pos[1]) + self.weapon_width // 2
        return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def draw_weapon(self, screen):
        start_pos, end_pos = self.get_weapon_line()
        width = int(self.weapon_width)

        if self.weapon_type == "sword":
            pygame.draw.line(screen, self.weapon_color, start_pos, end_pos, width)
            handle_start = start_pos
            handle_length = 15
            handle_x = start_pos[0] - handle_length * math.sin(math.radians(self.weapon_angle))
            handle_y = start_pos[1] + handle_length * math.cos(math.radians(self.weapon_angle))
            pygame.draw.line(screen, (101, 67, 33), handle_start, (handle_x, handle_y), max(1, width - 2))

        elif self.weapon_type == "spear":
            pygame.draw.line(screen, self.weapon_color, start_pos, end_pos, max(1, width - 2))
            tip_length = 20
            tip_x = end_pos[0] + tip_length * math.sin(math.radians(self.weapon_angle))
            tip_y = end_pos[1] - tip_length * math.cos(math.radians(self.weapon_angle))
            left_x = end_pos[0] + 8 * math.sin(math.radians(self.weapon_angle + 90))
            left_y = end_pos[1] - 8 * math.cos(math.radians(self.weapon_angle + 90))
            right_x = end_pos[0] + 8 * math.sin(math.radians(self.weapon_angle - 90))
            right_y = end_pos[1] - 8 * math.cos(math.radians(self.weapon_angle - 90))
            pygame.draw.polygon(screen, (192, 192, 192), [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])

    def draw(self, screen):
        ball_color = self.color
        if self.is_invulnerable and (self.invulnerable_timer // 3) % 2:
            ball_color = tuple(min(255, c + 50) for c in self.color)

        self.draw_weapon(screen)
        pygame.draw.circle(screen, ball_color, self.rect.center, self.radius)

        if self.health > 0:
            health_text = f"{int(self.health)}"
            font = pygame.font.Font(None, 24)
            text_surface = font.render(health_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
