# main.py
import os
import shutil
import pygame
import time

from config import *
from simulation import GameState
from renderer import Renderer
from audio_generator import generate_intro_audio
from video_compiler import compile_video

# Импортируем новых бойцов
from balls.sword_ball import SwordBall
from balls.spear_ball import SpearBall

def cleanup():
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    # Создаем папку assets если её нет
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        print(f"Создана папка {ASSETS_DIR} для изображений оружия")

def main():
    pygame.init()
    
    # Инициализируем звук
    pygame.mixer.init()
    
    # Сохраняем главный экран в переменную
    display_screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Ball Duel Simulator - Physics Combat")

    cleanup()

    renderer = Renderer(WIDTH, HEIGHT)

    # Создаем шары - теперь они подчиняются гравитации!
    ball1 = SwordBall(x=ARENA_X + 100, y=ARENA_Y + 100)  # Начинаем сверху
    ball2 = SpearBall(x=ARENA_X + ARENA_WIDTH - 100, y=ARENA_Y + 100)

    game_state = GameState(ball1, ball2)

    # Генерируем интро аудио
    intro_text = f"Physics-based epic battle! {ball1.name} versus {ball2.name}! Watch them fall, bounce and fight with gravity!"
    generate_intro_audio(intro_text, INTRO_AUDIO_PATH)

    running = True
    frame_count = 0
    clock = pygame.time.Clock()
    max_frames = FPS * 120  # 2 минуты максимум

    print("Начинаем физическую симуляцию с гравитацией!")
    print("Шарики будут падать, отскакивать и вращаться реалистично!")

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Замедление при парировании
        if game_state.parry_effect_timer > 15:
            time.sleep(0.03)

        game_state.update()

        # Рендер
        screen_surface = renderer.draw(game_state)
        
        # Показываем на экране
        display_screen.blit(screen_surface, (0, 0))
        pygame.display.flip()

        # Сохранение кадра для видео
        frame_filename = os.path.join(FRAMES_DIR, f"frame_{frame_count:05d}.png")
        pygame.image.save(screen_surface, frame_filename)

        frame_count += 1
        clock.tick(FPS)

        # Показываем прогресс
        if frame_count % (FPS * 10) == 0:  # Каждые 10 секунд
            print(f"Прошло {frame_count // FPS} секунд. Здоровье: {game_state.ball1.name}={int(game_state.ball1.health)}, {game_state.ball2.name}={int(game_state.ball2.health)}")

        if game_state.winner:
            print(f"Победитель: {game_state.winner}!")
            # Сохраняем еще 4 секунды кадров с победным экраном
            for _ in range(FPS * 4):
                screen_surface = renderer.draw(game_state)
                display_screen.blit(screen_surface, (0, 0))
                pygame.display.flip()
                
                frame_filename = os.path.join(FRAMES_DIR, f"frame_{frame_count:05d}.png")
                pygame.image.save(screen_surface, frame_filename)
                frame_count += 1
                clock.tick(FPS)
            running = False

    pygame.quit()
    
    print("Компилируем видео...")
    compile_video(FRAMES_DIR, INTRO_AUDIO_PATH, HIT_SOUND_PATH, game_state.hit_events, FINAL_VIDEO_PATH, FPS)
    
    # Очищаем временные кадры
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    
    print(f"Готово! Видео сохранено: {FINAL_VIDEO_PATH}")

if __name__ == "__main__":
    main()