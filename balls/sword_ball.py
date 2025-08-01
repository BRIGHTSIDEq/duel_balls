# balls/sword_ball.py
from .base_fighter import FightingBall
import pygame

class SwordBall(FightingBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, radius=40, color=(200, 0, 0), 
                         name="Sword", weapon_image_name="sword.png")
        self.stats = {'damage': 10, 'range': 100, 'speed': 5}
        self.vx = self.stats['speed']

    def attack(self, target):
        # С каждым ударом урон меча растёт
        self.stats['damage'] += 1
        target.take_damage(self.stats['damage'])