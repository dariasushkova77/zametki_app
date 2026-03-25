import tkinter as tk
from tkinter import messagebox


class NoteDialog:
    """Диалоговое окно для создания/редактирования заметки"""

    def __init__(self, parent, title="", content=""):
        self.result = None

        # Создаем окно
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Новая заметка")
        self.dialog.geometry("400x350")

        # Делаем окно модальным
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Заголовок
        tk.Label(self.dialog, text="Заголовок:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))

        # Поле для заголовка
        self.title_entry = tk.Entry(self.dialog, font=('Arial', 12), width=40)
        self.title_entry.insert(0, title)
        self.title_entry.pack(pady=(0, 10), padx=20, fill=tk.X)

        # Содержимое
        tk.Label(self.dialog, text="Содержимое:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))

        # Текстовое поле
        self.text_widget = tk.Text(self.dialog, height=10, font=('Arial', 11), wrap=tk.WORD)
        self.text_widget.insert(1.0, content)
        self.text_widget.pack(pady=(0, 10), padx=20, fill=tk.BOTH, expand=True)

        # Кнопки
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)

        save_btn = tk.Button(button_frame, text="Сохранить", command=self.save,
                             bg="#4CAF50", fg="white", padx=20)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(button_frame, text="Отмена", command=self.cancel,
                               bg="#f44336", fg="white", padx=20)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Устанавливаем фокус
        self.dialog.after(100, self.set_focus)

        # Обработка клавиш
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        self.dialog.wait_window()

    def set_focus(self):
        """Устанавливает фокус на поле заголовка"""
        self.title_entry.focus_set()
        self.title_entry.icursor(tk.END)

    def save(self):
        """Сохраняет заметку"""
        title = self.title_entry.get().strip()
        content = self.text_widget.get(1.0, tk.END).strip()

        if title:
            self.result = (title, content)
            self.dialog.destroy()
        else:
            messagebox.showwarning("Ошибка", "Введите заголовок заметки!", parent=self.dialog)

    def cancel(self):
        """Закрывает окно"""
        self.dialog.destroy()