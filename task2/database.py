import json
from typing import List, Optional
from models import Task

class JSONDatabase:
    """Простая JSON-база данных для хранения задач"""
    
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path
        self._init_database()
        print(f"База данных создана: {self.file_path}")  # Для отладки
    
    def _init_database(self):
        """Инициализация файла БД, если его нет"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Создаём новый файл с пустым списком
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _read_data(self) -> list:
        """Чтение всех задач из JSON-файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _write_data(self, data: list):
        """Запись данных в JSON-файл"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_next_id(self) -> int:
        """Генерация следующего ID"""
        tasks = self._read_data()
        if not tasks:
            return 1
        return max(task["id"] for task in tasks) + 1
    
    def get_all_tasks(self) -> List[Task]:
        """Получить все задачи"""
        data = self._read_data()
        return [Task(**task) for task in data]
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Получить задачу по ID"""
        tasks = self._read_data()
        for task in tasks:
            if task["id"] == task_id:
                return Task(**task)
        return None
    
    def add_task(self, title: str, completed: bool = False) -> Task:
        """Добавить новую задачу"""
        new_id = self.get_next_id()
        new_task = Task(id=new_id, title=title, completed=completed)
        
        tasks = self._read_data()
        tasks.append(new_task.dict())
        self._write_data(tasks)
        
        return new_task
    
    def delete_task(self, task_id: int) -> bool:
        """Удалить задачу по ID. Возвращает True если успешно"""
        tasks = self._read_data()
        initial_length = len(tasks)
        
        tasks = [task for task in tasks if task["id"] != task_id]
        
        if len(tasks) == initial_length:
            return False  # Задача не найдена
        
        self._write_data(tasks)
        return True

# Создаём глобальный экземпляр базы данных
db = JSONDatabase()
