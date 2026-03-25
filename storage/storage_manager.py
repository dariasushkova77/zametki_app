# storage/storage_manager.py
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
            data = [note.to_dict() for note in notes]
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

            # Преобразуем словари обратно в объекты Note
            from models.note import Note
            notes = []
            for item in data:
                note = Note(item['title'], item['content'])
                notes.append(note)
            return notes
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return []