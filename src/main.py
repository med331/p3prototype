import time
from math import floor

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from src.game import Game
from src.gesture_engine import Hand
import sys
import cv2


class GameWidget(QtWidgets.QWidget):
    """
        THE CLASS THAT HANDLES USER MOUSE INPUT AND DRAWS THE GAME OBJECTS
    """

    def __init__(self, game, program):
        super(GameWidget, self).__init__()   # calls QtWidgets.QWidget constructor
        self.program = program               # a reference to the main app
        self.game = game                     # a reference to the game object
        self.game.two_hands_in_frame = True  # when testing, there are always two hands in the frame
        self.time_stamp = 0                  # time variable to maintaining consistent game tile renders

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Update the game when the user moves the mouse

        NOTE: THIS IS ONLY USED FOR DEBUGGING PURPOSES
        This method is invoked by Qt internally, and therefore never explicitly called in our code"""

        # save mouse coordinates as x and y, and offset them to fit the screen
        (x, y) = (a0.globalX(), a0.globalY())
        (x, y) = (x - 650, y - 300)

        # declare the "fake" middle point
        self.game.middle_point = (x + 100, y)

        # Initialize two new hands, offsetting them appropriately from mouse coordinate
        new_hands = [Hand(x - 100, y, 1, 1),
                     Hand(x + 100, y, 1, 1)]

        # override the old hands with the new hands
        self.game.hands = new_hands

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Update the game when the user presses a mouse button

        NOTE: THIS IS ONLY USED FOR DEBUGGING PURPOSES
        This method is invoked by Qt internally, and therefore never explicitly called in our code"""

        self.game.is_holding_turtle = True  # pick up turtle when mouse button is pressed

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Update the game when the user lets go of a mouse button

        NOTE: THIS IS ONLY USED FOR DEBUGGING PURPOSES
        This method is invoked by Qt internally, and therefore never explicitly called in our code"""

        self.game.is_holding_turtle = False  # release the turtle when mouse button is no longer being pressed

    def draw(self):
        """Draws the game tiles, player hands, and the position of the turtle

        This method renders the turtle based on whether or not it's being carried. It also renders the game field,
        turning the two-dimensional array from the Game object into sprites on the screen."""

        program = self.program  # shorthand

        # Only render anything if the game detects two hands in the frame
        if self.game.two_hands_in_frame:
            try:

                # if the turtle is being held, render it in the player's hands, otherwise, render it on the game tile
                if self.game.is_holding_turtle:
                    # render Bila Turtle in the hands of the player
                    program.GameBilaturtle.setGeometry(
                        QtCore.QRect(self.game.middle_point[0] - 70, self.game.middle_point[1] - 250, 100, 110))
                else:
                    # Render Bila Turtle on closest tile
                    x_position = 100 + floor((600 / 3) * self.game.field.turtleXPosition)
                    program.GameBilaturtle.setGeometry(
                        QtCore.QRect(x_position - 50, 300, 100, 110))

                # draw player hands
                program.GameLeftHand.setGeometry(
                    QtCore.QRect(self.game.hands[0].x + 20, self.game.hands[0].y, 200, 220))
                program.GameRightHand.setGeometry(
                    QtCore.QRect(self.game.hands[1].x - 20, self.game.hands[1].y, 200, 220))

            except: pass  # ignore any potential errors that may occur

            # only update the game tiles if at least 20 milliseconds have passed
            if self.time_stamp == 0 or time.time() - self.time_stamp > 0.02:  # ensure at least 20 ms delay
                self.time_stamp = time.time()                            # reset time_stamp
                delta_time = (time.time() - self.game.update_time) * 50  # Used to give the illusion of tile movement
                for x in range(len(self.game.field.fieldArray)):
                    for y in range(len(self.game.field.fieldArray[x])):

                        # define the position of the tile according to it's position in the 2d game field list
                        pos_x = 200 + 200 * (x - 1)
                        pos_y = -400 + 200 * (y - 1)
                        pos_y = pos_y + delta_time  # make sure to offset the y coordinate

                        # draw appropriate sprite
                        reverse_y = (len(self.game.field.fieldArray[0]) - 1) - y  # accounting for difference in implementation of 2d lists
                        new_sprite = program.field[(6 * x) - reverse_y]           # the QLabel to be turned into a game tile
                        sprite_type = self.game.field.fieldArray[x][reverse_y]    # the type of the sprite, with 0 = grass, 1 = carrot, 2 = seagull, and 3 = water

                        if sprite_type != 3:  # activates for type 0, 1, and 2
                            # draw the new sprite as a grass tile
                            new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                            new_sprite.setPixmap(QPixmap("sprites/Plain.png"))
                            new_sprite.setScaledContents(True)
                            new_sprite.setObjectName("PlainTile%s%s" % (x, y))

                        if sprite_type == 1:
                            # draw the new sprite as a carrot tile
                            new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                            new_sprite.setPixmap(QPixmap("sprites/Carrot.png"))
                            new_sprite.setScaledContents(True)
                            new_sprite.setObjectName("Pickup%s%s" % (x, y))

                        elif sprite_type == 2:
                            # draw the new sprite as a seagull tile
                            new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                            new_sprite.setPixmap(QPixmap("sprites/Seagull.png"))
                            new_sprite.setScaledContents(True)
                            new_sprite.setObjectName("Seagull%s%s" % (x, y))

                        elif sprite_type == 3:
                            # draw the new sprite as a water tile
                            new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                            new_sprite.setPixmap(QPixmap("sprites/Lake.png"))
                            new_sprite.setScaledContents(True)
                            new_sprite.setObjectName("River%s%s" % (x, y))


class BilaTurtle(object):
    """
        THE MAIN CLASS REPRESENTING THE APP
    """

    def __init__(self, mw):

        # declare essential variables
        self.field = []          # list to hold "dummy tiles" that will be overwritten on game start
        self.mw = mw             # save a reference to the main window of the app
        self.updating = False    # whether or not a game update is currently in progress
        self.previous_index = 1  # the index of the previously shown screen

        # initialize and setup GUI
        self.game = Game()
        self.setup_gui()

        # initialize OpenCV and the built-in front-facing camera, setting video source and dimensions
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 800)
        self.cap.set(4, 600)

        # initialize the game update timer, ideally updating the game every millisecond
        self.timer = QTimer()
        self.timer.setInterval(1)  # 1 millisecond update intervals
        self.timer.timeout.connect(self.update_game)  # call the update_game function when interval is completed
        self.timer.start()  # run the timer

    def update_game(self):
        """Update the game and associated GUI values

        This method should be called repeatedly, and processes both gesture input, game state, and game GUI elements."""

        if self.updating:  # for debugging, game updates are only skipped in extreme circumstances
            print("Skipped a scheduled game update, because one is already under way!")
        # if the game hasn't finished yet and the previous game update has completed, update the game again
        if not self.game.hasFinished or self.updating:
            self.updating = True        # if this game update hangs, another will not be called until this is disabled
            frame = self.cap.read()[1]  # retrieve a new frame from the built-in front-facing camera
            self.game.update(frame)     # update the game logic and Gesture Engine
            self.update_gui()           # updates static parts of the GUI, like text showing points and streaks
            self.GameScreen.draw()      # update the game tiles, turtle, and hand positions
            self.updating = False       # Game update has finished, opening up for new ones

    def change_screen(self, index):
        """Switch between screens in the app using an Integer index

        Additionally, this method also makes sure to start and stop the game when moving to and from the Game Screen."""

        if index == 0:
            # switching to game screen, start the game
            self.game.start()
        else:
            if self.previous_index == 0:
                # switching away from game screen, reset the game
                self.game.stop()
        # perform the screen switch, saving the index for reference during next change_screen call
        self.stackedWidget.setCurrentIndex(index)
        self.previous_index = index

    def change_difficulty(self):
        """Update the difficulty of the game

        This method reads the value of the difficulty slider and sets the difficulty of the game accordingly."""

        value = self.DifficultySlider.value()  # retrieve value from the difficulty slider on the Settings Screen
        self.game.change_difficulty(value)     # pass that value on to the game

    def setup_gui(self):
        """perform initializations of internal GUI components

        This method should only be called once, immediately upon creation of the Bila Turtle object."""

        # build main window, set fixed size and standard button sizes
        MainWindow = self.mw
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.buttonWidth = 100
        self.buttonHeight = 50
        # build the QStackedWidget (the widget that contains all the screens as indexes of it) set it as central
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.stackedWidget.setObjectName("stackedWidget")
        # build GameScreen as an instance of the GameWidget class, in order to inherit all the Game Logic methods
        self.GameScreen = GameWidget(self.game, self)
        self.GameScreen.setObjectName("GameScreen")
        # build progress bar on the game screen, design it's geometry and assign it a default value of 0
        self.GameScreenProgressBar = QtWidgets.QProgressBar(self.GameScreen)
        self.GameScreenProgressBar.setGeometry(QtCore.QRect(660, 10, 118, 23))
        self.GameScreenProgressBar.setProperty("value", 0)
        self.GameScreenProgressBar.setObjectName("GameScreenProgressBar")
        # create a QLabel for indicative text
        self.GSInfoLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSInfoLabel.setGeometry(QtCore.QRect(660, 30, 221, 31))
        self.GSInfoLabel.setObjectName("GSInfoLabel")
        # using a loop, create 24 QLabels, representing the 24 images in the game field
        # insert them into the field array using the "append" method
        for i in range(24):
            widget = QtWidgets.QLabel(self.GameScreen)
            widget.setObjectName("FieldTile%s" % i)
            self.field.append(widget)
        # create the two buttons on the Game Screen, make them switch to the corresponding screens
        self.GameScreenButton1 = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenButton1.setGeometry(QtCore.QRect(20, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenButton1.setObjectName("GameScreenButton1")
        # lambda is used throughout this class because clicked.connect expects a returnable method
        self.GameScreenButton1.clicked.connect(lambda: self.change_screen(2))
        self.GameScreenQuit = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenQuit.setGeometry(QtCore.QRect(670, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenQuit.setObjectName("GameScreenButton1")
        self.GameScreenQuit.clicked.connect(lambda: self.change_screen(4))
        # create the QLabels where the turtle and the turtle projection will be added
        self.GameBilaturtle = QtWidgets.QLabel(self.GameScreen)
        self.GameBilaturtle.setGeometry(QtCore.QRect(2290, 340, 200, 220))
        self.GameBilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
        self.GameBilaturtle.setScaledContents(True)
        self.GameBilaturtle.setObjectName("GameBilaturtle")
        self.GameBilaProjection = QtWidgets.QLabel(self.GameScreen)
        self.GameBilaProjection.setGeometry(QtCore.QRect(2290, 340, 200, 220))
        self.GameBilaProjection.setPixmap(QPixmap("sprites/turtle_projection.png"))
        self.GameBilaProjection.setScaledContents(True)
        self.GameBilaProjection.setObjectName("GameBilaProjection")
        # create the QLabels where the hands will be added
        self.GameLeftHand = QtWidgets.QLabel(self.GameScreen)
        self.GameLeftHand.setGeometry(QtCore.QRect(2290, 340, 200, 220))
        self.GameLeftHand.setPixmap(QPixmap("sprites/sideways_left_hand.png"))
        self.GameLeftHand.setScaledContents(True)
        self.GameLeftHand.setObjectName("GameLeftHand")
        self.GameRightHand = QtWidgets.QLabel(self.GameScreen)
        self.GameRightHand.setGeometry(QtCore.QRect(2290, 340, 200, 220))
        self.GameRightHand.setPixmap(QPixmap("sprites/sideways_right_hand.png"))
        self.GameRightHand.setScaledContents(True)
        self.GameRightHand.setObjectName("GameLeftHand")
        # create a QLabel used for indicative text
        self.TwoHandsText = QtWidgets.QLabel(self.GameScreen)
        self.TwoHandsText.setGeometry(QtCore.QRect(210, 400, 400, 100))
        self.TwoHandsText.setObjectName("TwoHandsText")
        # create three labels for indicating the Points, Time Elapsed, and Streak to the user
        self.GSPointsLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSPointsLabel.setGeometry(QtCore.QRect(20, 5, 221, 31))
        self.GSPointsLabel.setObjectName("GSPointsLabel")
        self.GSTimeLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSTimeLabel.setGeometry(QtCore.QRect(20, 35, 161, 31))
        self.GSTimeLabel.setObjectName("GSTimeLabel")
        self.GSStreakLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSStreakLabel.setGeometry(QtCore.QRect(20, 65, 181, 31))
        self.GSStreakLabel.setObjectName("GSStreakLabel")
        # finally, add the screen to the stacked widget, Game Screen becoming index 0 in the stackedWidget
        self.stackedWidget.addWidget(self.GameScreen)
        # build difficulty screen as a QWidget
        self.DifficultyScreen = QtWidgets.QWidget()
        self.DifficultyScreen.setObjectName("DifficultyScreen")
        # create a Qlabel for the background of the difficulty (settings) screen
        self.DiffBackground = QtWidgets.QLabel(self.DifficultyScreen)
        self.DiffBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.DiffBackground.setPixmap(QPixmap("sprites/settings_screen.png"))
        self.DiffBackground.setScaledContents(True)
        self.DiffBackground.setObjectName("DiffBackground")
        # create a slider used for controlling the difficulty of the game
        self.DifficultySlider = QtWidgets.QSlider(self.DifficultyScreen)
        self.DifficultySlider.setGeometry(QtCore.QRect(90, 210, 621, 41))
        # set a maximum value of 5, horizontal orientation, ticks below the slider and assign it to change difficulty
        self.DifficultySlider.setMaximum(5)
        self.DifficultySlider.setOrientation(QtCore.Qt.Horizontal)
        self.DifficultySlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.DifficultySlider.valueChanged.connect(self.change_difficulty)
        self.DifficultySlider.setObjectName("DifficultySlider")
        # create the check boxes, which would have been used for more customization, but current implementation does
        # not allow it
        self.PullingCheckBox = QtWidgets.QCheckBox(self.DifficultyScreen)
        self.PullingCheckBox.setGeometry(QtCore.QRect(80, 340, 70, 17))
        self.PullingCheckBox.setChecked(True)
        self.PullingCheckBox.setObjectName("PullingCheckBox")
        self.PushingCheckBox = QtWidgets.QCheckBox(self.DifficultyScreen)
        self.PushingCheckBox.setGeometry(QtCore.QRect(80, 370, 70, 17))
        self.PushingCheckBox.setChecked(True)
        self.PushingCheckBox.setObjectName("PushingCheckBox")
        self.GrabbingCheckBox = QtWidgets.QCheckBox(self.DifficultyScreen)
        self.GrabbingCheckBox.setGeometry(QtCore.QRect(80, 400, 70, 17))
        self.GrabbingCheckBox.setChecked(True)
        self.GrabbingCheckBox.setObjectName("GrabbingCheckBox")
        self.ReachingCheckBox = QtWidgets.QCheckBox(self.DifficultyScreen)
        self.ReachingCheckBox.setGeometry(QtCore.QRect(80, 430, 70, 17))
        self.ReachingCheckBox.setChecked(True)
        self.ReachingCheckBox.setObjectName("ReachingCheckBox")
        # create the back button, assign it to go back to the start screen
        self.BackButtonSettingsScreen = QtWidgets.QPushButton(self.DifficultyScreen)
        self.BackButtonSettingsScreen.setGeometry(QtCore.QRect(360, 480, self.buttonWidth, self.buttonHeight))
        self.BackButtonSettingsScreen.setObjectName("BackButtonSettingsScreen")
        self.BackButtonSettingsScreen.clicked.connect(lambda: self.change_screen(3))
        # add screen to StackedWidget, meaning it gets index 1
        self.stackedWidget.addWidget(self.DifficultyScreen)
        # create Instructions Screen as a QWidget
        self.InstructionsScreen = QtWidgets.QWidget()
        self.InstructionsScreen.setObjectName("InstructionsScreen")
        # create the QLabel that contains the picture displaying the Instructions Screen
        self.InstructionsHeader = QtWidgets.QLabel(self.InstructionsScreen)
        self.InstructionsHeader.setGeometry(QtCore.QRect(0, 0, 801, 581))
        # given that this screen does not have any game functionality, it's just an image displayed on the screen
        self.InstructionsHeader.setPixmap(QPixmap("sprites/Instructions.png"))
        self.InstructionsHeader.setScaledContents(True)
        self.InstructionsHeader.setObjectName("InstructionsHeader")
        # create the button to go back to the Game Screen
        self.InstructionsBackButton = QtWidgets.QPushButton(self.InstructionsScreen)
        self.InstructionsBackButton.setGeometry(QtCore.QRect(360, 525, self.buttonWidth, self.buttonHeight))
        self.InstructionsBackButton.setObjectName("pushButton_3")
        self.InstructionsBackButton.clicked.connect(lambda: self.change_screen(0))
        # add the screen to the StackedWidget, it gets index 2
        self.stackedWidget.addWidget(self.InstructionsScreen)

        # create Start Screen as a QWidget
        self.StartScreen = QtWidgets.QWidget()
        self.StartScreen.setObjectName("StartScreen")
        # create the background containing the title text
        self.BilaturtleText = QtWidgets.QLabel(self.StartScreen)
        self.BilaturtleText.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.BilaturtleText.setPixmap(QPixmap("sprites/start_screen.png"))
        self.BilaturtleText.setScaledContents(True)
        self.BilaturtleText.setObjectName("BilaturtleText")
        # create the QLabel containing the turtle logo
        self.Bilaturtle = QtWidgets.QLabel(self.StartScreen)
        self.Bilaturtle.setGeometry(QtCore.QRect(290, 340, 200, 220))
        self.Bilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
        self.Bilaturtle.setScaledContents(True)
        self.Bilaturtle.setObjectName("Bilaturtle")
        # create the two buttons and assign them to be linked to the proper screens
        self.StartButton = QtWidgets.QPushButton(self.StartScreen)
        self.StartButton.setGeometry(QtCore.QRect(330, 160, self.buttonWidth, self.buttonHeight))
        self.StartButton.setObjectName("StartButton")
        self.StartButton.clicked.connect(lambda: self.change_screen(0))
        self.SettingsButton = QtWidgets.QPushButton(self.StartScreen)
        self.SettingsButton.setGeometry(QtCore.QRect(330, 230, self.buttonWidth, self.buttonHeight))
        self.SettingsButton.setObjectName("SettingsButton")
        self.SettingsButton.clicked.connect(lambda: self.change_screen(1))
        # create the two filler tables, which would have been developed more with more time
        # currently, these tables offer an indication of what the competition system of a fuller implementation of
        # Bilaturtle would look like
        self.PersonalTable = QtWidgets.QTableWidget(self.StartScreen)
        self.PersonalTable.setGeometry(QtCore.QRect(120, 150, 121, 191))
        self.PersonalTable.setObjectName("PersonalTable")
        self.PersonalTable.setColumnCount(1)
        self.PersonalTable.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PersonalTable.setItem(4, 0, item)
        self.GroupTable = QtWidgets.QTableWidget(self.StartScreen)
        self.GroupTable.setGeometry(QtCore.QRect(550, 150, 121, 191))
        self.GroupTable.setObjectName("GroupTable")
        self.GroupTable.setColumnCount(1)
        self.GroupTable.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.GroupTable.setItem(4, 0, item)
        # add screen to the StackedWidget, gets index 3
        self.stackedWidget.addWidget(self.StartScreen)
        # create QuitScreen as a QWidget
        self.QuitScreen = QtWidgets.QWidget()
        self.QuitScreen.setObjectName("QuitScreen")
        # create a QLabel containing the background of the quit screen, with the header text
        self.QuitBackground = QtWidgets.QLabel(self.QuitScreen)
        self.QuitBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.QuitBackground.setPixmap(QPixmap("sprites/quit_screen.png"))
        self.QuitBackground.setScaledContents(True)
        self.QuitBackground.setObjectName("QuitBackground")
        # create the two buttons and link them to the proper screens
        self.QuitYesButton = QtWidgets.QPushButton(self.QuitScreen)
        self.QuitYesButton.setGeometry(QtCore.QRect(290, 240, self.buttonWidth, self.buttonHeight))
        self.QuitYesButton.setObjectName("QuitYesButton")
        self.QuitYesButton.clicked.connect(lambda: self.change_screen(5))
        self.QuitNoButton = QtWidgets.QPushButton(self.QuitScreen)
        self.QuitNoButton.setGeometry(QtCore.QRect(420, 240, self.buttonWidth, self.buttonHeight))
        self.QuitNoButton.setObjectName("QuitNoButton")
        self.QuitNoButton.clicked.connect(lambda: self.change_screen(0))
        # finally, add the screen to the StackedWidget, gets index 4
        self.stackedWidget.addWidget(self.QuitScreen)
        # lastly, create Progress Screeen as a QWidget
        self.ProgressScreen = QtWidgets.QWidget()
        # create the QLabel containing the plain background
        self.ProgressBackground = QtWidgets.QLabel(self.ProgressScreen)
        self.ProgressBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.ProgressBackground.setPixmap(QPixmap("sprites/Plain.png"))
        self.ProgressBackground.setScaledContents(True)
        self.ProgressBackground.setObjectName("DiffBackground")
        self.ProgressScreen.setObjectName("ProgressScreen")
        # create the QLabel with the text congratulating the player
        self.GoodJobText = QtWidgets.QLabel(self.ProgressScreen)
        self.GoodJobText.setGeometry(QtCore.QRect(370, 90, 261, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.GoodJobText.setFont(font)
        self.GoodJobText.setObjectName("GoodJobText")
        # create the progress bar, points, time and streak label, which are basically the same as the
        # ones on the GameScreen
        self.ProgressScreenProgressBar = QtWidgets.QProgressBar(self.ProgressScreen)
        self.ProgressScreenProgressBar.setGeometry(QtCore.QRect(310, 220, 231, 61))
        self.ProgressScreenProgressBar.setProperty("value", 24)
        self.ProgressScreenProgressBar.setObjectName("ProgressScreenProgressBar")
        self.PointsLabel = QtWidgets.QLabel(self.ProgressScreen)
        self.PointsLabel.setGeometry(QtCore.QRect(310, 300, 221, 31))
        self.PointsLabel.setObjectName("PointsLabel")
        self.TimeLabel = QtWidgets.QLabel(self.ProgressScreen)
        self.TimeLabel.setGeometry(QtCore.QRect(310, 330, 161, 31))
        self.TimeLabel.setObjectName("TimeLabel")
        self.StreakLabel = QtWidgets.QLabel(self.ProgressScreen)
        self.StreakLabel.setGeometry(QtCore.QRect(310, 360, 181, 31))
        self.StreakLabel.setObjectName("StreakLabel")
        # create the Continue button on the main screen, link it to the Start Screen
        self.ProgressContinueButton = QtWidgets.QPushButton(self.ProgressScreen)
        self.ProgressContinueButton.setGeometry(QtCore.QRect(370, 430, self.buttonWidth, self.buttonHeight))
        self.ProgressContinueButton.setObjectName("ProgressContinueButton")
        self.ProgressContinueButton.clicked.connect(lambda: self.change_screen(3))
        # finally add the screen to the StackedWidget, getting index 5
        self.stackedWidget.addWidget(self.ProgressScreen)
        # set the central widget (QStackedWidget) as the central widget in the main window
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # call the update_gui method to refresh the gui
        self.update_gui()
        # set the starting index to 3, which is the Start Screen
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # finally, assign text to UI elements that don't need to be continuously updated
        _translate = QtCore.QCoreApplication.translate
        # set window name and icon
        MainWindow.setWindowTitle(_translate("MainWindow", "Bilaturtle Alpha"))
        MainWindow.setWindowIcon(QtGui.QIcon('sprites/Turtle.png'))
        # set corresponding text to the Buttons, QLabels, CheckBoxes and tables that
        # don't change their value at any point
        self.GameScreenButton1.setText(_translate("MainWindow", "Instructions"))
        self.GameScreenQuit.setText(_translate("MainWindow", "Quit"))
        self.PullingCheckBox.setText(_translate("MainWindow", "Pulling"))
        self.PushingCheckBox.setText(_translate("MainWindow", "Pushing"))
        self.GrabbingCheckBox.setText(_translate("MainWindow", "Grabbing"))
        self.ReachingCheckBox.setText(_translate("MainWindow", "Reaching"))
        self.BackButtonSettingsScreen.setText(_translate("MainWindow", "Back"))
        self.InstructionsBackButton.setText(_translate("MainWindow", "Back"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.SettingsButton.setText(_translate("MainWindow", "Settings"))
        item = self.PersonalTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1."))
        item = self.PersonalTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2."))
        item = self.PersonalTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3."))
        item = self.PersonalTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4."))
        item = self.PersonalTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5."))
        item = self.PersonalTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Personal"))
        __sortingEnabled = self.PersonalTable.isSortingEnabled()
        self.PersonalTable.setSortingEnabled(False)
        item = self.PersonalTable.item(0, 0)
        item.setText(_translate("MainWindow", "John"))
        item = self.PersonalTable.item(1, 0)
        item.setText(_translate("MainWindow", "Mary"))
        item = self.PersonalTable.item(2, 0)
        item.setText(_translate("MainWindow", "You"))
        item = self.PersonalTable.item(3, 0)
        item.setText(_translate("MainWindow", "Peter"))
        item = self.PersonalTable.item(4, 0)
        item.setText(_translate("MainWindow", "Sue"))
        self.PersonalTable.setSortingEnabled(__sortingEnabled)
        item = self.GroupTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1."))
        item = self.GroupTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2. "))
        item = self.GroupTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3."))
        item = self.GroupTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4."))
        item = self.GroupTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5."))
        item = self.GroupTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Group"))
        __sortingEnabled = self.GroupTable.isSortingEnabled()
        self.GroupTable.setSortingEnabled(False)
        item = self.GroupTable.item(0, 0)
        item.setText(_translate("MainWindow", "Team 1"))
        item = self.GroupTable.item(1, 0)
        item.setText(_translate("MainWindow", "Team 2 (Your Team!)"))
        item = self.GroupTable.item(2, 0)
        item.setText(_translate("MainWindow", "Team 4"))
        item = self.GroupTable.item(3, 0)
        item.setText(_translate("MainWindow", "Team 5"))
        item = self.GroupTable.item(4, 0)
        item.setText(_translate("MainWindow", "Team 3"))
        self.GroupTable.setSortingEnabled(__sortingEnabled)
        self.QuitYesButton.setText(_translate("MainWindow", "Yes"))
        self.QuitNoButton.setText(_translate("MainWindow", "No"))
        self.ProgressContinueButton.setText(_translate("MainWindow", "Continue"))

    def update_gui(self):
        """update game-dependant text in the GUI

        Method used for continuously refreshing the GUI when in the Game Screen and when hands are detected,
        also assigns text to the previously created labels."""

        _translate = QtCore.QCoreApplication.translate
        # set the values of the labels and progress bars that change their value, this has to be called continuously.
        self.PointsLabel.setText(_translate("MainWindow", "Points: %s" % self.game.currentPoints))
        self.TimeLabel.setText(_translate("MainWindow", "Time: %s" % self.game.get_elapsed_play_time()))
        self.StreakLabel.setText(_translate("MainWindow", "Streak: %s" % self.game.currentStreak))
        self.GSPointsLabel.setText(_translate("MainWindow", "Points: %s" % self.game.currentPoints))
        self.GSInfoLabel.setText(_translate("MainWindow", "Get to 20 minutes!"))
        self.GSTimeLabel.setText(_translate("MainWindow", "Time: %s" % self.game.get_elapsed_play_time()))
        self.GSStreakLabel.setText(_translate("MainWindow", "Streak: %s" % self.game.currentStreak))
        self.GameScreenProgressBar.setProperty("value", self.game.get_elapsed_play_time()/12)
        self.ProgressScreenProgressBar.setProperty("value", self.game.get_elapsed_play_time() / 12)
        # if the user completes the 20 minutes recommended session time, they get congratulated, else they
        # are encouraged to try again
        if self.game.get_elapsed_play_time() >= 1200:
            self.GoodJobText.setText(_translate("MainWindow", "Good job!"))
        else:
            self.GoodJobText.setGeometry(QtCore.QRect(100, 90, 661, 91))
            self.GoodJobText.setText(_translate("MainWindow", "You haven't reached the 20 minute target, you have "
                                                              "to try harder!"))
        # show text indicating that two hands were not found when two hands are not in frame
        if not self.game.two_hands_in_frame:
            self.TwoHandsText.setText(_translate("MainWindow", "CANNOT DETECT HANDS. Try moving your hands towards \n" +
                                                           "the center or improve the lighting conditions in the room"))
        else:
            self.TwoHandsText.setText(_translate("MainWindow", ""))


if __name__ == "__main__":

    # set up GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    bt = BilaTurtle(MainWindow)

    # launch app
    MainWindow.show()

    # there is no returning from this
    sys.exit(app.exec_())  # thread will be held in this call until program termination
