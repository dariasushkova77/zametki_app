# models/note.py - создаем
class Note:
    """Класс заметки - хранит данные одной заметки"""

    def __init__(self, title, content=""):
        self.title = title  # Заголовок заметки
        self.content = content  # Содержимое заметки
        self.created_at = None  # Дата создания (будет добавлена позже)

    def to_dict(self):
        """Преобразует заметку в словарь для сохранения"""
        return {
            "title": self.title,
            "content": self.content
        }