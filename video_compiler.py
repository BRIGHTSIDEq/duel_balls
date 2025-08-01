# video_compiler.py
import os
import glob
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip

# Меняем название параметра для ясности
def compile_video(frames_dir, intro_audio_path, hit_sound_path, hit_frames, output_path, fps):
    print("Сборка видео...")
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
    if not frame_files:
        print("Кадры не найдены!")
        return

    clip = ImageSequenceClip(frame_files, fps=fps)

    final_audio_clips = []
    if os.path.exists(intro_audio_path):
        final_audio_clips.append(AudioFileClip(intro_audio_path))
    
    # Конвертируем кадры в секунды
    if os.path.exists(hit_sound_path) and hit_frames:
        hit_sound = AudioFileClip(hit_sound_path)
        for frame_num in hit_frames:
            time_sec = frame_num / fps # Конвертируем номер кадра в секунды
            final_audio_clips.append(hit_sound.set_start(time_sec))

    if final_audio_clips:
        final_audio = CompositeAudioClip(final_audio_clips)
        if final_audio.duration > clip.duration:
             final_audio = final_audio.subclip(0, clip.duration)
        clip = clip.set_audio(final_audio)

    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4, logger='bar')
    print(f"Видео успешно сохранено в {output_path}")