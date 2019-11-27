"""
        GameScreen must define Game-related GUI elements and handle keyboard input (not webcam gesture detection)
"""

from src.screen import Screen
from src.game import Game
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from src.screen_manager import ScreenManager


class GameScreen(Game, Screen):  # GameScreen inherits from both Screen and Game

    def __init__(self):
        super(GameScreen, self).__init__()  # calling all parent constructors

    def show(self):  # implementing abstract method from Screen
        # TODO: Implement this
        #app = QApplication([])
        window = QWidget()
        layout = QVBoxLayout()
        button = QPushButton("Bottom")
        button2 = QPushButton("Top")
        layout.addWidget(button2)
        layout.addWidget(button)
        button.clicked.connect(lambda:ScreenManager.change_screen(1)) # clicked.connect expects a callable function, we use lambda because ScreenManager is an abstract class
        window.setLayout(layout)
        window.show()
        #app.exec_()

    def button_press(self, button):  # implementing abstract method from Screen
        # if "q" is pressed, stop the game, otherwise start it
        if button != "q":
            if self.hasFinished:
                self.start()
        else:
            self.stop()
