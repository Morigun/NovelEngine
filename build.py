import os
import shutil
import subprocess
import sys

def build_exe():
    """
    Сборка проекта в исполняемый файл с помощью PyInstaller
    """
    print("Начинаю сборку проекта в EXE-файл...")
    
    # Создаем директорию для сборки, если она не существует
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # Параметры для PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--name=NovelEngine",
        "--onefile",  # Создаем один EXE-файл
        "--windowed",  # Без консольного окна
        "--icon=Assets/icon.ico" if os.path.exists("Assets/icon.ico") else "",
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
        
        # Копируем EXE-файл в корневую директорию
        if os.path.exists("dist/NovelEngine.exe"):
            shutil.copy("dist/NovelEngine.exe", "NovelEngine.exe")
            print("Исполняемый файл скопирован в корневую директорию: NovelEngine.exe")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сборке: {e}")
        return False

if __name__ == "__main__":
    build_exe() 