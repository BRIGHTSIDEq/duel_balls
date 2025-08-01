import pygame
from config import WIDTH, HEIGHT, FONT_PATH

BALL_OPTIONS = [
    "One Punchy",
    "Laserry",
    "Duplicator",
    "Gravislam",
    "Poisony"
]

def draw_menu(screen, font, selected_top, selected_bottom):
    screen.fill((245, 245, 220))  # бежевый фон

    title_font = pygame.font.Font(FONT_PATH, 50)
    text_top = title_font.render("Выберите шарик сверху:", True, (0, 0, 0))
    text_bottom = title_font.render("Выберите шарик снизу:", True, (0, 0, 0))
    screen.blit(text_top, (50, 20))
    screen.blit(text_bottom, (50, HEIGHT//2 + 20))

    option_font = pygame.font.Font(FONT_PATH, 36)

    for i, option in enumerate(BALL_OPTIONS):
        color_top = (0, 100, 255) if i == selected_top else (0,0,0)
        color_bottom = (255, 100, 0) if i == selected_bottom else (0,0,0)
        # Сверху
        text = option_font.render(option, True, color_top)
        screen.blit(text, (100, 80 + i*40))
        # Снизу
        text2 = option_font.render(option, True, color_bottom)
        screen.blit(text2, (100, HEIGHT//2 + 80 + i*40))

    instr_font = pygame.font.Font(FONT_PATH, 24)
    instr1 = instr_font.render("Используйте стрелки Вверх/Вниз для выбора сверху", True, (0,0,0))
    instr2 = instr_font.render("Используйте W/S для выбора снизу", True, (0,0,0))
    instr3 = instr_font.render("Нажмите ENTER для подтверждения", True, (0,0,0))
    screen.blit(instr1, (50, HEIGHT - 100))
    screen.blit(instr2, (50, HEIGHT - 75))
    screen.blit(instr3, (50, HEIGHT - 50))

    pygame.display.flip()

def get_selection():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Выбор шариков")

    selected_top = 0
    selected_bottom = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        draw_menu(screen, pygame.font.Font(FONT_PATH, 36), selected_top, selected_bottom)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_top = (selected_top - 1) % len(BALL_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected_top = (selected_top + 1) % len(BALL_OPTIONS)
                elif event.key == pygame.K_w:
                    selected_bottom = (selected_bottom - 1) % len(BALL_OPTIONS)
                elif event.key == pygame.K_s:
                    selected_bottom = (selected_bottom + 1) % len(BALL_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    running = False

        clock.tick(30)
    pygame.quit()
    return BALL_OPTIONS[selected_top], BALL_OPTIONS[selected_bottom]
