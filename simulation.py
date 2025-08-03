# simulation.py
import pygame
import math
import random
from config import *

class GameState:
    def __init__(self, ball1, ball2):
        self.ball1 = ball1
        self.ball2 = ball2
        self.balls = [self.ball1, self.ball2]
        self.winner = None
        self.parry_effect_timer = 0
        self.hit_events = []
        self.frame_count = 0
        
        # Система предотвращения застреваний
        self.separation_force = 2.0
        self.last_positions = {}
        self.stuck_timer = {}
        
        for ball in self.balls:
            self.last_positions[ball] = ball.rect.center
            self.stuck_timer[ball] = 0

    def check_balls_stuck(self):
        """Проверяет, не застряли ли шарики, и разделяет их"""
        for ball in self.balls:
            current_pos = ball.rect.center
            last_pos = self.last_positions[ball]
            
            # Если шарик почти не двигается
            distance_moved = math.sqrt((current_pos[0] - last_pos[0])**2 + 
                                     (current_pos[1] - last_pos[1])**2)
            
            if distance_moved < 1:
                self.stuck_timer[ball] += 1
            else:
                self.stuck_timer[ball] = 0
            
            # Если застрял больше 30 кадров - добавляем импульс
            if self.stuck_timer[ball] > 30:
                ball.vx += random.uniform(-3, 3)
                ball.vy += random.uniform(-3, 3)
                self.stuck_timer[ball] = 0
            
            self.last_positions[ball] = current_pos

    def force_separate_balls(self):
        """Принудительно разделяет шарики если они слишком близко"""
        dx = self.ball2.rect.centerx - self.ball1.rect.centerx
        dy = self.ball2.rect.centery - self.ball1.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        min_distance = self.ball1.radius + self.ball2.radius + 5
        
        if distance < min_distance and distance > 0:
            # Нормализованный вектор разделения
            nx = dx / distance
            ny = dy / distance
            
            # Требуемое расстояние для разделения
            separation_needed = min_distance - distance
            separation_per_ball = separation_needed / 2
            
            # Раздвигаем шарики
            self.ball1.rect.centerx -= nx * separation_per_ball
            self.ball1.rect.centery -= ny * separation_per_ball
            self.ball2.rect.centerx += nx * separation_per_ball
            self.ball2.rect.centery += ny * separation_per_ball
            
            # Добавляем силу отталкивания
            push_force = 3
            self.ball1.vx -= nx * push_force
            self.ball1.vy -= ny * push_force
            self.ball2.vx += nx * push_force
            self.ball2.vy += ny * push_force

    def enhanced_collision_detection(self):
        """Улучшенная система столкновений"""
        if self.parry_effect_timer > 0:
            return
            
        weapon1_rect = self.ball1.get_weapon_rect()
        weapon2_rect = self.ball2.get_weapon_rect()
        
        # 1. ПАРИРОВАНИЕ - наивысший приоритет
        if weapon1_rect.colliderect(weapon2_rect):
            self.trigger_parry()
            return
        
        # 2. УДАРЫ - только если можем атаковать
        hit_occurred = False
        
        # Проверяем удар первого шарика
        if weapon1_rect.colliderect(self.ball2.rect) and self.ball1.can_attack():
            if self.ball1.attack(self.ball2):
                self.hit_events.append(self.frame_count)
                hit_occurred = True
        
        # Проверяем удар второго шарика
        if weapon2_rect.colliderect(self.ball1.rect) and self.ball2.can_attack():
            if self.ball2.attack(self.ball1):
                self.hit_events.append(self.frame_count)
                hit_occurred = True

    def trigger_parry(self):
        """Запускает УЛУЧШЕННЫЙ эффект парирования - всего 1 кадр микро-стан"""
        self.ball1.parry()
        self.ball2.parry()
        self.parry_effect_timer = 1  # Только 1 кадр!
        self.hit_events.append(self.frame_count)

    def keep_balls_in_arena(self):
        """Гарантирует, что шарики остаются в арене"""
        for ball in self.balls:
            margin = 5
            
            if ball.rect.left < ARENA_X + margin:
                ball.rect.left = ARENA_X + margin
                ball.vx = abs(ball.vx) * ball.bounce_energy
                
            if ball.rect.right > ARENA_X + ARENA_WIDTH - margin:
                ball.rect.right = ARENA_X + ARENA_WIDTH - margin
                ball.vx = -abs(ball.vx) * ball.bounce_energy
                
            if ball.rect.top < ARENA_Y + margin:
                ball.rect.top = ARENA_Y + margin
                ball.vy = abs(ball.vy) * ball.bounce_energy
                
            if ball.rect.bottom > ARENA_Y + ARENA_HEIGHT - margin:
                ball.rect.bottom = ARENA_Y + ARENA_HEIGHT - margin
                ball.vy = -abs(ball.vy) * ball.bounce_energy

    def add_random_energy(self):
        """Добавляет случайную энергию для поддержания динамики"""
        if self.frame_count % 180 == 0:  # Каждые 3 секунды
            for ball in self.balls:
                total_speed = math.sqrt(ball.vx**2 + ball.vy**2)
                if total_speed < 3:  # Если движется слишком медленно
                    ball.vx += random.uniform(-2, 2)
                    ball.vy += random.uniform(-2, 2)

    def update(self):
        self.frame_count += 1
        
        if self.winner:
            return

        # Обновляем физику шаров с взаимодействием
        self.ball1.update(self.ball2)
        self.ball2.update(self.ball1)

        # Предотвращаем застревания
        self.check_balls_stuck()
        
        # Принудительно разделяем если слишком близко
        self.force_separate_balls()
        
        # Улучшенная система столкновений
        self.enhanced_collision_detection()

        # Гарантируем, что шарики остаются в арене
        self.keep_balls_in_arena()
        
        # Добавляем случайную энергию при необходимости
        self.add_random_energy()

        # Уменьшаем таймер эффекта парирования
        if self.parry_effect_timer > 0:
            self.parry_effect_timer -= 1
            
        # Проверка победителя
        if self.ball1.health <= 0:
            self.winner = self.ball2.name
        elif self.ball2.health <= 0:
            self.winner = self.ball1.name