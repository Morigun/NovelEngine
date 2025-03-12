import os
import sys
import subprocess
import shutil
import time

def main():
    """
    Основной скрипт для сборки проекта в EXE-файл
    """
    print("=" * 50)
    print("Сборка проекта NovelEngine в EXE-файл")
    print("=" * 50)
    
    # Шаг 1: Создание иконки
    print("\nШаг 1: Создание иконки...")
    try:
        import create_icon
        create_icon.create_icon()
    except Exception as e:
        print(f"Ошибка при создании иконки: {e}")
        print("Продолжаем без иконки...")
    
    # Шаг 2: Проверка зависимостей
    print("\nШаг 2: Проверка зависимостей...")
    required_packages = ["pygame", "pyinstaller"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} установлен")
        except ImportError:
            missing_packages.append(package)
            print(f"  ✗ {package} не установлен")
    
    if missing_packages:
        print("\nУстановка отсутствующих пакетов...")
        for package in missing_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                print(f"  ✓ {package} успешно установлен")
            except subprocess.CalledProcessError:
                print(f"  ✗ Не удалось установить {package}")
                print("Сборка прервана из-за отсутствия необходимых зависимостей.")
                return False
    
    # Шаг 3: Сборка проекта
    print("\nШаг 3: Сборка проекта...")
    
    # Параметры для PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--name=NovelEngine",
        "--onefile",  # Создаем один EXE-файл
        "--windowed",  # Без консольного окна
        "--icon=Assets/icon.png" if os.path.exists("Assets/icon.png") else "",
        "--add-data=Assets;Assets",  # Добавляем ресурсы
        "--add-data=story;story",
        "--add-data=engine;engine",
        "main.py"
    ]
    
    # Удаляем пустые аргументы
    pyinstaller_args = [arg for arg in pyinstaller_args if arg]
    
    # Запускаем PyInstaller
    try:
        subprocess.run(pyinstaller_args, check=True)
        print("Сборка успешно завершена!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сборке: {e}")
        return False
    
    # Шаг 4: Копирование результата
    print("\nШаг 4: Копирование результата...")
    if os.path.exists("dist/NovelEngine.exe"):
        shutil.copy("dist/NovelEngine.exe", "NovelEngine.exe")
        print("Исполняемый файл скопирован в корневую директорию: NovelEngine.exe")
    else:
        print("Ошибка: Исполняемый файл не найден в директории dist/")
        return False
    
    print("\n" + "=" * 50)
    print("Сборка успешно завершена!")
    print("Вы можете запустить игру, открыв файл NovelEngine.exe")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    start_time = time.time()
    success = main()
    end_time = time.time()
    
    print(f"\nВремя сборки: {end_time - start_time:.2f} секунд")
    
    if success:
        print("Нажмите Enter для выхода...")
        input()
    else:
        print("Сборка завершилась с ошибками. Нажмите Enter для выхода...")
        input()
        sys.exit(1) 