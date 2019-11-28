"""
        Screen is currently fully implemented
"""
from src.screen_manager import ScreenManager as sm


class Screen:  # abstract class

    @staticmethod
    def change_screen(index):  # forward method from Screen Manager
        sm.change_screen(index)

    def show(self):                  # abstract method
        raise NotImplementedError

    def button_press(self, button):  # abstract method
        raise NotImplementedError
