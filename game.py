"""
        Game must maintain the game state and handle the logic of the game itself
"""

from gesture_engine import GestureEngine


class Game(GestureEngine):

    def __init__(self):
        super(Game, self).__init__()  # calling GestureEngine constructor
        self.hasFinished = True

    def start(self):
        self.hasFinished = False
        # TODO: Implement the rest

    def stop(self):
        self.hasFinished = True
        # TODO: Implement the rest

    def get_game_data(self):
        return {"Two Hands In Frame?": self.twoHandsInFrame,
                "Game Has Finished?": self.hasFinished,
                "Is This Dictionary Placeholder?": True}
