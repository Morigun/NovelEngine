import pygame
import sys
from pygame import mixer
import os
from engine.config import *

class Game:
    """
    Основной класс игрового движка визуальной новеллы.
    Управляет сценами, персонажами, фонами и игровым циклом.
    """
    def __init__(self):
        """
        Инициализация игрового движка.
        """
        # Инициализация Pygame
        pygame.init()
        mixer.init()
        
        # Настройка экрана
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Флаг полноэкранного режима
        self.is_fullscreen = False
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        
        # Создаем основную поверхность для рендеринга
        self.game_surface = pygame.Surface((self.window_width, self.window_height))
        
        # Шрифты
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.name_font = pygame.font.Font(None, NAME_FONT_SIZE)
        self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        
        # Сцены
        self.scenes = []
        self.scene_map = {}  # Словарь для быстрого доступа к сценам по ID
        self.current_scene = 0
        
        # Флаг отображения выбора
        self.showing_choices = False
        self.choice_buttons = []
        
        # Переменные для отслеживания состояния игры
        self.variables = {}
        
        # Персонажи и фоны
        self.characters = {}
        self.backgrounds = {}
        self.original_backgrounds = {}  # Сохраняем оригинальные изображения фонов
        
        # Кнопки навигации
        self.back_button = pygame.Rect(BUTTON_PADDING, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.forward_button = pygame.Rect(WINDOW_WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 
                                      BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        # Флаг работы игры
        self.running = True
        
    def add_scene(self, scene):
        """
        Добавление сцены в игру
        
        :param scene: Объект класса Scene
        """
        self.scenes.append(scene)
        
        # Если у сцены есть ID, добавляем её в словарь для быстрого доступа
        if scene.scene_id is not None:
            self.scene_map[scene.scene_id] = len(self.scenes) - 1
            
    def add_character(self, name, image_path):
        """
        Добавление персонажа в игру.
        
        :param name: Имя персонажа (ключ)
        :param image_path: Путь к изображению персонажа
        """
        try:
            # Создаем директорию для персонажей, если её нет
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Если файл не существует, создаем заглушку
            if not os.path.exists(image_path):
                # Создаем простое изображение персонажа
                character_surface = pygame.Surface((200, 400))
                character_surface.fill(WHITE)
                pygame.draw.rect(character_surface, BLUE, (0, 0, 200, 400), 2)
                pygame.draw.ellipse(character_surface, BLUE, (50, 50, 100, 100))  # Голова
                pygame.draw.rect(character_surface, BLUE, (75, 150, 50, 200))    # Тело
                try:
                    pygame.image.save(character_surface, image_path)
                    print(f"Created placeholder image for character: {name}")
                except Exception as e:
                    print(f"Error creating placeholder for character {name}: {e}")
                    return
                
            try:
                character_img = pygame.image.load(image_path)
                self.characters[name] = character_img
            except pygame.error as e:
                print(f"Error loading character image {name}: {e}")
        except Exception as e:
            print(f"Error adding character {name}: {e}")
        
    def add_background(self, name, image_path):
        """
        Добавление фонового изображения
        
        :param name: Имя фона
        :param image_path: Путь к изображению
        """
        try:
            # Создаем директорию для фонов, если она не существует
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            if os.path.exists(image_path):
                try:
                    background = pygame.image.load(image_path).convert()
                    # Сохраняем оригинальное изображение
                    self.original_backgrounds[name] = background
                    # Масштабируем фон для заполнения экрана
                    self.backgrounds[name] = self.scale_background(background)
                except pygame.error as e:
                    print(f"Ошибка при загрузке фона {name}: {e}")
                    # Создаем заглушку для фона
                    placeholder = self.create_placeholder_background()
                    self.original_backgrounds[name] = placeholder
                    self.backgrounds[name] = placeholder
            else:
                print(f"Фоновое изображение не найдено: {image_path}")
                # Создаем заглушку для фона
                placeholder = self.create_placeholder_background()
                self.original_backgrounds[name] = placeholder
                self.backgrounds[name] = placeholder
        except Exception as e:
            print(f"Ошибка при добавлении фона {name}: {e}")
            # Создаем заглушку для фона
            placeholder = self.create_placeholder_background()
            self.original_backgrounds[name] = placeholder
            self.backgrounds[name] = placeholder

    def scale_background(self, background_image):
        """
        Масштабирует фоновое изображение, чтобы оно заполняло весь экран без рамок
        
        :param background_image: Исходное изображение фона
        :return: Масштабированное изображение
        """
        # Получаем размеры исходного изображения
        bg_width, bg_height = background_image.get_size()
        
        # Используем фактические размеры игровой поверхности
        game_width, game_height = self.game_surface.get_size()
        
        # Вычисляем соотношение сторон
        bg_ratio = bg_width / bg_height
        game_ratio = game_width / game_height
        
        # Определяем размеры для масштабирования
        if bg_ratio > game_ratio:
            # Изображение шире игровой поверхности (по соотношению сторон)
            # Масштабируем по высоте, ширина будет обрезана
            new_height = game_height
            new_width = int(new_height * bg_ratio)
        else:
            # Изображение уже игровой поверхности (по соотношению сторон)
            # Масштабируем по ширине, высота будет обрезана
            new_width = game_width
            new_height = int(new_width / bg_ratio)
        
        # Масштабируем изображение
        scaled_bg = pygame.transform.smoothscale(background_image, (new_width, new_height))
        
        # Создаем поверхность размером с игровую поверхность
        final_bg = pygame.Surface((game_width, game_height))
        
        # Вычисляем позицию для центрирования
        pos_x = (game_width - new_width) // 2
        pos_y = (game_height - new_height) // 2
        
        # Отображаем масштабированное изображение на поверхности
        final_bg.blit(scaled_bg, (pos_x, pos_y))
        
        return final_bg

    def create_placeholder_background(self):
        """
        Создает заглушку для фонового изображения
        
        :return: Поверхность с заглушкой
        """
        placeholder = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        placeholder.fill((200, 200, 200))  # Светло-серый фон
        
        # Добавляем сетку
        for x in range(0, WINDOW_WIDTH, 50):
            pygame.draw.line(placeholder, (180, 180, 180), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, 50):
            pygame.draw.line(placeholder, (180, 180, 180), (0, y), (WINDOW_WIDTH, y))
        
        # Добавляем текст "Фон отсутствует"
        font = pygame.font.Font(None, 48)
        text = font.render("Фон отсутствует", True, (100, 100, 100))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        placeholder.blit(text, text_rect)
        
        return placeholder

    def draw_character(self, character_name, position=None, scale=None):
        """
        Отрисовка персонажа на экране
        
        :param character_name: Имя персонажа
        :param position: Позиция персонажа (left, center, right)
        :param scale: Масштаб персонажа (float)
        """
        try:
            if character_name not in self.characters:
                print(f"Персонаж {character_name} не найден")
                return
                
            character_image = self.characters[character_name]
            
            # Получаем размеры игровой поверхности
            game_width, game_height = self.game_surface.get_size()
            
            # Вычисляем позиции персонажей с учетом размера окна
            character_left = game_width * 0.2
            character_center = game_width * 0.5
            character_right = game_width * 0.8
            
            # Вычисляем позицию персонажа по вертикали
            character_y_position = game_height - TEXT_BOX_HEIGHT - CHARACTER_HEIGHT
            
            # Масштабирование изображения персонажа
            try:
                if scale:
                    original_size = character_image.get_size()
                    new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                    character_image = pygame.transform.scale(character_image, new_size)
                else:
                    # Масштабируем персонажа по высоте
                    original_size = character_image.get_size()
                    height_ratio = CHARACTER_HEIGHT / original_size[1]
                    new_width = int(original_size[0] * height_ratio)
                    character_image = pygame.transform.scale(character_image, (new_width, CHARACTER_HEIGHT))
            except pygame.error as e:
                print(f"Ошибка при масштабировании изображения персонажа {character_name}: {e}")
                return
            
            # Определение позиции персонажа
            character_width = character_image.get_width()
            if position == "left" or position == "l":
                x_position = character_left - character_width // 2
            elif position == "right" or position == "r":
                x_position = character_right - character_width // 2
            else:  # По умолчанию по центру
                x_position = character_center - character_width // 2
            
            # Отрисовка персонажа
            self.game_surface.blit(character_image, (x_position, character_y_position))
        except Exception as e:
            print(f"Ошибка при отрисовке персонажа {character_name}: {e}")
    
    def draw_text_box(self, current_scene):
        """
        Отрисовка текстового окна и текста диалога
        
        :param current_scene: Текущая сцена
        """
        try:
            # Получаем размеры игровой поверхности
            game_width, game_height = self.game_surface.get_size()
            
            text_box_y = game_height - TEXT_BOX_HEIGHT
            
            # Создаем полупрозрачную поверхность для текстового окна
            text_box_surface = pygame.Surface((game_width, TEXT_BOX_HEIGHT), pygame.SRCALPHA)
            text_box_surface.fill(TEXT_BOX_COLOR)
            self.game_surface.blit(text_box_surface, (0, text_box_y))
            
            # Внутренняя часть текстового окна
            pygame.draw.rect(self.game_surface, WHITE, 
                            (TEXT_BOX_PADDING, 
                            text_box_y + TEXT_BOX_PADDING, 
                            game_width - 2*TEXT_BOX_PADDING, 
                            TEXT_BOX_HEIGHT - 2*TEXT_BOX_PADDING))
            
            # Отрисовка имени персонажа
            name_height = 0
            if current_scene.character_name:
                try:
                    name_surface = self.name_font.render(current_scene.character_name, True, BLUE)
                    name_rect = name_surface.get_rect(topleft=(20, text_box_y + 15))
                    self.game_surface.blit(name_surface, name_rect)
                    name_height = name_rect.height + 10
                except pygame.error as e:
                    print(f"Error rendering character name: {e}")
            
            # Рассчитываем ширину текстовой области с учетом размера окна
            text_area_width = game_width - 2 * (BUTTON_WIDTH + 2 * BUTTON_PADDING)
            
            # Разбиваем текст на слова
            words = current_scene.text.split()
            lines = []
            current_line = []
            current_width = 0
            
            # Рассчитываем отступ слева для текста, чтобы не перекрывать кнопку "Назад"
            left_margin = BUTTON_WIDTH + 2 * BUTTON_PADDING
            
            for word in words:
                # Проверяем, не слишком ли длинное слово
                word_surface = self.font.render(word + " ", True, BLACK)
                word_width = word_surface.get_width()
                
                # Если слово слишком длинное, разбиваем его
                if word_width > text_area_width:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = []
                        current_width = 0
                    
                    # Разбиваем длинное слово на части
                    chars = list(word)
                    part = ""
                    for char in chars:
                        test_part = part + char
                        test_surface = self.font.render(test_part + " ", True, BLACK)
                        if test_surface.get_width() <= text_area_width:
                            part = test_part
                        else:
                            if part:
                                lines.append(part)
                            part = char
                    if part:
                        current_line = [part]
                        current_width = self.font.render(part + " ", True, BLACK).get_width()
                else:
                    if current_width + word_width <= text_area_width:
                        current_line.append(word)
                        current_width += word_width
                    else:
                        if current_line:
                            lines.append(" ".join(current_line))
                        current_line = [word]
                        current_width = word_width
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Ограничиваем количество строк
            lines = lines[:MAX_TEXT_LINES]
            
            # Отрисовка текста
            text_start_y = text_box_y + TEXT_BOX_PADDING + name_height
            for i, line in enumerate(lines):
                try:
                    text_surface = self.font.render(line, True, BLACK)
                    text_rect = text_surface.get_rect(
                        topleft=(left_margin, 
                                text_start_y + i * (self.font.get_height() + TEXT_LINE_SPACING))
                    )
                    self.game_surface.blit(text_surface, text_rect)
                except pygame.error as e:
                    print(f"Error rendering text line: {e}")
        except Exception as e:
            print(f"Error drawing text box: {e}")
    
    def draw_navigation_buttons(self):
        """
        Отрисовка кнопок навигации
        """
        # Получаем размеры игровой поверхности
        game_width, game_height = self.game_surface.get_size()
        
        # Вычисляем позицию кнопок
        button_y = game_height - TEXT_BOX_HEIGHT // 2 - BUTTON_HEIGHT // 2
        
        # Кнопка "Назад"
        back_button = pygame.Rect(BUTTON_PADDING, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.game_surface, GRAY if self.current_scene > 0 else DARK_GRAY, back_button)
        pygame.draw.rect(self.game_surface, BLACK, back_button, 2)
        
        back_text = self.button_font.render("Назад", True, BLACK)
        back_rect = back_text.get_rect(center=back_button.center)
        self.game_surface.blit(back_text, back_rect)
        
        # Кнопка "Вперед"
        forward_button = pygame.Rect(game_width - BUTTON_WIDTH - BUTTON_PADDING, 
                                   button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.game_surface, GRAY if self.current_scene < len(self.scenes) - 1 else DARK_GRAY, 
                       forward_button)
        pygame.draw.rect(self.game_surface, BLACK, forward_button, 2)
        
        forward_text = self.button_font.render("Вперед", True, BLACK)
        forward_rect = forward_text.get_rect(center=forward_button.center)
        self.game_surface.blit(forward_text, forward_rect)
        
        self.back_button = back_button
        self.forward_button = forward_button

    def handle_navigation(self, pos):
        """
        Обработка нажатий на кнопки навигации
        
        :param pos: Позиция клика мыши (x, y)
        :return: True, если клик был по кнопке навигации, иначе False
        """
        if self.back_button.collidepoint(pos) and self.current_scene > 0:
            self.current_scene -= 1
            return True
        elif self.forward_button.collidepoint(pos) and self.current_scene < len(self.scenes) - 1:
            current_scene = self.scenes[self.current_scene]
            # Проверяем, есть ли у текущей сцены варианты выбора
            if current_scene.has_choices():
                # Если есть, показываем диалог с выбором
                self.showing_choices = True
                self.choice_buttons = self.draw_choices(current_scene.choices)
                return True
            else:
                # Проверяем, есть ли у текущей сцены идентификатор следующей сцены
                if current_scene.next_scene_id:
                    # Если есть, переходим к указанной сцене
                    self.go_to_scene(current_scene.next_scene_id)
                    return True
                else:
                    # Если нет, переходим к следующей сцене по порядку
                    self.current_scene += 1
                    return True
        return False

    def draw_confirmation_dialog(self):
        """
        Отрисовка диалогового окна подтверждения выхода
        """
        # Получаем размеры игровой поверхности
        game_width, game_height = self.game_surface.get_size()
        
        # Затемнение фона
        overlay = pygame.Surface((game_width, game_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.game_surface.blit(overlay, (0, 0))
        
        # Окно диалога
        dialog_width = 400
        dialog_height = 150
        dialog_x = (game_width - dialog_width) // 2
        dialog_y = (game_height - dialog_height) // 2
        
        # Фон диалога
        pygame.draw.rect(self.game_surface, WHITE, 
                        (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.game_surface, BLACK, 
                        (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Текст
        text = self.font.render("Вы хотите выйти из игры?", True, BLACK)
        text_rect = text.get_rect(center=(game_width // 2, dialog_y + 40))
        self.game_surface.blit(text, text_rect)
        
        # Кнопки
        button_width = 100
        button_height = 40
        padding = 20
        
        # Кнопка "Да"
        yes_button = pygame.Rect(dialog_x + padding, 
                               dialog_y + dialog_height - button_height - padding,
                               button_width, button_height)
        pygame.draw.rect(self.game_surface, GRAY, yes_button)
        yes_text = self.button_font.render("Да", True, BLACK)
        yes_rect = yes_text.get_rect(center=yes_button.center)
        self.game_surface.blit(yes_text, yes_rect)
        
        # Кнопка "Нет"
        no_button = pygame.Rect(dialog_x + dialog_width - button_width - padding,
                              dialog_y + dialog_height - button_height - padding,
                              button_width, button_height)
        pygame.draw.rect(self.game_surface, GRAY, no_button)
        no_text = self.button_font.render("Нет", True, BLACK)
        no_rect = no_text.get_rect(center=no_button.center)
        self.game_surface.blit(no_text, no_rect)
        
        return yes_button, no_button

    def toggle_fullscreen(self):
        """
        Переключение между оконным и полноэкранным режимами
        """
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # Сохраняем текущие размеры окна
            if not pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                self.window_width = pygame.display.get_surface().get_width()
                self.window_height = pygame.display.get_surface().get_height()
            
            # Получаем информацию о текущем дисплее
            display_info = pygame.display.Info()
            screen_width = display_info.current_w
            screen_height = display_info.current_h
            
            # Переключаемся в полноэкранный режим
            self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
            print(f"Переключение в полноэкранный режим: {screen_width}x{screen_height}")
            
            # Обновляем размеры игровой поверхности
            self.game_surface = pygame.Surface((screen_width, screen_height))
        else:
            # Возвращаемся в оконный режим
            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            print(f"Возврат в оконный режим: {self.window_width}x{self.window_height}")
            
            # Обновляем размеры игровой поверхности
            self.game_surface = pygame.Surface((self.window_width, self.window_height))
        
        # Перемасштабируем все фоны
        self.rescale_all_backgrounds()

    def rescale_all_backgrounds(self):
        """
        Перемасштабирует все фоновые изображения при изменении размера окна
        """
        for name, original_bg in self.original_backgrounds.items():
            self.backgrounds[name] = self.scale_background(original_bg)

    def scale_to_screen(self):
        """
        Масштабирует игровую поверхность на весь экран
        """
        # Всегда обновляем параметры масштабирования
        self.update_scale_params()
            
        scaled_width = self.scale_params['scaled_width']
        scaled_height = self.scale_params['scaled_height']
        pos_x = self.scale_params['pos_x']
        pos_y = self.scale_params['pos_y']
        
        # Масштабируем игровую поверхность
        scaled_surface = pygame.transform.smoothscale(self.game_surface, (scaled_width, scaled_height))
        
        # Очищаем экран
        self.screen.fill((0, 0, 0))
        
        # Отображаем масштабированную поверхность
        self.screen.blit(scaled_surface, (pos_x, pos_y))

    def run(self):
        """
        Основной игровой цикл
        """
        show_exit_dialog = False
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show_exit_dialog = True
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                        self.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE and not self.is_fullscreen:
                    # Обновляем размеры окна при изменении размера
                    self.window_width = event.w
                    self.window_height = event.h
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    print(f"Изменение размера окна: {event.w}x{event.h}")
                    
                    # Обновляем размеры игровой поверхности
                    self.game_surface = pygame.Surface((event.w, event.h))
                    
                    # Перемасштабируем все фоны
                    self.rescale_all_backgrounds()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Обрабатываем клики мыши напрямую, без преобразования координат
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if show_exit_dialog:
                        yes_button, no_button = self.draw_confirmation_dialog()
                        if yes_button.collidepoint(mouse_pos):
                            self.running = False
                        elif no_button.collidepoint(mouse_pos):
                            show_exit_dialog = False
                    elif self.showing_choices:
                        # Обработка выбора
                        self.handle_choice(mouse_pos)
                    else:
                        # Обработка навигации
                        if not self.handle_navigation(mouse_pos):
                            # Если клик не по кнопкам и у текущей сцены есть выбор, показываем его
                            current_scene = self.scenes[self.current_scene]
                            if current_scene.has_choices():
                                self.showing_choices = True
                                self.choice_buttons = self.draw_choices(current_scene.choices)
                            # Иначе переходим к следующей сцене
                            elif current_scene.next_scene_id:
                                # Если у сцены есть идентификатор следующей сцены, переходим к ней
                                self.go_to_scene(current_scene.next_scene_id)
                            elif self.current_scene < len(self.scenes) - 1:
                                self.current_scene += 1
                    
            if self.current_scene < len(self.scenes):
                current_scene = self.scenes[self.current_scene]
                
                # Рендерим на игровую поверхность
                self.game_surface.fill(WHITE)
                
                # Отрисовка фона
                if current_scene.background in self.backgrounds:
                    self.game_surface.blit(self.backgrounds[current_scene.background], (0, 0))
                
                # Отрисовка персонажей
                if current_scene.character in self.characters:
                    self.draw_character(current_scene.character, 
                                     current_scene.character_position, 
                                     current_scene.character_scale)
                
                # Отрисовка текстового окна и текста
                self.draw_text_box(current_scene)
                
                # Отрисовка кнопок навигации
                if not self.showing_choices:
                    self.draw_navigation_buttons()
                
                # Отрисовка диалога подтверждения выхода, если нужно
                if show_exit_dialog:
                    self.draw_confirmation_dialog()
                
                # Отрисовка вариантов выбора, если нужно
                if self.showing_choices:
                    self.choice_buttons = self.draw_choices(current_scene.choices)
                
                # Отображаем игровую поверхность на экране
                self.screen.blit(self.game_surface, (0, 0))
                
            pygame.display.flip()
            clock.tick(60)  # Ограничиваем FPS до 60
            
        pygame.quit()
        sys.exit()
        
    def screen_to_game_coordinates(self, screen_pos):
        """
        Преобразует координаты экрана в координаты игровой поверхности
        
        :param screen_pos: Координаты на экране (x, y)
        :return: Координаты на игровой поверхности (x, y)
        """
        # Обновляем параметры масштабирования, если они не установлены
        if not hasattr(self, 'scale_params'):
            self.update_scale_params()
            
        x, y = screen_pos
        pos_x = self.scale_params['pos_x']
        pos_y = self.scale_params['pos_y']
        scaled_width = self.scale_params['scaled_width']
        scaled_height = self.scale_params['scaled_height']
        
        # Проверяем, находится ли точка в пределах масштабированной поверхности
        if (x < pos_x or x >= pos_x + scaled_width or 
            y < pos_y or y >= pos_y + scaled_height):
            return (-1, -1)  # Точка вне игровой области
        
        # Преобразуем координаты
        game_x = int((x - pos_x) * WINDOW_WIDTH / scaled_width)
        game_y = int((y - pos_y) * WINDOW_HEIGHT / scaled_height)
        
        return (game_x, game_y)
        
    def create_default_background(self, name="bg_room"):
        """
        Создает фоновое изображение по умолчанию, если оно не существует
        
        :param name: Имя фона
        :return: Путь к созданному изображению
        """
        image_path = f"{BACKGROUNDS_PATH}{name}.png"
        
        # Проверяем, существует ли директория для фонов
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Если файл уже существует, просто возвращаем путь
        if os.path.exists(image_path):
            return image_path
        
        # Создаем простой фон в зависимости от имени
        bg_surface = pygame.Surface((1280, 720))  # Создаем с большим разрешением для лучшего качества
        
        if "room" in name.lower():
            # Комната
            bg_surface.fill((220, 220, 240))  # Светло-голубой фон для стен
            pygame.draw.rect(bg_surface, (180, 150, 100), (0, 500, 1280, 220))  # Пол
            pygame.draw.rect(bg_surface, (150, 150, 150), (500, 150, 300, 350))  # Окно
            pygame.draw.rect(bg_surface, (120, 120, 120), (500, 150, 300, 350), 10)  # Рама окна
        elif "lab" in name.lower():
            # Лаборатория
            bg_surface.fill((240, 240, 240))  # Белый фон для стен
            pygame.draw.rect(bg_surface, (200, 200, 200), (0, 500, 1280, 220))  # Пол
            # Лабораторное оборудование
            for i in range(3):
                pygame.draw.rect(bg_surface, (100, 100, 120), (100 + i*400, 200, 200, 300))  # Шкафы
                pygame.draw.rect(bg_surface, (80, 80, 100), (100 + i*400, 200, 200, 300), 5)  # Контуры шкафов
        elif "manufacture" in name.lower():
            # Производственная зона
            bg_surface.fill((200, 200, 200))  # Серый фон для стен
            pygame.draw.rect(bg_surface, (100, 100, 100), (0, 500, 1280, 220))  # Пол
            # Оборудование
            pygame.draw.rect(bg_surface, (80, 80, 80), (200, 300, 400, 200))  # Станок
            pygame.draw.rect(bg_surface, (80, 80, 80), (700, 300, 300, 200))  # Станок 2
        elif "music" in name.lower():
            # Музыкальный класс
            bg_surface.fill((250, 240, 230))  # Теплый фон для стен
            pygame.draw.rect(bg_surface, (180, 160, 140), (0, 500, 1280, 220))  # Деревянный пол
            # Музыкальные инструменты
            pygame.draw.ellipse(bg_surface, (60, 40, 20), (300, 200, 300, 400))  # Пианино
            pygame.draw.rect(bg_surface, (60, 40, 20), (700, 300, 200, 200))  # Шкаф с нотами
        elif "residential" in name.lower():
            # Жилая зона
            bg_surface.fill((240, 230, 220))  # Теплый фон для стен
            pygame.draw.rect(bg_surface, (180, 150, 120), (0, 500, 1280, 220))  # Деревянный пол
            # Мебель
            pygame.draw.rect(bg_surface, (150, 120, 90), (200, 300, 400, 200))  # Диван
            pygame.draw.rect(bg_surface, (140, 110, 80), (700, 350, 150, 150))  # Стол
        else:
            # Общий фон по умолчанию
            bg_surface.fill((220, 220, 240))  # Светло-голубой фон
            pygame.draw.rect(bg_surface, (180, 150, 100), (0, 500, 1280, 220))  # Пол
        
        try:
            pygame.image.save(bg_surface, image_path)
            print(f"Создан фон по умолчанию: {name}")
        except Exception as e:
            print(f"Ошибка при создании фона {name}: {e}")
        
        return image_path

    def update_scale_params(self):
        """
        Обновляет параметры масштабирования на основе текущего размера экрана
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Вычисляем соотношение сторон
        game_ratio = WINDOW_WIDTH / WINDOW_HEIGHT
        screen_ratio = screen_width / screen_height
        
        if screen_ratio > game_ratio:
            # Экран шире, чем игра
            scaled_height = screen_height
            scaled_width = int(scaled_height * game_ratio)
        else:
            # Экран уже, чем игра
            scaled_width = screen_width
            scaled_height = int(scaled_width / game_ratio)
        
        # Вычисляем позицию для центрирования
        pos_x = (screen_width - scaled_width) // 2
        pos_y = (screen_height - scaled_height) // 2
        
        # Сохраняем параметры масштабирования
        self.scale_params = {
            'scaled_width': scaled_width,
            'scaled_height': scaled_height,
            'pos_x': pos_x,
            'pos_y': pos_y
        }
        
        print(f"Обновлены параметры масштабирования: {self.scale_params}") 

    def go_to_scene(self, scene_id):
        """
        Переход к сцене по её ID
        
        :param scene_id: ID сцены
        :return: True, если переход выполнен успешно, иначе False
        """
        if scene_id in self.scene_map:
            self.current_scene = self.scene_map[scene_id]
            self.showing_choices = False
            self.choice_buttons = []
            
            # Выполняем действия при входе в сцену
            current_scene = self.scenes[self.current_scene]
            for action in current_scene.on_enter:
                action_type = action.get("action")
                if action_type == "set_variable":
                    self.set_variable(action["variable"], action["value"])
                    
            return True
        return False
        
    def draw_choices(self, choices):
        """
        Отрисовка вариантов выбора
        
        :param choices: Список вариантов выбора
        :return: Список прямоугольников кнопок выбора
        """
        # Фильтруем выборы по условиям
        filtered_choices = []
        for choice in choices:
            condition = choice.get("condition")
            if not condition or self.check_condition(condition):
                filtered_choices.append(choice)
        
        # Если нет доступных выборов, возвращаем пустой список
        if not filtered_choices:
            return []
        
        # Получаем размеры игровой поверхности
        game_width, game_height = self.game_surface.get_size()
        
        # Параметры кнопок выбора
        choice_width = game_width * 0.8
        choice_height = 50
        choice_padding = 10
        
        # Вычисляем общую высоту всех кнопок
        total_height = len(filtered_choices) * (choice_height + choice_padding) - choice_padding
        
        # Начальная позиция Y для первой кнопки
        start_y = (game_height - total_height) // 2
        
        # Создаем затемнение фона
        overlay = pygame.Surface((game_width, game_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # Полупрозрачный черный
        self.game_surface.blit(overlay, (0, 0))
        
        # Отрисовываем кнопки выбора
        choice_buttons = []
        for i, choice in enumerate(filtered_choices):
            # Вычисляем позицию кнопки
            button_x = (game_width - choice_width) // 2
            button_y = start_y + i * (choice_height + choice_padding)
            
            # Создаем прямоугольник кнопки
            button_rect = pygame.Rect(button_x, button_y, choice_width, choice_height)
            
            # Отрисовываем кнопку
            pygame.draw.rect(self.game_surface, (200, 200, 200), button_rect)
            pygame.draw.rect(self.game_surface, (0, 0, 0), button_rect, 2)
            
            # Отрисовываем текст кнопки
            text_surface = self.font.render(choice["text"], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.game_surface.blit(text_surface, text_rect)
            
            # Добавляем кнопку в список
            choice_buttons.append((button_rect, choice["next_scene"]))
        
        return choice_buttons
        
    def handle_choice(self, pos):
        """
        Обработка клика по варианту выбора
        
        :param pos: Позиция клика (x, y)
        :return: True, если клик был по варианту выбора, иначе False
        """
        for button, next_scene in self.choice_buttons:
            if button.collidepoint(pos):
                self.go_to_scene(next_scene)
                return True
        return False
        
    def set_variable(self, name, value):
        """
        Устанавливает значение переменной
        
        :param name: Имя переменной
        :param value: Значение переменной
        """
        self.variables[name] = value
        
    def get_variable(self, name, default=None):
        """
        Возвращает значение переменной
        
        :param name: Имя переменной
        :param default: Значение по умолчанию, если переменная не существует
        :return: Значение переменной или значение по умолчанию
        """
        return self.variables.get(name, default)
        
    def check_condition(self, condition):
        """
        Проверяет условие
        
        :param condition: Словарь с условием в формате {"variable": "имя_переменной", "value": значение}
        :return: True, если условие выполняется, иначе False
        """
        if not condition:
            return True
            
        # Проверка на оператор "and"
        if "and" in condition:
            sub_conditions = condition["and"]
            for sub_condition in sub_conditions:
                if not self.check_condition(sub_condition):
                    return False
            # Проверяем основное условие, если оно есть
            if "variable" in condition:
                temp_condition = condition.copy()
                del temp_condition["and"]
                if not self.check_condition(temp_condition):
                    return False
            return True
            
        # Проверка на оператор "or"
        if "or" in condition:
            sub_conditions = condition["or"]
            for sub_condition in sub_conditions:
                if self.check_condition(sub_condition):
                    return True
            # Проверяем основное условие, если оно есть
            if "variable" in condition:
                temp_condition = condition.copy()
                del temp_condition["or"]
                if self.check_condition(temp_condition):
                    return True
            return False
            
        variable_name = condition.get("variable")
        
        if variable_name is None:
            return True
            
        actual_value = self.get_variable(variable_name)
        
        # Проверка на равенство
        if "equals" in condition:
            return actual_value == condition["equals"]
            
        # Проверка на неравенство
        if "not_equals" in condition:
            return actual_value != condition["not_equals"]
            
        # Проверка на больше
        if "greater_than" in condition:
            return actual_value > condition["greater_than"]
            
        # Проверка на меньше
        if "less_than" in condition:
            return actual_value < condition["less_than"]
            
        # Проверка на наличие в списке
        if "in" in condition:
            return actual_value in condition["in"]
            
        # Проверка на отсутствие в списке
        if "not_in" in condition:
            return actual_value not in condition["not_in"]
            
        # По умолчанию проверяем на равенство expected_value
        expected_value = condition.get("value")
        return actual_value == expected_value 