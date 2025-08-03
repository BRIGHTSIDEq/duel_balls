import pygame
import math
import random
from config import *

class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.Surface((width, height))
        try:
            self.font_large = pygame.font.Font(FONT_PATH, 90)
            self.font_medium = pygame.font.Font(FONT_PATH, 50)
            self.font_small = pygame.font.Font(FONT_PATH, 32)
            self.font_tiny = pygame.font.Font(FONT_PATH, 24)
        except:
            # Если шрифт не найден, используем системный
            self.font_large = pygame.font.Font(None, 90)
            self.font_medium = pygame.font.Font(None, 50)
            self.font_small = pygame.font.Font(None, 32)
            self.font_tiny = pygame.font.Font(None, 24)

    def draw_text_with_shadow(self, text, font, color, x, y, center=True, shadow_offset=2):
        """Рисует текст с тенью для лучшей читаемости"""
        # Тень
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + shadow_offset, y + shadow_offset)
        else:
            shadow_rect.topleft = (x + shadow_offset, y + shadow_offset)
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Основной текст
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_gradient_background(self):
        """Рисует градиентный фон для лучшего вида"""
        for y in range(HEIGHT):
            color_ratio = y / HEIGHT
            r = int(243 * (1 - color_ratio) + 200 * color_ratio)
            g = int(229 * (1 - color_ratio) + 220 * color_ratio)
            b = int(171 * (1 - color_ratio) + 180 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def draw_spark_parry_effect(self, game_state):
        """НОВЫЙ эффект парирования - искры как при столкновении металла"""
        if game_state.parry_effect_timer <= 0:
            return
            
        # Центр между шариками для искр
        center_x = (game_state.ball1.rect.centerx + game_state.ball2.rect.centerx) // 2
        center_y = (game_state.ball1.rect.centery + game_state.ball2.rect.centery) // 2
        
        # Создаем искры вокруг точки столкновения
        for i in range(15):  # 15 искр
            # Случайное направление для каждой искры
            angle = random.uniform(0, 360)
            distance = random.uniform(10, 40)
            
            spark_x = center_x + distance * math.cos(math.radians(angle))
            spark_y = center_y + distance * math.sin(math.radians(angle))
            
            # Цвета искр - желтый, оранжевый, белый
            colors = [(255, 255, 100), (255, 200, 50), (255, 255, 255), (255, 150, 0)]
            spark_color = random.choice(colors)
            
            # Размер искры
            spark_size = random.randint(2, 5)
            
            # Рисуем искру
            pygame.draw.circle(self.screen, spark_color, (int(spark_x), int(spark_y)), spark_size)
            
            # Добавляем "хвостик" искры
            tail_x = spark_x - 8 * math.cos(math.radians(angle))
            tail_y = spark_y - 8 * math.sin(math.radians(angle))
            pygame.draw.line(self.screen, spark_color, (spark_x, spark_y), (tail_x, tail_y), 2)

    def draw_health_bar(self, ball, x, y, width, height, is_top=True):
        """Рисует стильную полоску здоровья с приятными цветами"""
        # Фон
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (60, 60, 60), bg_rect)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_rect, 3)

        # Полоска здоровья с более приятными цветами
        health_ratio = ball.health / ball.max_health
        fill_width = int(width * health_ratio)
        
        # Новые приятные цвета для здоровья
        if health_ratio > 0.6:
            health_color = (46, 204, 113)    # Мягкий зеленый
        elif health_ratio > 0.3:
            health_color = (230, 126, 34)    # Теплый оранжевый
        else:
            health_color = (231, 76, 60)     # Мягкий красный

        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, health_color, fill_rect)
        
        # Эффект блеска на полоске здоровья
        if fill_width > 10:
            shine_rect = pygame.Rect(x + 2, y + 2, fill_width - 4, height // 3)
            shine_color = tuple(min(255, c + 40) for c in health_color)
            pygame.draw.rect(self.screen, shine_color, shine_rect)

        # Имя и здоровье
        name_text = f"{ball.name}: {int(ball.health)}"
        text_color = WHITE if health_ratio > 0.3 else (255, 200, 200)
        self.draw_text_with_shadow(name_text, self.font_small, text_color, 
                                   x + width // 2, y + height // 2, True, 1)

    def draw_arena_decorations(self):
        """Рисует декоративные элементы арены"""
        # Основная арена
        arena_rect = pygame.Rect(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
        
        # Градиентный фон арены
        for i in range(ARENA_HEIGHT):
            ratio = i / ARENA_HEIGHT
            r = int(230 + (245 - 230) * ratio)
            g = int(230 + (245 - 230) * ratio)
            b = int(230 + (245 - 230) * ratio)
            pygame.draw.line(self.screen, (r, g, b), 
                           (ARENA_X, ARENA_Y + i), (ARENA_X + ARENA_WIDTH, ARENA_Y + i))
        
        # Красивая рамка арены
        pygame.draw.rect(self.screen, (100, 100, 100), arena_rect, 8)
        pygame.draw.rect(self.screen, (150, 150, 150), arena_rect, 4)
        pygame.draw.rect(self.screen, BLACK, arena_rect, 2)
        
        # Угловые украшения
        corner_size = 20
        corners = [
            (ARENA_X, ARENA_Y),
            (ARENA_X + ARENA_WIDTH - corner_size, ARENA_Y),
            (ARENA_X, ARENA_Y + ARENA_HEIGHT - corner_size),
            (ARENA_X + ARENA_WIDTH - corner_size, ARENA_Y + ARENA_HEIGHT - corner_size)
        ]
        
        for corner_x, corner_y in corners:
            corner_rect = pygame.Rect(corner_x, corner_y, corner_size, corner_size)
            pygame.draw.rect(self.screen, GOLD, corner_rect)
            pygame.draw.rect(self.screen, BLACK, corner_rect, 2)

    def draw_combat_effects(self, game_state):
        """Рисует эффекты боя"""
        # Эффекты от ударов
        for ball in game_state.balls:
            if ball.is_invulnerable and ball.invulnerable_timer > 15:
                # Эффект защиты
                shield_radius = ball.radius + 15
                alpha = int(100 * (ball.invulnerable_timer / 25))
                shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(shield_surface, (100, 100, 255, alpha), 
                                 (shield_radius, shield_radius), shield_radius, 3)
                self.screen.blit(shield_surface, 
                               (ball.rect.centerx - shield_radius, ball.rect.centery - shield_radius))

            # Эффект атаки
            if ball.attack_cooldown > 10:
                intensity = ball.attack_cooldown / 20
                glow_radius = int(ball.radius + 10 * intensity)
                glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                glow_color = (*ball.color, int(80 * intensity))
                pygame.draw.circle(glow_surface, glow_color, 
                                 (glow_radius, glow_radius), glow_radius)
                self.screen.blit(glow_surface, 
                               (ball.rect.centerx - glow_radius, ball.rect.centery - glow_radius))

    def draw_stats_display(self, game_state):
        """Отображает статистики внизу"""
        ball1, ball2 = game_state.ball1, game_state.ball2
        
        # Урон
        damage_text1 = f"DMG: {int(ball1.stats['damage'])}"
        damage_text2 = f"DMG: {int(ball2.stats['damage'])}"
        
        self.draw_text_with_shadow(damage_text1, self.font_tiny, (255, 100, 150), 
                                   120, STATS_Y, True, 1)
        self.draw_text_with_shadow(damage_text2, self.font_tiny, (100, 200, 255), 
                                   WIDTH - 120, STATS_Y, True, 1)
        
        # Длина оружия
        length_text1 = f"LENGTH: {int(ball1.weapon_length)}"
        length_text2 = f"LENGTH: {int(ball2.weapon_length)}"
        
        self.draw_text_with_shadow(length_text1, self.font_tiny, (200, 150, 200), 
                                   120, STATS_Y + 35, True, 1)
        self.draw_text_with_shadow(length_text2, self.font_tiny, (150, 200, 200), 
                                   WIDTH - 120, STATS_Y + 35, True, 1)

    def draw(self, game_state):
        # Градиентный фон
        self.draw_gradient_background()

        # Заголовок
        title_text = "SWORD  VS  SPEAR"
        self.draw_text_with_shadow(title_text, self.font_medium, BLACK, 
                                   WIDTH // 2, TITLE_Y, True, 2)

        # Арена с декорациями
        self.draw_arena_decorations()

        # Эффекты боя
        self.draw_combat_effects(game_state)

        # Рисуем шары
        for ball in game_state.balls:
            ball.draw(self.screen)

        # НОВЫЙ эффект парирования - искры
        self.draw_spark_parry_effect(game_state)

        # Полоски здоровья
        health_bar_width = WIDTH - 100
        health_bar_height = 35
        
        # Верхняя полоска здоровья
        self.draw_health_bar(game_state.ball1, 50, HEALTH_BAR_TOP_Y, 
                           health_bar_width, health_bar_height, True)
        
        # Нижняя полоска здоровья
        self.draw_health_bar(game_state.ball2, 50, HEALTH_BAR_BOTTOM_Y, 
                           health_bar_width, health_bar_height, False)

        # Статистики внизу
        self.draw_stats_display(game_state)

        # Индикаторы состояний
        for ball in [game_state.ball1, game_state.ball2]:
            if ball.is_invulnerable:
                indicator_text = ""
                pulse = math.sin(game_state.frame_count * 0.3) * 0.5 + 0.5
                color_intensity = int(255 * pulse)
                self.draw_text_with_shadow(indicator_text, self.font_tiny, 
                                         (255, color_intensity, 0), 
                                         ball.rect.centerx, ball.rect.centery - 70, True, 1)

        # Экран победы с анимацией
        if game_state.winner:
            # Полупрозрачный оверлей
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            # Анимированный текст победы
            pulse = math.sin(game_state.frame_count * 0.2) * 0.3 + 0.7
            winner_size = int(90 * pulse)
            try:
                winner_font = pygame.font.Font(FONT_PATH, winner_size)
            except:
                winner_font = pygame.font.Font(None, winner_size)
            
            winner_text = f"{game_state.winner.upper()}"
            self.draw_text_with_shadow(winner_text, winner_font, GOLD, 
                                     WIDTH // 2, HEIGHT // 2 - 50, True, 3)
            
            victory_text = "WINS!"
            self.draw_text_with_shadow(victory_text, self.font_large, WHITE, 
                                     WIDTH // 2, HEIGHT // 2 + 50, True, 2)
            
            # Эффект конфетти
            for i in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = random.choice([(255, 215, 0), (255, 100, 100), (100, 255, 100), (100, 100, 255)])
                size = random.randint(3, 8)
                pygame.draw.circle(self.screen, color, (x, y), size)

        return self.screen