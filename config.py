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

# УЛУЧШЕННЫЕ настройки арены - более квадратная и безопасная для TikTok UI
ARENA_PADDING_X = 60
ARENA_PADDING_Y = 150  # Больше отступ сверху и снизу для TikTok UI
ARENA_X = ARENA_PADDING_X
ARENA_Y = ARENA_PADDING_Y
ARENA_WIDTH = WIDTH - 2 * ARENA_PADDING_X  # 600px
ARENA_HEIGHT = 600  # Квадратная арена!

# UI зоны для TikTok/YouTube Shorts
SAFE_ZONE_TOP = 100  # Зона сверху для UI TikTok
SAFE_ZONE_BOTTOM = 150  # Зона снизу для UI TikTok

# Позиции для UI элементов
TITLE_Y = SAFE_ZONE_TOP // 2
HEALTH_BAR_TOP_Y = ARENA_Y - 40
HEALTH_BAR_BOTTOM_Y = ARENA_Y + ARENA_HEIGHT + 10
STATS_Y = ARENA_Y + ARENA_HEIGHT + 50  # Подняли статистики ближе к арене

# Пути
FONT_PATH = "assets/fonts/BebasNeue-Regular.ttf"
ASSETS_DIR = "assets" # Папка для звуков
OUTPUT_DIR = "output"
FRAMES_DIR = f"{OUTPUT_DIR}/frames"
FINAL_VIDEO_PATH = f"{OUTPUT_DIR}/final_video.mp4"
INTRO_AUDIO_PATH = f"{OUTPUT_DIR}/intro.mp3"
HIT_SOUND_PATH = "assets/sounds/ball_s.mp3"
PARRY_SOUND_PATH = "assets/sounds/parry.mp3"
WIN_SOUND_PATH = "assets/sounds/victory_sound.mp3"