from screen_manager import ScreenManager


if __name__ == "__main__":

    sm = ScreenManager()
    sm.show_active_screen()

    sm.button_press("start game pls")
    sm.show_active_screen()

    sm.button_press("q")
    sm.show_active_screen()