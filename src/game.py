"""
        Game must maintain the game state and handle the logic of the game itself
"""

import time
import random
from gesture_engine import GestureEngine


class GameField:  # 0: empty field 1:pickup 2:seagull 3:river 4:turtle
    sizeX = 4
    sizeY = 6
    fieldArray = []
    turtleXPosition = int(sizeX / 2)
    turtleZPosition = 0
    difficulty = 0
    riverChance = 7
    seagullChance = 7
    pickupChance = 8

    def __init__(self, _difficulty):
        self.difficulty = _difficulty+1
        self.riverChance = self.riverChance * self.difficulty
        self.seagullChance = self.seagullChance * self.difficulty
        for i in range(self.sizeX):  # reset the bottom row
            self.fieldArray.append([0] * self.sizeY)
        #self.fieldArray[self.turtleXPosition][0] = 4  # place the turtle

    def moveTurtle(self, _input):
        self.turtleZPosition = 0
        if _input == "Left":
            if self.turtleXPosition>0:
                self.turtleXPosition-=1
        elif _input == "Right":
            if self.turtleXPosition<self.sizeX-1:
                self.turtleXPosition+=1
        elif _input == "Jump":
            self.turtleZPosition+=1

    def moveField(self):  # move all fields
        for x in range(len(self.fieldArray)):
            self.fieldArray[x][0] = 0
        for x in range(len(self.fieldArray)):
            for y in range(1, len(self.fieldArray[x])):
                self.fieldArray[x][y - 1] = self.fieldArray[x][y]
        self.generateRow()
        self.fieldArray[self.turtleXPosition][0] = 4  # place the turtle

    def generateRow(self):  # generate new row
        chance = random.randint(0, 100)
        print("New tiles were generated")
        if chance < self.riverChance and self.fieldArray[0][self.sizeY-2] != 3:  # roll for river
            for x in range(len(self.fieldArray)):
                self.fieldArray[x][self.sizeY - 1] = 3
        else:
            for x in range(len(self.fieldArray)):
                chance = random.randint(self.riverChance, 100)
                if chance < self.riverChance+self.seagullChance and ((self.fieldArray[x-1][self.sizeY-1] != 2) if x > 0 else True) and ((self.fieldArray[x+1][self.sizeY-1] != 2) if x < self.sizeX-1 else True) and (self.fieldArray[x][self.sizeY-2] != 2 and self.fieldArray[x][self.sizeY-3] != 2):
                    self.fieldArray[x][self.sizeY - 1] = 2
                elif chance < self.riverChance+self.seagullChance+self.pickupChance:
                    self.fieldArray[x][self.sizeY - 1] = 1
                else:
                    self.fieldArray[x][self.sizeY - 1] = 0

    def checkTurtleField(self):
        gameObject = self.fieldArray[self.turtleXPosition][0]
        if gameObject == 2 or gameObject == 3:
            if self.turtleZPosition == 0:
                Game.currentStreak = 0
        elif gameObject == 1:
            if self.turtleZPosition == 0:
                Game.currentStreak += 1
                Game.currentPoints += 10

    def display(self):  # display the field for testing purposes
        for y in range(self.sizeY-1, -1, -1):
            print("[", end='')
            for x in range(self.sizeX):
                print(self.fieldArray[x][y], end=' ')
            print("]")
        print("")

    def setup(self):
        for x in range(self.sizeY):
            self.moveField()
            self.generateRow()


class Game(GestureEngine):  # please see tests/test_game for how to test your code
    currentStreak = 0
    currentPoints = 0
    difficulty = 1  # difficulty (the higher the harder, 1 to 5)
    speed = 0.6  # how many seconds in between movements
    field = GameField(difficulty)
    kbPressed = 0
    last_is_holding_turtle = False

    def __init__(self):
        super(Game, self).__init__()  # calling GestureEngine constructor
        self.hasFinished = True
        self.startTime = 0

    def start(self):
        self.hasFinished = False
        self.field.setup()
        self.startTime = time.time()

    def stop(self):
        self.hasFinished = True
        # TODO: Implement the rest

    def update(self, frame):

        print(self.is_holding_turtle)  # debugging

        # process updates from GestureEngine
        self.process_frame(frame)
        if self.two_hands_in_frame:
            # TODO: maybe pause the game if this is not the case
            print(self.middle_point)
            hand_tile = round((4 / 100) * self.middle_point[0])  # what tile the hand is currently over
            if self.last_is_holding_turtle and not self.is_holding_turtle:  # register turtle pickup
                if hand_tile == self.field.turtleXPosition:
                    # TODO: in this case, the turtle should be rendered on the middle_point and not the tiles
                    self.field.moveTurtle("Jump")
            if not self.last_is_holding_turtle and self.is_holding_turtle:  # register turtle drop
                self.field.turtleXPosition = hand_tile
                self.field.turtleZPosition = 0
            self.last_is_holding_turtle = self.is_holding_turtle

        # update playing field after a specific amount of time
        if time.time() - self.startTime >= self.speed:
            self.startTime = time.time()
            self.field.moveField()

            # TODO: debugging
            movement = random.randint(0, 1)
            if movement == 0:
                self.field.moveTurtle("Left")
            elif movement == 1:
                self.field.moveTurtle("Right")
            self.field.checkTurtleField()
