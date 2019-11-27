"""
        Game must maintain the game state and handle the logic of the game itself
"""

import random
from src.gesture_engine import GestureEngine

class GameField:  # 0: empty field 1:pickup 2:seagull 3:river
    sizeX = 4
    sizeY = 6
    fieldArray = []
    for i in range(sizeX):  # reset the bottom row
        fieldArray.append([0] * sizeY)

    #def __init__(self):


    def moveField(self):  # move all fields
        for x in range(len(self.fieldArray)):
            self.fieldArray[x][0] = 0
        for x in range(len(self.fieldArray)):
            for y in range(1, len(self.fieldArray[x])):
                self.fieldArray[x][y - 1] = self.fieldArray[x][y]
        self.generateRow(self)

    def generateRow(self):  # generate new row
        if random.randint(0, 10) == 1:  # roll for river
            for x in range(len(self.fieldArray)):
                self.fieldArray[x][self.sizeY - 1] = 3
        else:
            for x in range(len(self.fieldArray)):
                result = random.randint(0, 4)
                if result == 0:
                    self.fieldArray[x][self.sizeY - 1] = 1
                elif result == 1:
                    self.fieldArray[x][self.sizeY - 1] = 2
                else:
                    self.fieldArray[x][self.sizeY - 1] = 0

    def checkField(self, bila):
        gameObject = self.fieldArray[bila.xPosition][bila.yPosition]
        if gameObject == 2 or gameObject == 3:
            if bila.zPosition == 0:
                Game.currentStreak = 0
        elif gameObject == 1:
            if bila.zPosition == 0:
                Game.currentStreak += 1
                Game.currentPoints += 10

    def display(self):
        for x in range(6):
            self.generateRow(self)
            self.moveField(self)
        for x in range(self.sizeX):
            print(self.fieldArray[x])


class Game(GestureEngine):  # please see tests/test_game for how to test your code
    currentStreak = 0
    currentPoints = 0
    field = GameField

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


class Turtle:
    isHeld = False
    xPosition = 0
    # yPosition = 0
    zPosition = 0
    speed = 0

    def turtleMove(self, movetype="forward"):
        if movetype == "forward":
            self.yPosition = self.yPosition + 1
        elif movetype == "left":
            self.xPosition = self.xPosition - 1
        elif movetype == "right":
            self.xPosition = self.xPosition + 1
        elif movetype == "up":
            self.zPosition = self.zPosition + 1


class GameObject:
    # xPosition = 0
    # yPosition = 0
    # zPosition = 0
    isWide = False
    isPickup = False
    pointsWorth = 0

    def objectFunction(self, Bila):
        if self.isWide == True:
            if self.yPosition == Bila.yPosition and self.zPosition == Bila.zPosition:
                Game.currentStreak = 0
        else:
            if self.xPosition == Bila.xPosition and self.yPosition == Bila.yPosition and self.zPosition == Bila.zPosition:
                if self.isPickup == True:
                    Game.currentStreak += 1
                    Game.currentPoints += self.pointsWorth

                else:
                    Game.currentStreak = 0


