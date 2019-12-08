# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
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
    def __init__(self, game, program):
        super(GameWidget, self).__init__()
        self.program = program
        self.game = game
        self.game.two_hands_in_frame = True
        self.time_stamp = 0

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        (x, y) = (a0.globalX(), a0.globalY())
        (x, y) = (x - 650, y - 300)
        self.game.middle_point = (x + 100, y)
        new_hands = []
        new_hands.append(Hand(x - 100, y, 1, 1))
        new_hands.append(Hand(x + 100, y, 1, 1))
        self.game.hands = new_hands
        #self.draw()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.game.is_holding_turtle = True
        time.sleep(0.05)  # add delay to ensure GestureEngine update before drawing
        #self.draw()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.game.is_holding_turtle = False
        time.sleep(0.05)  # add delay to ensure GestureEngine update before drawing
        #self.draw()

    def draw(self):
        program = self.program
        if self.game.two_hands_in_frame:
            try:
                program.Bilaturtle.setGeometry(QtCore.QRect(self.game.hands[0].x, self.game.hands[0].y, 200, 220))
                if self.game.is_holding_turtle:
                    program.GameBilaturtle.setGeometry(
                        QtCore.QRect(self.game.middle_point[0] - 50, self.game.middle_point[1] - 55, 100, 110))
                else:
                    #print(game.field.turtleXPosition)
                    x_position = 100 + floor((600 / 3) * self.game.field.turtleXPosition)
                    program.GameBilaturtle.setGeometry(
                        QtCore.QRect(x_position - 50, 300, 100, 110))

                # TODO: this is debugging only
                '''x_position = 150 + floor((500 / 3) * game.hand_tile)
                self.GameBilaturtle.setGeometry(
                    QtCore.QRect(x_position - 50, 250, 100, 110))'''

                # draw hands
                program.GameLeftHand.setGeometry(
                    QtCore.QRect(self.game.hands[0].x, self.game.hands[0].y, 200, 220))
                program.GameRightHand.setGeometry(
                    QtCore.QRect(self.game.hands[1].x, self.game.hands[1].y, 200, 220))
            except:
                pass

            #print(time.time() - game.startTime)
            if self.time_stamp == 0 or time.time() - self.time_stamp > 0.02:  # game field updates ten times per second
                self.time_stamp = time.time()
                delta_time = (time.time() - self.game.startTime) * 50

                for x in range(len(self.game.field.fieldArray)):
                    for y in range(len(self.game.field.fieldArray[x])):
                        if True:  #x == 0:  # TODO: only for debugging
                            #print(x != 0 and y != 0)
                            #print("x: %s & y: %s" % (x, y))
                            pos_x = 200 + 200 * (x - 1)
                            pos_y = -400 + 200 * (y - 1)
                            #new_tiles = round((time.time() - game.startTime) - game.speed)
                            #print("new_tiles: %s" % new_tiles)
                            pos_y = pos_y + delta_time
                            #print("pos_x: %s & pos_y: %s" % (pos_x, pos_y))

                            '''program.GameBilaturtle = QtWidgets.QLabel(program.GameScreen)
                            program.GameBilaturtle.setGeometry(QtCore.QRect(290, 340, 200, 220))
                            program.GameBilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
                            program.GameBilaturtle.setScaledContents(True)
                            program.GameBilaturtle.setObjectName("GameBilaturtle")'''

                            # draw appropriate sprite
                            reverse_y = (len(self.game.field.fieldArray[0]) - 1) - y
                            new_sprite = program.field[(6 * x) - reverse_y]
                            sprite_type = self.game.field.fieldArray[x][reverse_y]
                            #print(sprite_type)
                            #print("Reverse: %s & input: %s" % (reverse_y, y))


                            #new_sprite.setText("Peter is a douchebag")
                            #print("x: %s and y: %s" % (pos_x, pos_y))
                            #new_sprite = QtWidgets.QLabel(program.GameScreen)
                            if sprite_type != 3:  # activates for type 0, 1, 2, and 4
                                # TODO: draw plain sprite
                                new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                                new_sprite.setPixmap(QPixmap("sprites/Plain.png"))
                                new_sprite.setScaledContents(True)
                                new_sprite.setObjectName("PlainTile%s%s" % (x, y))
                            if sprite_type == 1:
                                new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                                new_sprite.setPixmap(QPixmap("sprites/Carrot.png"))
                                new_sprite.setScaledContents(True)
                                new_sprite.setObjectName("Pickup%s%s" % (x, y))
                                # TODO: draw pickupsF
                            elif sprite_type == 2:
                                new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                                new_sprite.setPixmap(QPixmap("sprites/Seagull.png"))
                                new_sprite.setScaledContents(True)
                                new_sprite.setObjectName("Seagull%s%s" % (x, y))
                                # TODO: draw seaguls
                            elif sprite_type == 3:
                                new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                                new_sprite.setPixmap(QPixmap("sprites/Lake.png"))
                                new_sprite.setScaledContents(True)
                                new_sprite.setObjectName("River%s%s" % (x, y))
                                # TODO: draw water


