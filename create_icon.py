import pygame
import os

def create_icon():
    """
    Создает простую иконку для приложения
    """
    # Инициализация Pygame
    pygame.init()
    
    # Создаем директорию для иконки, если она не существует
    if not os.path.exists("Assets"):
        os.makedirs("Assets")
    
    # Создаем поверхность для иконки
    icon_size = 64
    icon = pygame.Surface((icon_size, icon_size))
    
    # Заполняем фон
    icon.fill((50, 50, 150))  # Темно-синий фон
    
    # Рисуем книгу
    pygame.draw.rect(icon, (200, 200, 200), (10, 15, 44, 34))  # Страницы
    pygame.draw.rect(icon, (150, 100, 50), (10, 15, 5, 34))    # Корешок
    
    # Рисуем текст на книге (имитация строк)
    for i in range(5):
        pygame.draw.line(icon, (100, 100, 100), 
                        (20, 22 + i*6), (45, 22 + i*6), 1)
    
    # Сохраняем иконку
    pygame.image.save(icon, "Assets/icon.png")
    
    # Конвертируем PNG в ICO с помощью Pygame
    try:
        # Загружаем PNG
        icon_surface = pygame.image.load("Assets/icon.png")
        
        # Создаем ICO
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        pygame.display.set_icon(icon_surface)
        
        # Сохраняем иконку как ICO
        with open("Assets/icon.ico", "wb") as f:
            pygame.image.save(pygame.display.get_surface(), "Assets/icon.ico")
        
        print("Иконка успешно создана: Assets/icon.ico")
        return True
    except Exception as e:
        print(f"Ошибка при создании ICO: {e}")
        print("Будет использована PNG-иконка")
        return False
    finally:
        pygame.quit()

if __name__ == "__main__":
    create_icon() 