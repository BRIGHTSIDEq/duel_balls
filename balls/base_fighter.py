# balls/base_fighter.py
import pygame
import os
import math
from config import ASSETS_DIR, ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT

class FightingBall:
    def __init__(self, x, y, radius, color, name, weapon_image_name):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.name = name
        
        self.vx = 0
        self.vy = 0
        self.max_speed = 10
        
        self.angle = 0  # Угол поворота в градусах
        self.angular_velocity = 2 # Скорость вращения
        
        self.max_health = 100
        self.health = self.max_health

        # Загрузка и настройка оружия
        self.original_weapon_image = pygame.image.load(os.path.join(ASSETS_DIR, weapon_image_name)).convert_alpha()
        self.weapon_image = self.original_weapon_image
        self.weapon_rect = self.weapon_image.get_rect()
        self.weapon_offset_y = -self.radius - 20 # Смещение оружия относительно центра шара

        self.is_stunned = False
        self.stun_timer = 0
        self.stun_duration = 15 # в кадрах (1/4 секунды при 60 FPS)
        
        # Характеристики для UI
        self.stats = {'damage': 1, 'range': 1, 'speed': 1}

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.is_stunned = True
        self.stun_timer = self.stun_duration

    def attack(self, target):
        # Эта функция будет переопределена в дочерних классах
        pass

    def parry(self):
        # Меняем направление вращения при парировании
        self.angular_velocity *= -1.1 # Немного ускоряем вращение
        self.vx *= -0.5 # Немного отскакиваем
        self.vy *= -0.5

    def update(self):
        if self.is_stunned:
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.is_stunned = False
            return # Не двигаемся и не вращаемся в стане

        # Движение
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Вращение
        self.angle = (self.angle + self.angular_velocity) % 360

        # Столкновение со стенами арены
        if self.rect.left < ARENA_X:
            self.rect.left = ARENA_X
            self.vx *= -1
        if self.rect.right > ARENA_X + ARENA_WIDTH:
            self.rect.right = ARENA_X + ARENA_WIDTH
            self.vx *= -1
        if self.rect.top < ARENA_Y:
            self.rect.top = ARENA_Y
            self.vy *= -1
        if self.rect.bottom > ARENA_Y + ARENA_HEIGHT:
            self.rect.bottom = ARENA_Y + ARENA_HEIGHT
            self.vy *= -1

    def draw(self, screen):
        # Рисуем шар
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
        if self.is_stunned: # Эффект стана
             s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
             pygame.draw.circle(s, (255, 255, 0, 90), (self.radius, self.radius), self.radius)
             screen.blit(s, self.rect.topleft)

        # Вращаем и рисуем оружие
        rotated_weapon = pygame.transform.rotate(self.weapon_image, self.angle)
        
        # Позиционирование оружия
        offset_x = self.weapon_offset_y * math.sin(math.radians(self.angle))
        offset_y = self.weapon_offset_y * math.cos(math.radians(self.angle))

        weapon_pos = (self.rect.centerx - rotated_weapon.get_width() / 2 + offset_x,
                      self.rect.centery - rotated_weapon.get_height() / 2 - offset_y)
        
        self.weapon_rect = rotated_weapon.get_rect(center=self.rect.center)
        self.weapon_rect.center = (weapon_pos[0] + rotated_weapon.get_width()/2, weapon_pos[1] + rotated_weapon.get_height()/2)

        screen.blit(rotated_weapon, weapon_pos)