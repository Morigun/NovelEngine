from engine.scene import Scene
from engine.config import CHARACTERS_PATH, BACKGROUNDS_PATH

def load_story(game):
    """
    Загрузка сюжета игры.
    
    :param game: Экземпляр класса Game
    """
    # Создание фона по умолчанию
    bg_path = game.create_default_background("bg_room")
    bg_lab = game.create_default_background("Laboratory")
    bg_manufacture = game.create_default_background("Manufacturing area")
    bg_music_class = game.create_default_background("Music class")
    bg_residental_area = game.create_default_background("Residential area")
    game.add_background("bg_room", bg_path)
    game.add_background("bg_lab", bg_lab)
    game.add_background("bg_manufacture", bg_manufacture)
    game.add_background("bg_music_class", bg_music_class)
    game.add_background("bg_residental_area", bg_residental_area)
    
    # Загрузка персонажей
    game.add_character("dr_carter", f"{CHARACTERS_PATH}Dr. Carter.png")
    game.add_character("lily", f"{CHARACTERS_PATH}Lily.png")
    game.add_character("ryan", f"{CHARACTERS_PATH}Ryan.png")
    
    # Инициализация переменных
    game.set_variable("visited_music_class", False)
    game.set_variable("visited_manufacturing", False)
    game.set_variable("visited_residential", False)
    
    # Создание сцен
    scenes = [
        # Начальная сцена
        Scene("Добро пожаловать в визуальную новеллу! Это демонстрация работы движка с системой выбора.", 
              background="bg_manufacture",
              scene_id="start",
              next_scene_id="meet_carter"),
              
        # Знакомство с доктором Картером
        Scene("Здравствуйте! Я доктор Картер, руководитель лаборатории. Я занимаюсь исследованиями в области искусственного интеллекта и робототехники.", 
              character="dr_carter", 
              background="bg_lab",
              character_position="center",
              character_name="Доктор Картер",
              scene_id="meet_carter",
              next_scene_id="first_choice"),
              
        # Первый выбор
        Scene("Чем бы вы хотели заняться сегодня?", 
              character="dr_carter", 
              background="bg_lab",
              character_position="center",
              character_name="Доктор Картер",
              scene_id="first_choice",
              choices=[
                  {"text": "Посетить музыкальный класс", "next_scene": "music_class"},
                  {"text": "Осмотреть производственную зону", "next_scene": "manufacturing"},
                  {"text": "Пойти в жилую зону", "next_scene": "residential"},
                  {"text": "Завершить демонстрацию", "next_scene": "end", "condition": {
                      "variable": "visited_music_class",
                      "equals": True,
                      "and": [
                          {"variable": "visited_manufacturing", "equals": True},
                          {"variable": "visited_residential", "equals": True}
                      ]
                  }}
              ]),
              
        # Ветка музыкального класса
        Scene("Вы решили посетить музыкальный класс.", 
              background="bg_music_class",
              scene_id="music_class",
              next_scene_id="lily_intro",
              on_enter=[
                  {"action": "set_variable", "variable": "visited_music_class", "value": True}
              ]),
              
        Scene("А я Лили! Рада познакомиться! Я преподаю музыку и помогаю доктору Картеру в создании алгоритмов для распознавания музыкальных паттернов.", 
              character="lily", 
              background="bg_music_class",
              character_position="right",
              character_name="Лили",
              scene_id="lily_intro",
              next_scene_id="music_choice"),
              
        Scene("Чем бы вы хотели заняться в музыкальном классе?", 
              character="lily", 
              background="bg_music_class",
              character_position="right",
              character_name="Лили",
              scene_id="music_choice",
              choices=[
                  {"text": "Послушать музыку", "next_scene": "listen_music"},
                  {"text": "Узнать больше о проекте", "next_scene": "music_project"},
                  {"text": "Вернуться к доктору Картеру", "next_scene": "meet_carter"}
              ]),
              
        Scene("Вы слушаете прекрасную мелодию, которую играет Лили. Это помогает вам расслабиться.", 
              character="lily", 
              background="bg_music_class",
              character_position="right",
              character_name="Лили",
              scene_id="listen_music",
              next_scene_id="music_choice"),
              
        Scene("Мы работаем над созданием ИИ, который сможет распознавать эмоции в музыке и создавать композиции, вызывающие определенные чувства.", 
              character="lily", 
              background="bg_music_class",
              character_position="right",
              character_name="Лили",
              scene_id="music_project",
              next_scene_id="music_choice"),
              
        # Ветка производственной зоны
        Scene("Вы решили осмотреть производственную зону.", 
              background="bg_manufacture",
              scene_id="manufacturing",
              next_scene_id="ryan_intro",
              on_enter=[
                  {"action": "set_variable", "variable": "visited_manufacturing", "value": True}
              ]),
              
        Scene("Привет всем! Меня зовут Райан. Я работаю над системами машинного обучения и нейронными сетями в нашей лаборатории.", 
              character="ryan", 
              background="bg_manufacture",
              character_position="left",
              character_name="Райан",
              scene_id="ryan_intro",
              next_scene_id="manufacturing_choice"),
              
        Scene("Что вас интересует в производственной зоне?", 
              character="ryan", 
              background="bg_manufacture",
              character_position="left",
              character_name="Райан",
              scene_id="manufacturing_choice",
              choices=[
                  {"text": "Узнать о роботах", "next_scene": "robots"},
                  {"text": "Спросить о нейронных сетях", "next_scene": "neural_networks"},
                  {"text": "Вернуться к доктору Картеру", "next_scene": "meet_carter"}
              ]),
              
        Scene("Мы разрабатываем роботов, которые могут адаптироваться к различным условиям и выполнять сложные задачи.", 
              character="ryan", 
              background="bg_manufacture",
              character_position="left",
              character_name="Райан",
              scene_id="robots",
              next_scene_id="manufacturing_choice"),
              
        Scene("Наши нейронные сети способны обучаться на основе опыта и принимать решения в сложных ситуациях.", 
              character="ryan", 
              background="bg_manufacture",
              character_position="left",
              character_name="Райан",
              scene_id="neural_networks",
              next_scene_id="manufacturing_choice"),
              
        # Ветка жилой зоны
        Scene("Вы решили пойти в жилую зону.", 
              background="bg_residental_area",
              scene_id="residential",
              next_scene_id="residential_info",
              on_enter=[
                  {"action": "set_variable", "variable": "visited_residential", "value": True}
              ]),
              
        Scene("В жилой зоне тихо и спокойно. Здесь сотрудники лаборатории отдыхают после работы.", 
              background="bg_residental_area",
              scene_id="residential_info",
              next_scene_id="residential_choice"),
              
        Scene("Что бы вы хотели сделать в жилой зоне?", 
              background="bg_residental_area",
              scene_id="residential_choice",
              choices=[
                  {"text": "Отдохнуть", "next_scene": "rest"},
                  {"text": "Почитать книгу", "next_scene": "read_book"},
                  {"text": "Вернуться к доктору Картеру", "next_scene": "meet_carter"}
              ]),
              
        Scene("Вы решили отдохнуть. Это помогает вам восстановить силы.", 
              background="bg_residental_area",
              scene_id="rest",
              next_scene_id="residential_choice"),
              
        Scene("Вы нашли интересную книгу о искусственном интеллекте и погрузились в чтение.", 
              background="bg_residental_area",
              scene_id="read_book",
              next_scene_id="residential_choice"),
              
        # Финальная сцена
        Scene("Спасибо за внимание! Вы посетили все локации и ознакомились с возможностями нашего движка визуальных новелл с системой выбора и условиями.", 
              background="bg_manufacture",
              scene_id="end")
    ]
    
    # Добавление сцен в игру
    for scene in scenes:
        game.add_scene(scene) 