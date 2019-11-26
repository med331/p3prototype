"""
        ScreenManager is currently (almost) fully implemented
"""


class ScreenManager:

    _screens = []  # TODO: screens must be added manually at runtime
    _activeScreenIndex = 0

    @classmethod
    def change_screen(cls, index):
        cls._activeScreenIndex = index

    @classmethod
    def button_press(cls, button):
        return cls._screens[cls._activeScreenIndex].button_press(button)

    @classmethod
    def show_active_screen(cls):
        return cls._screens[cls._activeScreenIndex].show()
