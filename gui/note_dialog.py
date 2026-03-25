import tkinter as tk
from tkinter import messagebox


class NoteDialog:
    """Диалоговое окно для создания/редактирования заметки"""

    def __init__(self, parent, title="", content=""):
        self.result = None

        dialog = tk.Toplevel(parent)
        dialog.title("Заметка")
        dialog.geometry("350x300")

        tk.Label(dialog, text="Заголовок:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.entry_title = tk.Entry(dialog, font=('Arial', 11))
        self.entry_title.insert(0, title)
        self.entry_title.pack(fill=tk.X, padx=10)

        tk.Label(dialog, text="Содержимое:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.text_content = tk.Text(dialog, height=8, font=('Arial', 10))
        self.text_content.insert(1.0, content)
        self.text_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Сохранить", command=lambda: self.save(dialog),
                  bg="#4CAF50", fg="white", padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy,
                  bg="#f44336", fg="white", padx=20).pack(side=tk.LEFT, padx=5)

        dialog.transient(parent)
        dialog.grab_set()
        dialog.wait_window()

    def save(self, dialog):
        title = self.entry_title.get().strip()
        content = self.text_content.get(1.0, tk.END).strip()

        if title:
            self.result = (title, content)
            dialog.destroy()
        else:
            messagebox.showwarning("Ошибка", "Введите заголовок!")