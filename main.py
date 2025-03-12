"""
NovelEngine - движок для создания визуальных новелл на Python с использованием Pygame.
"""

import os
import sys

def resource_path(relative_path):
    """
    Получает абсолютный путь к ресурсу, работает как для разработки, 
    так и для PyInstaller
    """
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    """
    Основная функция для запуска игры.
    """
    # Добавляем текущую директорию в путь поиска модулей
    if getattr(sys, 'frozen', False):
        # Если запущено из PyInstaller
        os.chdir(os.path.dirname(sys.executable))
    else:
        # Если запущено из исходного кода
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Импортируем модули после настройки путей
    from engine.game import Game
    from story.story import load_story
    
    # Создание экземпляра игры
    game = Game()
    
    # Загрузка сюжета
    load_story(game)
    
    # Запуск игры
    game.run()

if __name__ == "__main__":
    main() 