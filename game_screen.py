"""
        GameScreen must define Game-related GUI elements and handle keyboard input (not webcam gesture detection)
"""

from screens import Screen
from game import Game


class GameScreen(Screen):

    def __init__(self):
        super(GameScreen, self).__init__()  # calling Screen constructor
        self.game = Game()

    def show(self):  # implementing abstract method from Screen
        # TODO: Implement this
        if self.game.hasFinished:
            print("Game has finished!")
        else:
            print("Game is running!")

    def buttonPress(self, button):  # implementing abstract method from Screen
        # if "q" is pressed, stop the game, otherwise start it
        if button != "q":
            if self.game.hasFinished:
                self.game.start()
        else:
            self.game.stop()
