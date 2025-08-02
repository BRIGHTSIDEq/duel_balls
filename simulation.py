# simulation.py
import pygame
from config import *

class GameState:
    def __init__(self, ball1, ball2):
        self.ball1 = ball1
        self.ball2 = ball2
        self.balls = [self.ball1, self.ball2]
        self.winner = None
        self.parry_effect_timer = 0
        self.hit_events = []  # Для записи звуков ударов
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        
        if self.winner:
            return

        # Обновляем физику шаров
        for ball in self.balls:
            ball.update()

        # Проверка столкновений только если нет эффекта парирования
        if self.parry_effect_timer <= 0:
            weapon1_rect = self.ball1.get_weapon_rect()
            weapon2_rect = self.ball2.get_weapon_rect()
            
            # 1. Парирование (оружие против оружия) - приоритет!
            if weapon1_rect.colliderect(weapon2_rect):
                self.ball1.parry()
                self.ball2.parry()
                self.parry_effect_timer = 20 # Эффект парирования
                self.hit_events.append(self.frame_count)
                return # Прерываем проверку ударов

            # 2. Удары (оружие против шара) - только если можем атаковать
            if weapon1_rect.colliderect(self.ball2.rect):
                if self.ball1.attack(self.ball2):
                    self.hit_events.append(self.frame_count)
            
            if weapon2_rect.colliderect(self.ball1.rect):
                if self.ball2.attack(self.ball1):
                    self.hit_events.append(self.frame_count)

        # Уменьшаем таймер эффекта парирования
        if self.parry_effect_timer > 0:
            self.parry_effect_timer -= 1
            
        # Проверка победителя
        if self.ball1.health <= 0:
            self.winner = self.ball2.name
        elif self.ball2.health <= 0:
            self.winner = self.ball1.name