from screen_manager import ScreenManager


if __name__ == "__main__":

    # test that ScreenManager initializes and "shows" a screen
    sm = ScreenManager()
    sm.show_active_screen()

    # test that pressing any key other than "q" starts the game
    sm.button_press("start game pls")
    sm.show_active_screen()

    # test that pressing "q" stops the game
    sm.button_press("q")
    sm.show_active_screen()
