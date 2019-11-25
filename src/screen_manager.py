"""
        ScreenManager is currently (almost) fully implemented
"""

from src.game_screen import GameScreen


class ScreenManager:

    def __init__(self):
        self._screens = [GameScreen()]  # TODO: add more screens here
        self._activeScreenIndex = 0

    def change_screen(self, index):
        self._activeScreenIndex = index

    def button_press(self, button):
        self._screens[self._activeScreenIndex].button_press(button)

    def show_active_screen(self):
        self._screens[self._activeScreenIndex].show()
