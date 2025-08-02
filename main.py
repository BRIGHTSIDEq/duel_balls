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

# Импортируем улучшенных бойцов
from balls.sword_ball import SwordBall
from balls.spear_ball import SpearBall

def cleanup():
    """Очистка временных файлов и создание необходимых папок"""
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    # Создаем папку assets если её нет (для звуков)
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        print(f"Создана папка {ASSETS_DIR} для звуковых файлов")

def main():
    pygame.init()
    
    # Инициализируем звук
    pygame.mixer.init()
    
    # Сохраняем главный экран в переменную
    display_screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption("Epic Ball Duel - Pixel Weapons Combat!")

    cleanup()

    renderer = Renderer(WIDTH, HEIGHT)

    # Создаем улучшенных бойцов с пиксельными оружиями
    # Позиционируем их в противоположных углах арены
    ball1 = SwordBall(x=ARENA_X + 80, y=ARENA_Y + 80)
    ball2 = SpearBall(x=ARENA_X + ARENA_WIDTH - 80, y=ARENA_Y + ARENA_HEIGHT - 80)

    game_state = GameState(ball1, ball2)

    # Генерируем интро аудио
    intro_text = f"Epic pixel weapon combat! {ball1.name} with evolving sword versus {ball2.name} with extending spear! Watch weapons grow with every hit!"
    generate_intro_audio(intro_text, INTRO_AUDIO_PATH)

    running = True
    frame_count = 0
    clock = pygame.time.Clock()
    max_frames = FPS * 150  # 2.5 минуты максимум

    print("🎮 Запускаем ПИКСЕЛЬНУЮ дуэль!")
    print("⚔️ Новые фичи:")
    print("  - Красивые пиксельные мечи и копья")
    print("  - Оружие растет с каждым ударом")
    print("  - Статистики подняты ближе к арене")
    print("  - Квадратная арена для TikTok/YouTube")
    print("  - Улучшенная физика и парирование")

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Драматическое замедление при парировании
        if game_state.parry_effect_timer > 20:
            time.sleep(0.05)  # Более заметное замедление
        elif game_state.parry_effect_timer > 10:
            time.sleep(0.02)

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
        if frame_count % (FPS * 15) == 0:  # Каждые 15 секунд
            minutes = frame_count // FPS // 60
            seconds = (frame_count // FPS) % 60
            print(f"⏱️ {minutes:02d}:{seconds:02d} | "
                  f"💚 {ball1.name}: {int(ball1.health)} (⚔️{int(ball1.weapon_length)}) | "
                  f"💙 {ball2.name}: {int(ball2.health)} (🔱{int(ball2.weapon_length)}) | "
                  f"💥 Hits: {len(game_state.hit_events)}")

        if game_state.winner:
            winner_ball = ball1 if game_state.winner == ball1.name else ball2
            print(f"🏆 ПОБЕДИТЕЛЬ: {game_state.winner}!")
            print(f"💪 Финальный урон: {int(winner_ball.stats['damage'])}")
            print(f"⚔️ Финальная длина оружия: {int(winner_ball.weapon_length)}")
            print(f"💥 Всего ударов в бою: {len(game_state.hit_events)}")
            
            # Сохраняем еще 5 секунд кадров с победным экраном
            for victory_frame in range(FPS * 5):
                screen_surface = renderer.draw(game_state)
                display_screen.blit(screen_surface, (0, 0))
                pygame.display.flip()
                
                frame_filename = os.path.join(FRAMES_DIR, f"frame_{frame_count:05d}.png")
                pygame.image.save(screen_surface, frame_filename)
                frame_count += 1
                clock.tick(FPS)
            running = False

    pygame.quit()
    
    print("🎬 Компилируем финальное видео...")
    compile_video(FRAMES_DIR, INTRO_AUDIO_PATH, HIT_SOUND_PATH, game_state.hit_events, FINAL_VIDEO_PATH, FPS)
    
    # Очищаем временные кадры
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    
    print(f"✅ ГОТОВО! Пиксельное эпическое видео сохранено: {FINAL_VIDEO_PATH}")
    print("🎥 Готово для TikTok/YouTube Shorts!")
    print("⚔️ С растущими пиксельными оружиями!")

if __name__ == "__main__":
    main()