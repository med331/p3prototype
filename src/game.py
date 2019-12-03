"""
        Game must maintain the game state and handle the logic of the game itself
"""

from src.gesture_engine import GestureEngine


class Game(GestureEngine):  # please see tests/test_game for how to test your code

    def __init__(self):
        super(Game, self).__init__()  # calling GestureEngine constructor
        self.hasFinished = True

    def start(self):
        self.hasFinished = False
        # TODO: Implement the rest

    def stop(self):
        self.hasFinished = True
        # TODO: Implement the rest

    def update(self, frame):
        # update GestureEngine
        print(self.is_holding_turtle)
        return self.process_frame(frame)
        # TODO: update the rest of the game
