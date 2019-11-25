from unittest import TestCase

from src.game import Game


# TODO: Make your own test file in this folder and follow this guide for writing tests:
#  https://www.jetbrains.com/help/pycharm/testing-your-first-python-application.html

class TestGame(TestCase):

    def setUp(self) -> None:
        self._game = Game()


class TestGame(TestGame):

    def testStart(self):
        self.assertEqual(self._game.hasFinished, True, "Game starts off not finished!")
        self._game.start()
        self.assertEqual(self._game.hasFinished, False, "Game does not start!")

    def testStop(self):  # requires Game.start to work
        self._game.start()
        self._game.stop()
        self.assertEqual(self._game.hasFinished, True, "Game does not stop!")
