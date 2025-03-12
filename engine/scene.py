class Scene:
    """
    Класс для представления сцены в визуальной новелле.
    Содержит текст, информацию о персонаже и фоне.
    """
    def __init__(self, text, character=None, background=None, character_position=None, 
                 character_scale=None, character_name=None, choices=None, scene_id=None, next_scene_id=None,
                 on_enter=None):
        """
        Инициализация сцены.
        
        :param text: Текст диалога
        :param character: Имя персонажа в словаре персонажей
        :param background: Имя фона в словаре фонов
        :param character_position: Позиция персонажа (left, center, right)
        :param character_scale: Масштаб персонажа (float)
        :param character_name: Отображаемое имя персонажа (если отличается от ключа)
        :param choices: Список вариантов выбора в формате [{"text": "Текст варианта", "next_scene": id_сцены, "condition": {...}}, ...]
        :param scene_id: Уникальный идентификатор сцены для переходов
        :param next_scene_id: Идентификатор следующей сцены для автоматического перехода
        :param on_enter: Список действий, выполняемых при входе в сцену, например [{"action": "set_variable", "variable": "visited_lab", "value": True}]
        """
        self.text = text
        self.character = character
        self.background = background
        self.character_position = character_position
        self.character_scale = character_scale
        self.character_name = character_name if character_name else character
        self.choices = choices or []
        self.scene_id = scene_id
        self.next_scene_id = next_scene_id
        self.on_enter = on_enter or []
        
    def add_choice(self, text, next_scene, condition=None):
        """
        Добавляет вариант выбора к сцене
        
        :param text: Текст варианта выбора
        :param next_scene: ID сцены, к которой ведет этот выбор
        :param condition: Условие для отображения варианта выбора
        """
        if self.choices is None:
            self.choices = []
        self.choices.append({"text": text, "next_scene": next_scene, "condition": condition})
        
    def has_choices(self):
        """
        Проверяет, есть ли у сцены варианты выбора
        
        :return: True, если есть варианты выбора, иначе False
        """
        return bool(self.choices)
        
    def get_filtered_choices(self, game):
        """
        Возвращает список вариантов выбора, отфильтрованный по условиям
        
        :param game: Экземпляр класса Game для проверки условий
        :return: Список вариантов выбора, удовлетворяющих условиям
        """
        if not self.choices:
            return []
            
        filtered_choices = []
        for choice in self.choices:
            condition = choice.get("condition")
            if not condition or game.check_condition(condition):
                filtered_choices.append(choice)
                
        return filtered_choices 