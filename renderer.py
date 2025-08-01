# renderer.py
import pygame
from config import *

class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.Surface((width, height))
        self.font_large = pygame.font.Font(FONT_PATH, 80)
        self.font_medium = pygame.font.Font(FONT_PATH, 60)
        self.font_small = pygame.font.Font(FONT_PATH, 30)

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
        fill_width = (value / max_value) * width
        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, color, fill_rect)

        # Рисуем рамку
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
        # Рисуем текст
        stat_text = f"{label}: {value:.1f}"
        self.draw_text(stat_text, self.font_small, WHITE, x + width / 2, y + height / 2)


    def draw(self, game_state):
        # Фон
        self.screen.fill(VANILLA)

        # Арена
        arena_rect = pygame.Rect(ARENA_X, ARENA_Y, ARENA_WIDTH, ARENA_HEIGHT)
        pygame.draw.rect(self.screen, GREY, arena_rect)
        pygame.draw.rect(self.screen, BLACK, arena_rect, 5)

        # Заголовок
        title_text = f"{game_state.ball1.name} vs {game_state.ball2.name}"
        self.draw_text(title_text, self.font_medium, BLACK, WIDTH / 2, ARENA_PADDING_Y / 2)

        # Рисуем шары
        for ball in game_state.balls:
            ball.draw(self.screen)

        # Эффект парирования
        if game_state.parry_effect_timer > 0:
            # Белая вспышка на весь экран
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = 150 * (game_state.parry_effect_timer / 5) # Затухание
            s.fill((255, 255, 255, alpha))
            self.screen.blit(s, (0,0))
            # Микро-замирание экрана будет достигаться за счет паузы в main loop (опционально)

        # Полоски здоровья
        # Ball 1 (сверху)
        hp1_rect = pygame.Rect(50, 50, WIDTH - 100, 30)
        pygame.draw.rect(self.screen, RED, hp1_rect)
        hp1_fill = (game_state.ball1.health / game_state.ball1.max_health) * hp1_rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (hp1_rect.x, hp1_rect.y, hp1_fill, hp1_rect.height))
        
        # Ball 2 (снизу)
        hp2_rect = pygame.Rect(50, HEIGHT - 80, WIDTH - 100, 30)
        pygame.draw.rect(self.screen, RED, hp2_rect)
        hp2_fill = (game_state.ball2.health / game_state.ball2.max_health) * hp2_rect.width
        pygame.draw.rect(self.screen, (0, 255, 0), (hp2_rect.x, hp2_rect.y, hp2_fill, hp2_rect.height))

        # Полоски характеристик внизу
        stat_y_start = HEIGHT - 180
        stats1 = game_state.ball1.stats
        self.draw_stats_bar("Damage", stats1['damage'], 50, 50, stat_y_start, 200, 30, RED)
        self.draw_stats_bar("Range", stats1['range'], 200, 50, stat_y_start + 40, 200, 30, BLUE)
        
        stats2 = game_state.ball2.stats
        self.draw_stats_bar("Damage", stats2['damage'], 50, WIDTH - 250, stat_y_start, 200, 30, RED)
        self.draw_stats_bar("Range", stats2['range'], 200, WIDTH - 250, stat_y_start + 40, 200, 30, BLUE)

        # Экран победы
        if game_state.winner:
            winner_text = f"{game_state.winner.upper()} WINS!"
            self.draw_text(winner_text, self.font_large, GOLD, WIDTH / 2, HEIGHT / 2)

        return self.screen