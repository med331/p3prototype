# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import time
from math import floor

from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread

from PyQt5.QtGui import QImage, QPixmap
from game import Game
import sys
import cv2

import random


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, game):
        self.game = game
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.buttonWidth = 100
        self.buttonHeight = 50
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 801, 581))
        self.stackedWidget.setObjectName("stackedWidget")

        self.GameScreen = QtWidgets.QWidget()
        self.GameScreen.setObjectName("GameScreen")
        self.GameScreenProgressBar = QtWidgets.QProgressBar(self.GameScreen)
        self.GameScreenProgressBar.setGeometry(QtCore.QRect(660, 10, 118, 23))
        self.GameScreenProgressBar.setProperty("value", 24)
        self.GameScreenProgressBar.setObjectName("GameScreenProgressBar")
        self.GameScreenButton1 = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenButton1.setGeometry(QtCore.QRect(20, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenButton1.setObjectName("GameScreenButton1")
        self.GameScreenButton1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.GameScreenQuit = QtWidgets.QPushButton(self.GameScreen)
        self.GameScreenQuit.setGeometry(QtCore.QRect(670, 500, self.buttonWidth, self.buttonHeight))
        self.GameScreenQuit.setObjectName("GameScreenButton1")
        self.GameScreenQuit.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.GameBilaturtle = QtWidgets.QLabel(self.GameScreen)
        self.GameBilaturtle.setGeometry(QtCore.QRect(290, 340, 200, 220))
        self.GameBilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
        self.GameBilaturtle.setScaledContents(True)
        self.GameBilaturtle.setObjectName("GameBilaturtle")
        self.GameLeftHand = QtWidgets.QLabel(self.GameScreen)
        self.GameLeftHand.setGeometry(QtCore.QRect(290, 340, 200, 220))
        self.GameLeftHand.setPixmap(QPixmap("sprites/sideways_left_hand.png"))
        self.GameLeftHand.setScaledContents(True)
        self.GameLeftHand.setObjectName("GameLeftHand")
        self.GameRightHand = QtWidgets.QLabel(self.GameScreen)
        self.GameRightHand.setGeometry(QtCore.QRect(290, 340, 200, 220))
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
        self.StartButton.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(0))
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

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
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
        self.PointsLabel.setText(_translate("MainWindow", "Points: Insert points instead"))
        self.TimeLabel.setText(_translate("MainWindow", "Time: Insert time instead"))
        self.StreakLabel.setText(_translate("MainWindow", "Streak: Insert streak instead"))
        self.GSPointsLabel.setText(_translate("MainWindow", "Points: %s" % game.is_holding_turtle))
        self.GSTimeLabel.setText(_translate("MainWindow", "Time: Insert time instead"))
        self.GSStreakLabel.setText(_translate("MainWindow", "Streak: Insert streak instead"))
        self.ProgressContinueButton.setText(_translate("MainWindow", "Continue"))
        if game.two_hands_in_frame:
            try:
                self.Bilaturtle.setGeometry(QtCore.QRect(game.hands[0].x, game.hands[0].y, 200, 220))
                if game.is_holding_turtle:
                    self.GameBilaturtle.setGeometry(
                        QtCore.QRect(game.middle_point[0] - 50, game.middle_point[1] - 55, 100, 110))
                    # TODO: draw hand_tile
                else:
                    x_position = 150 + floor((500 / 3) * game.field.turtleXPosition)
                    self.GameBilaturtle.setGeometry(
                        QtCore.QRect(x_position - 50, 250, 100, 110))

                # TODO: this is debugging only
                '''x_position = 150 + floor((500 / 3) * game.hand_tile)
                self.GameBilaturtle.setGeometry(
                    QtCore.QRect(x_position - 50, 250, 100, 110))'''

                # draw hands
                self.GameLeftHand.setGeometry(
                    QtCore.QRect(game.hands[0].x, game.hands[0].y, 200, 220))
                self.GameRightHand.setGeometry(
                    QtCore.QRect(game.hands[1].x, game.hands[1].y, 200, 220))
            except:
                pass

            #TODO: draw the game field
            for x in range(len(game.field.fieldArray)):
                for y in range(len(game.field.fieldArray[x])):
                    pos_x = 200 + x * (50 * (x - 1))
                    pos_y = 200 + y * (50 * (y - 1))
                    new_tiles = int((time.time() - game.startTime) - game.speed)
                    pos_y = pos_y - (new_tiles * 10)

                    '''self.GameBilaturtle = QtWidgets.QLabel(self.GameScreen)
                    self.GameBilaturtle.setGeometry(QtCore.QRect(290, 340, 200, 220))
                    self.GameBilaturtle.setPixmap(QPixmap("sprites/Turtle.png"))
                    self.GameBilaturtle.setScaledContents(True)
                    self.GameBilaturtle.setObjectName("GameBilaturtle")'''

                    # draw appropriate sprite
                    type = game.field.fieldArray[x][y]
                    new_sprite = QtWidgets.QLabel(self.GameScreen)
                    new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                    #new_sprite.setText("Peter is a douchebag")
                    print("x: %s and y: %s" % (pos_x, pos_y))
                    if type == 0 or type == 1:
                        # TODO: draw nothing
                        new_sprite.setPixmap(QPixmap("sprites/Plain.png"))
                        new_sprite.setScaledContents(True)
                        new_sprite.setObjectName("PlainTile%s%s" % (x, y))
                        pass
                    if type == 1:
                        new_sprite = QtWidgets.QLabel(self.GameScreen)
                        new_sprite.setGeometry(QtCore.QRect(pos_x, pos_y, 200, 200))
                        new_sprite.setPixmap(QPixmap("sprites/Carrot.png"))
                        new_sprite.setScaledContents(True)
                        new_sprite.setObjectName("Pickup%s%s" % (x, y))
                        # TODO: draw pickupsF
                        pass
                    elif type == 2:
                        new_sprite.setPixmap(QPixmap("sprites/Seagull.png"))
                        new_sprite.setScaledContents(True)
                        new_sprite.setObjectName("Seagull%s%s" % (x, y))
                        # TODO: draw seaguls
                        pass
                    else:
                        new_sprite.setPixmap(QPixmap("sprites/Lake.png"))
                        new_sprite.setScaledContents(True)
                        new_sprite.setObjectName("River%s%s" % (x, y))
                        # TODO: draw water
                        pass


class UpdateThread(Thread):

    def __init__(self, main_window, main_main_window, game):
        super().__init__()
        self.main_window = main_window
        self.main_main_window = main_main_window
        self.game = game

    def run(self):

        # initialize game
        game.start()

        # initialize OpenCV and webcam capture
        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 600)

        while True:
            if game.hasFinished:
                continue
            # read a frame from the webcam and pass it on to the game (GestureEngine)
            frame = cap.read()[1]
            game.update(frame)
            self.main_window.retranslateUi(self.main_main_window)  # updates the entire gui


if __name__ == "__main__":

    game = Game()

    # set up GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, game)

    # set up game-updating thread
    t = UpdateThread(ui, MainWindow, game)

    # launch app
    MainWindow.show()
    t.start()

    # there is no returning from this
    sys.exit(app.exec_())
