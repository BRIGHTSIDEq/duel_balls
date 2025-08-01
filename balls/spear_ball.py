# balls/spear_ball.py
from .base_fighter import FightingBall
import pygame

class SpearBall(FightingBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, radius=40, color=(0, 0, 200), 
                         name="Spear", weapon_image_name="spear.png")
        self.stats = {'damage': 5, 'range': 120, 'speed': 7}
        self.vx = -self.stats['speed'] # Двигается влево

    def attack(self, target):
        # С каждым ударом урон и длина копья растут
        self.stats['damage'] += 0.5
        
        # Увеличиваем длину (range) и масштабируем изображение
        self.stats['range'] += 2
        new_height = self.original_weapon_image.get_height() * (self.stats['range'] / 120)
        self.weapon_image = pygame.transform.scale(self.original_weapon_image, (self.original_weapon_image.get_width(), int(new_height)))
        
        target.take_damage(self.stats['damage'])