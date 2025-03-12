import pygame

# Настройки экрана
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Visual Novel"

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 150)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
TEXT_BOX_COLOR = (0, 0, 0, 180)

# Настройки текста
FONT_SIZE = 24
NAME_FONT_SIZE = 32
BUTTON_FONT_SIZE = 20

# Настройки текстового окна
TEXT_BOX_HEIGHT = 180
TEXT_BOX_PADDING = 15

# Настройки кнопок навигации
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_PADDING = 20
BUTTON_Y = WINDOW_HEIGHT - TEXT_BOX_HEIGHT // 2 - BUTTON_HEIGHT // 2

# Настройки области текста
TEXT_AREA_WIDTH = WINDOW_WIDTH - 2 * (BUTTON_WIDTH + 2 * BUTTON_PADDING)
TEXT_LINE_SPACING = 4
MAX_TEXT_LINES = 5

# Настройки персонажей
CHARACTER_HEIGHT = int(WINDOW_HEIGHT * 0.25)
CHARACTER_Y_POSITION = WINDOW_HEIGHT - TEXT_BOX_HEIGHT - CHARACTER_HEIGHT

# Позиции персонажей по горизонтали
CHARACTER_LEFT = WINDOW_WIDTH * 0.2
CHARACTER_CENTER = WINDOW_WIDTH * 0.5
CHARACTER_RIGHT = WINDOW_WIDTH * 0.8

# Пути к ресурсам
CHARACTERS_PATH = "Assets/Characters/"
BACKGROUNDS_PATH = "Assets/Backgrounds/" 