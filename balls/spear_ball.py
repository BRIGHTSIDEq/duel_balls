# balls/spear_ball.py  
from .base_fighter import FightingBall

class SpearBall(FightingBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, radius=40, color=(0, 200, 200), 
                         name="Spear", weapon_type="spear")
        self.stats = {'damage': 6, 'range': 120, 'speed': 7, 'radius': self.radius}
        
        # Параметры копья
        self.weapon_length = 70  # Копье изначально длиннее
        self.weapon_width = 6
        self.weapon_color = (139, 69, 19)  # Коричневое древко

    def on_successful_attack(self, target):
        # С каждым ударом урон и длина копья растут
        self.stats['damage'] += 0.8
        self.stats['range'] += 3
        self.weapon_length += 5  # Копье растет быстрее чем меч