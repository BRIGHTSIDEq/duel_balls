
# balls/sword_ball.py
from .base_fighter import FightingBall

class SwordBall(FightingBall):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, radius=40, color=(200, 0, 200), 
                         name="Sword", weapon_type="sword")
        self.stats = {'damage': 8, 'range': 100, 'speed': 5, 'radius': self.radius}
        
        # Параметры меча
        self.weapon_length = 50
        self.weapon_width = 10
        self.weapon_color = (150, 150, 150)  # Серебристый

    def on_successful_attack(self, target):
        # С каждым ударом урон меча растёт и он становится длиннее
        self.stats['damage'] += 1.2
        self.weapon_length += 2  # Меч растет с каждым ударом
        self.weapon_width = min(12, self.weapon_width + 0.2)  # И становится толще