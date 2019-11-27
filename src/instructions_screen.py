from src.screen import Screen
from src.game import Game


class InstructionsScreen(Screen):

    def __init__(self):
        super(InstructionsScreen, self).__init__()  # calling all parent constructors

    def show(self):  # implementing abstract method from Screen
        # TODO: Implement this
        if self.hasFinished:
            print("Game has finished!")
        else:
            print("Game is running!")

    def button_press(self, button):  # implementing abstract method from Screen
        # if "q" is pressed, stop the game, otherwise start it
        if button != "q":
            if self.hasFinished:
                self.start()
        else:
            self.stop()