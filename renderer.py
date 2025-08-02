# renderer.py
import pygame
from config import *

class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.Surface((width, height))
        try:
            self.font_large = pygame.font.Font(FONT_PATH, 80)
            self.font_medium = pygame.font.Font(FONT_PATH, 60)
            self.font_small = pygame.font.Font(FONT_PATH, 30)
        except:
            # Если шрифт не найден, используем системный
            self.font_large = pygame.font.Font(None, 80)
            self.font_medium = pygame.font.Font(None, 60)
            self.font_small = pygame.font.Font(None, 30)

    def draw_text(self, text, font, color, x, y, center=True):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def draw_stats_bar(self, label, value, max_value, x, y, width, height, color):
        # Рисуем фон полоски
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
        
        # Рисуем саму полоску
        fill_width = min(width, (value / max_value) * width)
        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, color, fill_rect)

        # Рисуем рамку
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
        # Рисуем текст
        stat_text = f"{label}: {value:.1f}"
        self.draw_text(stat_text, self.font_small, WHITE, x + width / 2, y + height / 2)

    def draw_physics_info(self, ball, x, y):
        """Отображает физическую информацию о шарике"""
        speed = (ball.vx**2 + ball.vy**2)**0.5
        self.draw_text(f"Speed: {speed:.1f}", self.font_small, WHITE, x, y, False)
        self.draw_text(f"Angle: {ball.angle:.0f}°", self.font_small, WHITE, x, y + 25, False)

    def draw(self, game_state):
        # Фон
        self.screen.fill(VANILLA)

        # Арена
        arena_rect = pygame.Rect(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
        pygame.draw.rect(self.screen, GREY, arena_rect)
        pygame.draw.rect(self.screen, BLACK, arena_rect, 5)

        # Интерфейс как на скриншоте
        title_text = f"Sword  VS  Spear"
        self.draw_text(title_text, self.font_medium, BLACK, WIDTH / 2, ARENA_PADDING_Y / 2)

        # Рисуем шары
        for ball in game_state.balls:
            ball.draw(self.screen)

        # Эффект парирования
        if game_state.parry_effect_timer > 0:
            intensity = game_state.parry_effect_timer / 20
            
            # Центральная вспышка
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(150 * intensity)
            flash_surface.fill((255, 255, 200, alpha))
            self.screen.blit(flash_surface, (0, 0))
            
            # Волны от центра
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            for i in range(3):
                radius = int(100 * (1 - intensity) + i * 50)
                wave_alpha = int(100 * intensity)
                wave_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(wave_surface, (255, 255, 255, wave_alpha), (radius, radius), radius, 5)
                self.screen.blit(wave_surface, (center_x - radius, center_y - radius))

        # Полоски здоровья
        # Ball 1 (сверху)
        hp1_rect = pygame.Rect(50, 50, WIDTH - 100, 25)
        pygame.draw.rect(self.screen, (100, 0, 0), hp1_rect)
        hp1_fill = (game_state.ball1.health / game_state.ball1.max_health) * hp1_rect.width
        
        health_color = (0, 255, 0) if game_state.ball1.health > 50 else (255, 255, 0) if game_state.ball1.health > 25 else (255, 0, 0)
        pygame.draw.rect(self.screen, health_color, (hp1_rect.x, hp1_rect.y, hp1_fill, hp1_rect.height))
        pygame.draw.rect(self.screen, BLACK, hp1_rect, 3)
        
        self.draw_text(f"{game_state.ball1.name}: {int(game_state.ball1.health)}", 
                      self.font_small, WHITE, hp1_rect.centerx, hp1_rect.centery)
        
        # Ball 2 (снизу)
        hp2_rect = pygame.Rect(50, HEIGHT - 75, WIDTH - 100, 25)
        pygame.draw.rect(self.screen, (100, 0, 0), hp2_rect)
        hp2_fill = (game_state.ball2.health / game_state.ball2.max_health) * hp2_rect.width
        
        health_color = (0, 255, 0) if game_state.ball2.health > 50 else (255, 255, 0) if game_state.ball2.health > 25 else (255, 0, 0)
        pygame.draw.rect(self.screen, health_color, (hp2_rect.x, hp2_rect.y, hp2_fill, hp2_rect.height))
        pygame.draw.rect(self.screen, BLACK, hp2_rect, 3)
        
        self.draw_text(f"{game_state.ball2.name}: {int(game_state.ball2.health)}", 
                      self.font_small, WHITE, hp2_rect.centerx, hp2_rect.centery)

        # НЕ рисуем полоски характеристик пока - сосредотачиваемся на главном
        # stat_y_start = HEIGHT - 180
        # stats1 = game_state.ball1.stats
        # self.draw_stats_bar("Damage", stats1['damage'], 50, 50, stat_y_start, 150, 25, RED)
        
        # Простой счетчик внизу как на скриншоте
        self.draw_text(f"Poisons: 0", self.font_small, (128, 0, 128), 100, HEIGHT - 50)
        self.draw_text(f"Range/Damage: 1", self.font_small, (0, 255, 255), WIDTH - 150, HEIGHT - 50)

        # Показываем физическую информацию
        # self.draw_physics_info(game_state.ball1, 10, 100)
        # self.draw_physics_info(game_state.ball2, 10, 150)

        # Индикаторы состояний
        if game_state.ball1.is_invulnerable:
            self.draw_text("INVULNERABLE", self.font_small, (255, 255, 0), 
                          game_state.ball1.rect.centerx, game_state.ball1.rect.centery - 60)
        
        if game_state.ball2.is_invulnerable:
            self.draw_text("INVULNERABLE", self.font_small, (255, 255, 0), 
                          game_state.ball2.rect.centerx, game_state.ball2.rect.centery - 60)

        # Экран победы
        if game_state.winner:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            winner_text = f"{game_state.winner.upper()} WINS!"
            self.draw_text(winner_text, self.font_large, GOLD, WIDTH / 2, HEIGHT / 2)
            
            self.draw_text("PHYSICS VICTORY!", self.font_medium, WHITE, WIDTH / 2, HEIGHT / 2 + 100)

        return self.screen