# balls/spear_ball.py  
from .base_fighter import FightingBall

class SpearBall(FightingBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, radius=40, color=(50, 200, 200), 
                         name="Spear Hunter", weapon_type="spear")
        
        self.stats = {'damage': 5, 'range': 120, 'speed': 7, 'radius': self.radius}
        
        # Параметры копья - увеличенные в 2 раза
        self.weapon_length = 100
        self.weapon_width = 10
        
        # Улучшенная физика для копейщика
        self.max_speed = 25
        self.weapon_rotation_speed = 6

    def on_successful_attack(self, target):
        # Копье растет быстрее по длине и урону
        self.stats['damage'] += 2.0
        self.stats['range'] += 4
        self.weapon_length += 12  # Копье растет еще быстрее
        self.weapon_width = min(40, self.weapon_width + 0.6)
        
        # Копейщик получает скорость после удара
        self.max_speed = min(30, self.max_speed + 0.5)