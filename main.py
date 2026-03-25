# main.py - точка входа
from gui.main_window import MainWindow

def main():
    """Главная функция приложения"""
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()