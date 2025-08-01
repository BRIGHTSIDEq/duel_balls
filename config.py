# config.py

# Настройки экрана и видео (вертикальный формат для Shorts/TikTok)
WIDTH = 720
HEIGHT = 1280
FPS = 60

# Цвета (RGB)
VANILLA = (243, 229, 171) # Ванильный фон
GREY = (220, 220, 220) # Серовато-белый для арены
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# Настройки арены
ARENA_PADDING_X = 50
ARENA_PADDING_Y = 200
ARENA_X = ARENA_PADDING_X
ARENA_Y = ARENA_PADDING_Y
ARENA_WIDTH = WIDTH - 2 * ARENA_PADDING_X
ARENA_HEIGHT = HEIGHT - 2 * ARENA_PADDING_Y

# Пути
FONT_PATH = "assets/fonts/BebasNeue-Regular.ttf"
ASSETS_DIR = "assets" # Новая папка для изображений
OUTPUT_DIR = "output"
FRAMES_DIR = f"{OUTPUT_DIR}/frames"
FINAL_VIDEO_PATH = f"{OUTPUT_DIR}/final_video.mp4"
INTRO_AUDIO_PATH = f"{OUTPUT_DIR}/intro.mp3"
HIT_SOUND_PATH = "assets/sounds/ball_s.mp3"
PARRY_SOUND_PATH = "assets/sounds/parry.mp3" # Добавьте звук для парирования
WIN_SOUND_PATH = "assets/sounds/victory_sound.mp3"