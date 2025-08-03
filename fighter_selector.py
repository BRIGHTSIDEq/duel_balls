# fighter_selector.py
import pygame
import sys
from config import WIDTH, HEIGHT, VANILLA, BLACK, WHITE, GOLD

class FighterSelector:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Выберите бойцов для эпической дуэли!")
        
        try:
            self.font_large = pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", 80)
            self.font_medium = pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", 50)
            self.font_small = pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", 35)
        except:
            self.font_large = pygame.font.Font(None, 80)
            self.font_medium = pygame.font.Font(None, 50)
            self.font_small = pygame.font.Font(None, 35)
        
        self.fighters = {
            1: {
                'name': 'Sword Master',
                'color': (200, 50, 200),
                'description': 'Мощные удары мечом',
                'special': 'Растет в силе с каждым ударом',
                'class': 'SwordBall'
            },
            2: {
                'name': 'Spear Hunter', 
                'color': (50, 200, 200),
                'description': 'Длинное копье, быстрые атаки',
                'special': 'Копье растет быстрее всех',
                'class': 'SpearBall'
            },
            3: {
                'name': 'Axe Berserker',
                'color': (150, 75, 0),
                'description': 'Двуручный топор, мощный рывок',
                'special': 'Неуязвим во время рывка раз в 5 сек',
                'class': 'AxeBall'
            },
            4: {
                'name': 'Archer Lord',
                'color': (34, 139, 34),
                'description': 'Стрелы издалека, растущий залп',
                'special': 'Количество стрел +1 после каждого выстрела',
                'class': 'BowBall'
            }
        }
        
        self.selected_fighter1 = None
        self.selected_fighter2 = None
        self.selection_stage = 1  # 1 = выбор первого бойца, 2 = выбор второго

    def draw_text_with_shadow(self, text, font, color, x, y, center=True):
        """Рисует текст с тенью"""
        # Тень
        shadow_surface = font.render(text, True, BLACK)
        shadow_rect = shadow_surface.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Основной текст
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_fighter_card(self, fighter_id, x, y, width, height, is_selected=False, is_available=True):
        """Рисует карточку бойца"""
        fighter = self.fighters[fighter_id]
        
        # Цвет рамки в зависимости от состояния
        border_color = GOLD if is_selected else WHITE
        if not is_available:
            border_color = (100, 100, 100)
        
        # Основная рамка
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, fighter['color'] if is_available else (80, 80, 80), card_rect)
        pygame.draw.rect(self.screen, border_color, card_rect, 5)
        
        # Номер бойца
        number_text = str(fighter_id)
        self.draw_text_with_shadow(number_text, self.font_large, WHITE, x + 30, y + 30, False)
        
        # Имя бойца
        name_color = WHITE if is_available else (150, 150, 150)
        self.draw_text_with_shadow(fighter['name'], self.font_medium, name_color, 
                                   x + width//2, y + 60, True)
        
        # Описание
        desc_color = (220, 220, 220) if is_available else (120, 120, 120)
        self.draw_text_with_shadow(fighter['description'], self.font_small, desc_color,
                                   x + width//2, y + 110, True)
        
        # Особенность
        special_color = GOLD if is_available else (150, 120, 80)
        special_lines = self.wrap_text(fighter['special'], self.font_small, width - 20)
        for i, line in enumerate(special_lines):
            self.draw_text_with_shadow(line, self.font_small, special_color,
                                       x + width//2, y + 150 + i*30, True)

    def wrap_text(self, text, font, max_width):
        """Переносит текст на несколько строк"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def draw_selection_screen(self):
        """Рисует экран выбора"""
        # Градиентный фон
        for y in range(HEIGHT):
            color_ratio = y / HEIGHT
            r = int(243 * (1 - color_ratio) + 200 * color_ratio)
            g = int(229 * (1 - color_ratio) + 220 * color_ratio)
            b = int(171 * (1 - color_ratio) + 180 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Заголовок
        if self.selection_stage == 1:
            title = "ВЫБЕРИТЕ ПЕРВОГО БОЙЦА"
            subtitle = "Нажмите цифру 1-4"
        else:
            title = "ВЫБЕРИТЕ ВТОРОГО БОЙЦА"
            subtitle = f"Первый боец: {self.fighters[self.selected_fighter1]['name']}"
        
        self.draw_text_with_shadow(title, self.font_large, BLACK, WIDTH//2, 80, True)
        self.draw_text_with_shadow(subtitle, self.font_medium, (100, 100, 100), WIDTH//2, 140, True)
        
        # Карточки бойцов (2x2 сетка)
        card_width = 300
        card_height = 250
        spacing = 50
        start_x = (WIDTH - 2 * card_width - spacing) // 2
        start_y = 200
        
        positions = [
            (start_x, start_y),                                    # 1
            (start_x + card_width + spacing, start_y),             # 2
            (start_x, start_y + card_height + spacing),            # 3
            (start_x + card_width + spacing, start_y + card_height + spacing)  # 4
        ]
        
        for i, (x, y) in enumerate(positions):
            fighter_id = i + 1
            is_available = (self.selection_stage == 1 or fighter_id != self.selected_fighter1)
            self.draw_fighter_card(fighter_id, x, y, card_width, card_height, 
                                 False, is_available)
        
        # Инструкции
        if self.selection_stage == 1:
            instruction = "Нажмите цифру от 1 до 4 для выбора бойца"
        else:
            instruction = "Выберите второго бойца (не может быть таким же как первый)"
        
        self.draw_text_with_shadow(instruction, self.font_small, BLACK, 
                                   WIDTH//2, HEIGHT - 100, True)
        
        # ESC для выхода
        self.draw_text_with_shadow("ESC - Выход", self.font_small, (100, 100, 100),
                                   50, HEIGHT - 50, False)

    def select_fighters(self):
        """Основной цикл выбора бойцов"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    # Выбор бойца по цифрам
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        choice = event.key - pygame.K_0  # Преобразуем в число
                        
                        if self.selection_stage == 1:
                            self.selected_fighter1 = choice
                            self.selection_stage = 2
                        else:
                            if choice != self.selected_fighter1:
                                self.selected_fighter2 = choice
                                return self.selected_fighter1, self.selected_fighter2
                            # Если выбрал того же бойца - игнорируем
            
            self.draw_selection_screen()
            pygame.display.flip()
            clock.tick(60)
        
        return None, None

def get_fighter_classes():
    """Возвращает словарь классов бойцов"""
    from balls.sword_ball import SwordBall
    from balls.spear_ball import SpearBall  
    from balls.axe_ball import AxeBall
    from balls.bow_ball import BowBall
    
    return {
        'SwordBall': SwordBall,
        'SpearBall': SpearBall,
        'AxeBall': AxeBall,
        'BowBall': BowBall
    }