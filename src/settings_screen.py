from src.screen import Screen
from src.game import Game
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class SettingsScreen(Screen):

    def __init__(self):
        super(SettingsScreen, self).__init__()  # calling all parent constructors

    def show(self):  # implementing abstract method from Screen
        #app = QApplication([])
        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Topperino'))
        layout.addWidget(QPushButton('Bottom'))
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