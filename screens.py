"""
        Screen is currently fully implemented
"""


class Screen:  # abstract class

    def __init__(self):
        self._someState = "a state" # TODO: Class can be scrapped if no state is maintained here

    def show(self):                 # abstract method
        raise NotImplementedError

    def buttonPress(self, button):  # abstract method
        raise NotImplementedError
