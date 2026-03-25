import json
import os


class StorageManager:
    """Сохраняет и загружает заметки в JSON файл"""

    def __init__(self, filename="data/notes.json"):
        self.filename = filename
        # Создаем папку data если её нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def save(self, notes):
        """Сохраняет список заметок в файл"""
        try:
            # Преобразуем объекты Note в словари
            data = []
            for note in notes:
                if hasattr(note, 'to_dict'):  # Если есть метод to_dict
                    data.append(note.to_dict())
                elif isinstance(note, dict):  # Если уже словарь
                    data.append(note)
                else:  # Если объект Note
                    data.append({
                        "title": note.title,
                        "content": note.content
                    })

            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False

    def load(self):
        """Загружает заметки из файла"""
        try:
            if not os.path.exists(self.filename):
                return []

            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Возвращаем список словарей
            # НЕ создаем объекты Note здесь
            return data

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return []