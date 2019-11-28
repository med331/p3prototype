from asyncio import sleep
from unittest import TestCase

from PyQt5.QtWidgets import QApplication

from src.game_screen import GameScreen
from src.screen_manager import ScreenManager
import sys


class TestGameScreen(TestCase):

    def setUp(self) -> None:
        self.gs = GameScreen()
        ScreenManager._screens = [self.gs]

    def test_show(self):
        app = QApplication([sys.argv])
        ScreenManager.show_active_screen()
        sys.exit(app.exec_())

    def test_button_press(self):
        # TODO: write this test
        pass
