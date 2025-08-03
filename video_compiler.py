# video_compiler.py
import os
import glob
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip

def compile_video(frames_dir, intro_audio_path, hit_sound_path, hit_frames, output_path, fps, parry_frames=None):
    """
    Компилирует видео с раздельными звуками для ударов и парирований
    
    Args:
        frames_dir: Папка с кадрами
        intro_audio_path: Путь к интро аудио
        hit_sound_path: Путь к звуку удара
        hit_frames: Список кадров с ударами
        output_path: Путь для сохранения видео
        fps: Частота кадров
        parry_frames: Список кадров с парированием (опционально)
    """
    print("Сборка видео...")
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
    if not frame_files:
        print("Кадры не найдены!")
        return

    clip = ImageSequenceClip(frame_files, fps=fps)

    final_audio_clips = []
    
    # Добавляем интро аудио
    if os.path.exists(intro_audio_path):
        final_audio_clips.append(AudioFileClip(intro_audio_path))
    
    # Добавляем звуки ударов
    if os.path.exists(hit_sound_path) and hit_frames:
        hit_sound = AudioFileClip(hit_sound_path)
        
        # Отделяем парирования от обычных ударов
        parry_frame_set = set(parry_frames) if parry_frames else set()
        
        for frame_num in hit_frames:
            time_sec = frame_num / fps  # Конвертируем номер кадра в секунды
            
            if frame_num in parry_frame_set:
                # Для парирования используем звук удара, но с другой громкостью/эффектом
                parry_sound = hit_sound.volumex(0.8)  # Громче для парирования
                final_audio_clips.append(parry_sound.set_start(time_sec))
            else:
                # Обычный удар
                final_audio_clips.append(hit_sound.set_start(time_sec))
    
    # Попытка добавить отдельный звук парирования
    parry_sound_path = "assets/sounds/parry.mp3"
    if os.path.exists(parry_sound_path) and parry_frames:
        try:
            parry_sound_effect = AudioFileClip(parry_sound_path)
            for frame_num in parry_frames:
                time_sec = frame_num / fps
                final_audio_clips.append(parry_sound_effect.set_start(time_sec))
        except Exception as e:
            print(f"Не удалось загрузить звук парирования: {e}")

    # Компилируем финальное аудио
    if final_audio_clips:
        final_audio = CompositeAudioClip(final_audio_clips)
        if final_audio.duration > clip.duration:
             final_audio = final_audio.subclip(0, clip.duration)
        clip = clip.set_audio(final_audio)

    # Сохраняем видео
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, logger='bar')
    print(f"Видео успешно сохранено в {output_path}")