# main.py
import os
import shutil
import pygame
import time

from config import *
from simulation import GameState
from renderer import Renderer
from audio_generator import generate_intro_audio # Можно оставить
from video_compiler import compile_video # Можно оставить

# Импортируем новых бойцов
from balls.sword_ball import SwordBall
from balls.spear_ball import SpearBall

def cleanup():
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    os.makedirs(FRAMES_DIR, exist_ok=True)

def main():
    pygame.init()
    # Сохраняем главный экран в переменную
    display_screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Ball Duel Simulator") # Добавим заголовок окну

    cleanup()

    renderer = Renderer(WIDTH, HEIGHT)

    ball1 = SwordBall(x=ARENA_X + 100, y=ARENA_Y + ARENA_HEIGHT / 2)
    ball2 = SpearBall(x=ARENA_X + ARENA_WIDTH - 100, y=ARENA_Y + ARENA_HEIGHT / 2)

    game_state = GameState(ball1, ball2)

    running = True
    frame_count = 0
    clock = pygame.time.Clock()
    max_frames = FPS * 60

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state.parry_effect_timer == 5:
            time.sleep(0.1)

        game_state.update()

        # renderer.draw() возвращает поверхность, на которой всё нарисовано
        screen_surface = renderer.draw(game_state)
        
        # --- ДОБАВЬТЕ ЭТИ ДВЕ СТРОКИ ---
        display_screen.blit(screen_surface, (0, 0)) # Копируем наш холст на главный экран
        pygame.display.flip()                      # Обновляем экран, чтобы увидеть изменения
        # ---------------------------------

        # Сохранение кадра для видео остаётся без изменений
        frame_filename = os.path.join(FRAMES_DIR, f"frame_{frame_count:05d}.png")
        pygame.image.save(screen_surface, frame_filename)

        frame_count += 1
        clock.tick(FPS)

        if game_state.winner:
            # Сохраняем еще 2 секунды кадров с победным экраном
            for _ in range(FPS * 2):
                screen_surface = renderer.draw(game_state)
                frame_filename = os.path.join(FRAMES_DIR, f"frame_{frame_count:05d}.png")
                pygame.image.save(screen_surface, frame_filename)
                frame_count += 1
            running = False

    compile_video(FRAMES_DIR, INTRO_AUDIO_PATH, HIT_SOUND_PATH, game_state.hit_events, FINAL_VIDEO_PATH, FPS)

    shutil.rmtree(FRAMES_DIR) # Не удаляем кадры, если компилятор еще не отработал

if __name__ == "__main__":
    main()