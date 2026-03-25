import tkinter as tk
from tkinter import messagebox
from models.note import Note
from services.note_manager import NoteManager
from storage.storage_manager import StorageManager
from qui.note_dialog import NoteDialog  # Обратите внимание: qui, не gui


class MainWindow:
    """Главное окно приложения"""

    def __init__(self):
        # Инициализация менеджеров
        self.manager = NoteManager()
        self.storage = StorageManager()

        # Загружаем сохраненные заметки
        self.load_notes()

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Мои заметки")
        self.root.geometry("600x450")

        # Создаем интерфейс
        self.create_menu()
        self.create_widgets()

    def load_notes(self):
        """Загружает заметки из файла"""
        try:
            notes_data = self.storage.load()
            print(f"Загружено записей: {len(notes_data)}")  # Отладка

            for item in notes_data:
                # Проверяем тип данных
                if isinstance(item, dict):
                    # Если это словарь из JSON
                    title = item.get('title', 'Без названия')
                    content = item.get('content', '')
                    note = Note(title, content)
                elif isinstance(item, Note):
                    # Если это уже объект Note
                    note = item
                else:
                    print(f"Неизвестный тип: {type(item)}")
                    continue

                self.manager.add_note(note)

            print(f"Загружено заметок: {len(self.manager.get_notes())}")  # Отладка

        except Exception as e:
            print(f"Ошибка загрузки: {e}")

    def save_notes(self):
        """Сохраняет заметки в файл"""
        try:
            self.storage.save(self.manager.get_notes())
            print("Заметки сохранены")  # Отладка
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def create_menu(self):
        """Создает меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая заметка", command=self.add_note, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        self.root.bind('<Control-n>', lambda e: self.add_note())

    def create_widgets(self):
        """Создает элементы интерфейса"""

        # Панель инструментов
        toolbar = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, bd=1)
        toolbar.pack(fill=tk.X)

        self.btn_add = tk.Button(toolbar, text="➕ Добавить", command=self.add_note,
                                 bg="#f0f0f0", relief=tk.FLAT, padx=10)
        self.btn_add.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_edit = tk.Button(toolbar, text="✏️ Редактировать", command=self.edit_note,
                                  bg="#f0f0f0", relief=tk.FLAT, padx=10)
        self.btn_edit.pack(side=tk.LEFT, padx=2, pady=2)

        self.btn_delete = tk.Button(toolbar, text="🗑️ Удалить", command=self.delete_note,
                                    bg="#f0f0f0", relief=tk.FLAT, padx=10)
        self.btn_delete.pack(side=tk.LEFT, padx=2, pady=2)

        # Основной контейнер
        main_panel = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True)

        # Левая панель - список заметок
        left_frame = tk.Frame(main_panel)
        main_panel.add(left_frame, width=200)

        tk.Label(left_frame, text="Список заметок", font=('Arial', 10, 'bold')).pack(pady=5)

        scrollbar = tk.Scrollbar(left_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(left_frame, font=('Arial', 10),
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Правая панель - просмотр
        right_frame = tk.Frame(main_panel)
        main_panel.add(right_frame, width=350)

        tk.Label(right_frame, text="Содержимое заметки", font=('Arial', 10, 'bold')).pack(pady=5)

        self.text_content = tk.Text(right_frame, wrap=tk.WORD, font=('Arial', 10))
        self.text_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text_content.config(state=tk.DISABLED)

        self.update_list()

    def update_list(self):
        """Обновляет список заметок"""
        self.listbox.delete(0, tk.END)
        for note in self.manager.get_notes():
            self.listbox.insert(tk.END, note.title)

    def update_content(self):
        """Обновляет область просмотра содержимого"""
        selection = self.listbox.curselection()
        self.text_content.config(state=tk.NORMAL)
        self.text_content.delete(1.0, tk.END)

        if selection:
            index = selection[0]
            note = self.manager.get_notes()[index]
            content = f"📝 {note.title}\n\n{note.content}"
            self.text_content.insert(1.0, content)
        else:
            self.text_content.insert(1.0, "Выберите заметку для просмотра")

        self.text_content.config(state=tk.DISABLED)

    def on_select(self, event):
        """Обработчик выбора заметки"""
        self.update_content()

    def add_note(self):
        """Добавляет новую заметку"""
        try:
            dialog = NoteDialog(self.root)
            if dialog.result:
                title, content = dialog.result
                note = Note(title, content)
                self.manager.add_note(note)
                self.update_list()
                self.save_notes()
                print(f"Заметка '{title}' добавлена")  # Отладка
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить заметку:\n{e}")

    def edit_note(self):
        """Редактирует выбранную заметку"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Информация", "Выберите заметку для редактирования")
            return

        index = selection[0]
        note = self.manager.get_notes()[index]

        dialog = NoteDialog(self.root, note.title, note.content)
        if dialog.result:
            title, content = dialog.result
            self.manager.update_note(index, title, content)
            self.update_list()
            self.save_notes()
            self.update_content()

    def delete_note(self):
        """Удаляет выбранную заметку"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Информация", "Выберите заметку для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную заметку?"):
            index = selection[0]
            self.manager.delete_note(index)
            self.update_list()
            self.save_notes()
            self.update_content()

    def show_about(self):
        """Показывает информацию о программе"""
        messagebox.showinfo("О программе",
                            "Мои заметки v1.0\n\n"
                            "Простое приложение для ведения заметок\n"
                            "Создано с использованием Python и Tkinter")

    def run(self):
        """Запускает приложение"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """При закрытии окна сохраняем заметки"""
        self.save_notes()
        self.root.destroy()