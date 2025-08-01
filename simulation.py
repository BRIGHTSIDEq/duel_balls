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

    def update(self):
        if self.winner:
            return

        for ball in self.balls:
            ball.update()

        # Проверка столкновений
        # 1. Парирование (оружие против оружия)
        if self.ball1.weapon_rect.colliderect(self.ball2.weapon_rect):
            self.ball1.parry()
            self.ball2.parry()
            self.parry_effect_timer = 5 # Показываем эффект 5 кадров
            return # В этот кадр ударов не происходит

        # 2. Удар (оружие против шара)
        if self.ball1.weapon_rect.colliderect(self.ball2.rect):
            self.ball1.attack(self.ball2)
        
        if self.ball2.weapon_rect.colliderect(self.ball1.rect):
            self.ball2.attack(self.ball1)

        # Уменьшаем таймер эффекта парирования
        if self.parry_effect_timer > 0:
            self.parry_effect_timer -= 1
            
        # Проверка победителя
        if self.ball1.health <= 0:
            self.winner = self.ball2.name
        elif self.ball2.health <= 0:
            self.winner = self.ball1.name