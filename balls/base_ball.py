import pygame
import random
from config import WIDTH, HEIGHT

class Ball:
    def __init__(self, x, y, radius, color, name, direction, hit_sound=None):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.name = name
        self.direction = direction

        self.vx = random.uniform(-3, 3)
        self.vy = 0
        self.gravity = 0.6
        self.damage = 1
        self.hit_sound = hit_sound

        self.texture = None  # для текстуры (если есть)

    def update(self, platforms, game_state, frame_count):
        self.vy += self.gravity if self.direction == 'down' else -self.gravity

        self.rect.x += self.vx
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        steps = int(abs(self.vy))
        step_direction = 1 if self.vy > 0 else -1
        for _ in range(steps):
            self.rect.y += step_direction
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if step_direction > 0:
                        self.rect.bottom = platform.rect.top
                    else:
                        self.rect.top = platform.rect.bottom
                    self.vy *= -1
                    self.attack(platform, game_state, frame_count)
                    return

        self.rect.y += self.vy - steps * step_direction

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy *= -1

    def attack(self, platform, game_state, frame_count):
        platform.take_damage(self.damage)
        game_state.hit_events.append(frame_count)
        if self.hit_sound:
            self.hit_sound.play()

    def draw(self, screen):
        if self.texture:
            # Рисуем текстуру, масштабируя под радиус
            texture_scaled = pygame.transform.smoothscale(self.texture, (self.radius*2, self.radius*2))
            screen.blit(texture_scaled, (self.rect.x, self.rect.y))
        else:
            pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