class BilaTurtle(object):
    def __init__(self, mw):
        self.field = []
        self.mw = mw
        self.updating = False

        # initialize game
        self.game = Game()
        self.game.start()

        # initialize OpenCV and webcam capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 800)
        self.cap.set(4, 600)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_game)
        self.timer.start()

    def update_game(self):
        if self.updating:
            print("Skipped a scheduled game update, because one is already under way!")
        if not self.game.hasFinished or self.updating:
            self.updating = True
            # read a frame from the webcam and pass it on to the game (GestureEngine)
            frame = self.cap.read()[1]
            self.game.update(frame)
            self.update_gui()  # updates the entire gui
            self.GameScreen.draw()
            self.updating = False

    def setup_gui(self):
        MainWindow = self.mw
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.buttonWidth = 100
        self.buttonHeight = 50
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.stackedWidget.setObjectName("stackedWidget")

        self.GameScreen = GameWidget(self.game, self)
        self.GameScreen.setObjectName("GameScreen")
        self.GameScreenProgressBar = QtWidgets.QProgressBar(self.GameScreen)
        self.GameScreenProgressBar.setGeometry(QtCore.QRect(660, 10, 118, 23))
        self.GameScreenProgressBar.setProperty("value", 24)
        self.GameScreenProgressBar.setObjectName("GameScreenProgressBar")
        for i in range(24):
            widget = QtWidgets.QLabel(self.GameScreen)
            widget.setObjectName("FieldTile%s" % i)
            self.field.append(widget)
        self.GameScreenButton1 = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenButton1.setGeometry(QtCore.QRect(20, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenButton1.setObjectName("GameScreenButton1")
        self.GameScreenButton1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.GameScreenQuit = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenQuit.setGeometry(QtCore.QRect(670, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenQuit.setObjectName("GameScreenButton1")
        self.GameScreenQuit.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.GameBilaturtle = QtWidgets.QLabel(self.GameScreen)
        self.GameBilaturtle.setGeometry(QtCore.QRect(2290, 340, 200, 220))
        self.GameBilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
        self.GameBilaturtle.setScaledContents(True)
        self.GameBilaturtle.setObjectName("GameBilaturtle")
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
        self.GSPointsLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSPointsLabel.setGeometry(QtCore.QRect(20, 5, 221, 31))
        self.GSPointsLabel.setObjectName("GSPointsLabel")
        self.GSTimeLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSTimeLabel.setGeometry(QtCore.QRect(20, 35, 161, 31))
        self.GSTimeLabel.setObjectName("GSTimeLabel")
        self.GSStreakLabel = QtWidgets.QLabel(self.GameScreen)
        self.GSStreakLabel.setGeometry(QtCore.QRect(20, 65, 181, 31))
        self.GSStreakLabel.setObjectName("GSStreakLabel")
        self.stackedWidget.addWidget(self.GameScreen)

        self.DifficultyScreen = QtWidgets.QWidget()
        self.DifficultyScreen.setObjectName("DifficultyScreen")
        self.DiffBackground = QtWidgets.QLabel(self.DifficultyScreen)
        self.DiffBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.DiffBackground.setPixmap(QPixmap("sprites/settings_screen.png"))
        self.DiffBackground.setScaledContents(True)
        self.DiffBackground.setObjectName("DiffBackground")
        self.DifficultySlider = QtWidgets.QSlider(self.DifficultyScreen)
        self.DifficultySlider.setGeometry(QtCore.QRect(90, 210, 621, 41))
        self.DifficultySlider.setMaximum(2)
        self.DifficultySlider.setOrientation(QtCore.Qt.Horizontal)
        self.DifficultySlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.DifficultySlider.setObjectName("DifficultySlider")
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
        self.BackButtonSettingsScreen = QtWidgets.QPushButton(self.DifficultyScreen)
        self.BackButtonSettingsScreen.setGeometry(QtCore.QRect(360, 480, self.buttonWidth, self.buttonHeight))
        self.BackButtonSettingsScreen.setObjectName("BackButtonSettingsScreen")
        self.BackButtonSettingsScreen.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.stackedWidget.addWidget(self.DifficultyScreen)

        self.InstructionsScreen = QtWidgets.QWidget()
        self.InstructionsScreen.setObjectName("InstructionsScreen")
        self.InstructionsHeader = QtWidgets.QLabel(self.InstructionsScreen)
        self.InstructionsHeader.setGeometry(QtCore.QRect(0, 0, 801, 581))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.InstructionsHeader.setFont(font)
        self.InstructionsHeader.setPixmap(QPixmap("sprites/Instructions.png"))
        self.InstructionsHeader.setScaledContents(True)
        self.InstructionsHeader.setObjectName("InstructionsHeader")
        self.InstructionsBackButton = QtWidgets.QPushButton(self.InstructionsScreen)
        self.InstructionsBackButton.setGeometry(QtCore.QRect(360, 525, self.buttonWidth, self.buttonHeight))
        self.InstructionsBackButton.setObjectName("pushButton_3")
        self.InstructionsBackButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.stackedWidget.addWidget(self.InstructionsScreen)

        self.StartScreen = QtWidgets.QWidget()
        self.StartScreen.setObjectName("StartScreen")
        self.BilaturtleText = QtWidgets.QLabel(self.StartScreen)
        self.BilaturtleText.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.BilaturtleText.setPixmap(QPixmap("sprites/start_screen.png"))
        self.BilaturtleText.setScaledContents(True)
        self.BilaturtleText.setObjectName("BilaturtleText")
        self.Bilaturtle = QtWidgets.QLabel(self.StartScreen)
        self.Bilaturtle.setGeometry(QtCore.QRect(290, 340, 200, 220))
        self.Bilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
        self.Bilaturtle.setScaledContents(True)
        self.Bilaturtle.setObjectName("Bilaturtle")
        self.StartButton = QtWidgets.QPushButton(self.StartScreen)
        self.StartButton.setGeometry(QtCore.QRect(330, 160, self.buttonWidth, self.buttonHeight))
        self.StartButton.setObjectName("StartButton")
        self.StartButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.SettingsButton = QtWidgets.QPushButton(self.StartScreen)
        self.SettingsButton.setGeometry(QtCore.QRect(330, 230, self.buttonWidth, self.buttonHeight))
        self.SettingsButton.setObjectName("SettingsButton")
        self.SettingsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
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
        self.stackedWidget.addWidget(self.StartScreen)

        self.QuitScreen = QtWidgets.QWidget()
        self.QuitScreen.setObjectName("QuitScreen")
        self.QuitBackground = QtWidgets.QLabel(self.QuitScreen)
        self.QuitBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.QuitBackground.setPixmap(QPixmap("sprites/quit_screen.png"))
        self.QuitBackground.setScaledContents(True)
        self.QuitBackground.setObjectName("QuitBackground")
        self.QuitYesButton = QtWidgets.QPushButton(self.QuitScreen)
        self.QuitYesButton.setGeometry(QtCore.QRect(290, 240, self.buttonWidth, self.buttonHeight))
        self.QuitYesButton.setObjectName("QuitYesButton")
        self.QuitYesButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.QuitNoButton = QtWidgets.QPushButton(self.QuitScreen)
        self.QuitNoButton.setGeometry(QtCore.QRect(420, 240, self.buttonWidth, self.buttonHeight))
        self.QuitNoButton.setObjectName("QuitNoButton")
        self.QuitNoButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.stackedWidget.addWidget(self.QuitScreen)

        self.ProgressScreen = QtWidgets.QWidget()
        self.ProgressBackground = QtWidgets.QLabel(self.ProgressScreen)
        self.ProgressBackground.setGeometry(QtCore.QRect(0, 0, 801, 612))
        self.ProgressBackground.setPixmap(QPixmap("sprites/Plain.png"))
        self.ProgressBackground.setScaledContents(True)
        self.ProgressBackground.setObjectName("DiffBackground")
        self.ProgressScreen.setObjectName("ProgressScreen")
        self.GoodJobText = QtWidgets.QLabel(self.ProgressScreen)
        self.GoodJobText.setGeometry(QtCore.QRect(370, 90, 261, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.GoodJobText.setFont(font)
        self.GoodJobText.setObjectName("GoodJobText")
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
        self.ProgressContinueButton = QtWidgets.QPushButton(self.ProgressScreen)
        self.ProgressContinueButton.setGeometry(QtCore.QRect(370, 430, self.buttonWidth, self.buttonHeight))
        self.ProgressContinueButton.setObjectName("ProgressContinueButton")
        self.ProgressContinueButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.stackedWidget.addWidget(self.ProgressScreen)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.update_gui()
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_gui(self):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        item.setText(_translate("MainWindow", "Team 2"))
        item = self.GroupTable.item(2, 0)
        item.setText(_translate("MainWindow", "Team 4"))
        item = self.GroupTable.item(3, 0)
        item.setText(_translate("MainWindow", "Team 5"))
        item = self.GroupTable.item(4, 0)
        item.setText(_translate("MainWindow", "Team 3"))
        self.GroupTable.setSortingEnabled(__sortingEnabled)
        self.QuitYesButton.setText(_translate("MainWindow", "Yes"))
        self.QuitNoButton.setText(_translate("MainWindow", "No"))
        self.GoodJobText.setText(_translate("MainWindow", "Good job!"))
        self.PointsLabel.setText(_translate("MainWindow", "Points: %s" % self.game.currentPoints))
        self.TimeLabel.setText(_translate("MainWindow", "Time: Insert time instead"))
        self.StreakLabel.setText(_translate("MainWindow", "Streak: %s" % self.game.currentStreak))
        self.GSPointsLabel.setText(_translate("MainWindow", "Points: %s" % self.game.currentPoints))
        self.GSTimeLabel.setText(_translate("MainWindow", "Time: Insert time instead"))
        self.GSStreakLabel.setText(_translate("MainWindow", "Streak: %s" % self.game.currentStreak))
        self.ProgressContinueButton.setText(_translate("MainWindow", "Continue"))


if __name__ == "__main__":

    # set up GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    bt = BilaTurtle(MainWindow)
    bt.setup_gui()

    # launch app
    MainWindow.show()

    # there is no returning from this
    sys.exit(app.exec_())
