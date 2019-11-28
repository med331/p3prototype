from unittest import TestCase
from src.screen_manager import ScreenManager as sm
from src.screen import Screen


class TestScreen(Screen):

    def __init__(self, name):
        super(Screen, self).__init__()
        self._name = name

    def show(self):
        return self._name

    def button_press(self, button):
        return "%s: %s" % (self._name, button)


class TestScreenManagerMethods(TestCase):

    def setUp(self) -> None:
        sm._screens.append(TestScreen("s1"))
        sm._screens.append(TestScreen("s2"))

    def test_change_screen(self):
        sm.change_screen(0)
        self.assertEqual(sm._screens[sm._activeScreenIndex]._name, "s1", "Screen Manager does not change screens!")
        sm.change_screen(1)
        self.assertEqual(sm._screens[sm._activeScreenIndex]._name, "s2", "Screen Manager does not change screens at all!")

    def test_change_screen_from_within_screen(self):
        sm.change_screen(0)  # start at screen[0] - assuming change_screen works!
        sm._screens[0].change_screen(1)
        self.assertEqual(sm._screens[sm._activeScreenIndex]._name, "s2", "Screen Manager does not change screens when "
                                                                         "called from within a screen!")

    def test_button_press(self):
        sm.change_screen(0)  # start at screen[0] - assuming change_screen works!
        self.assertEqual(sm.button_press("b1"), "s1: b1", "Screen Manager does not forward button push!")
        sm.change_screen(1)
        self.assertEqual(sm.button_press("b2"), "s2: b2", "Screen Manager does not forward button push!")

    def test_show_active_screen(self):  # all tests rely on this method
        sm.change_screen(1)  # start at screen[1] - assuming change_screen works!
        self.assertEqual(sm.show_active_screen(), "s2", "Screen Manager does not show correct screen!")
        sm.change_screen(0)
        self.assertEqual(sm.show_active_screen(), "s1", "Screen Manager does not show correct screen!")
