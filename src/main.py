from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from src.game_screen import GameScreen
from src.settings_screen import SettingsScreen
from src.screen_manager import ScreenManager


gs = GameScreen()
ss = SettingsScreen()
ScreenManager._screens = [gs, ss]
ScreenManager.change_screen(0)

if __name__ == "__main__":
    app = QApplication([])
    ScreenManager.show_active_screen()
    app.exec_()
