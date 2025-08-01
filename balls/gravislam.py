from .base_ball import Ball
import pygame

class Gravislam(Ball):
    def __init__(self, x, y, direction, hit_sound=None):
        super().__init__(x, y, radius=25, color=(0, 255, 255), name="Gravislam", direction=direction, hit_sound=hit_sound)
        self.gravity = 0.6
        self.base_gravity = 0.6
        self.damage = 1
        self.hit_count = 0
        self.echo_positions = []

    def attack(self, platform, game_state, frame_count):
        super().attack(platform, game_state, frame_count)
        self.hit_count += 1
        self.damage += 1
        # Уменьшаем гравитацию постепенно, но не меньше 0
        self.gravity = max(0, self.base_gravity - self.hit_count * 0.1)
        # Добавляем позицию для эффекта эхо
        self.echo_positions.append(self.rect.center)
        if len(self.echo_positions) > 5:
            self.echo_positions.pop(0)

    def draw(self, screen):
        # Рисуем эхо
        for i, pos in enumerate(self.echo_positions):
            alpha = max(0, 255 - i * 50)
            surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(surf, (pos[0] - self.radius, pos[1] - self.radius))
        super().draw(screen)
