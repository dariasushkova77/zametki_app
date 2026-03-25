# services/note_manager.py
class NoteManager:
    """Управляет коллекцией заметок"""

    def __init__(self):
        self.notes = []  # Список заметок

    def add_note(self, note):
        """Добавляет заметку"""
        self.notes.append(note)
        return True

    def delete_note(self, index):
        """Удаляет заметку по индексу"""
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return True
        return False

    def get_notes(self):
        """Возвращает все заметки"""
        return self.notes

    def update_note(self, index, title, content):
        """Обновляет заметку"""
        if 0 <= index < len(self.notes):
            self.notes[index].title = title
            self.notes[index].content = content
            return True
        return False