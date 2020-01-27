import time
import random
from math import floor

from src.gesture_engine import GestureEngine


class GameField:
    """
        THE CLASS THAT MAINTAINS THE GAME FIELD
    """

    sizeX = 4                         # the horizontal size of the game field
    sizeY = 6                         # the vertical sixe og the game field
    fieldArray = []                   # the array of field tiles
    turtleXPosition = int(sizeX / 2)  # the x position of the turtle, which must be between 0 and sizeX - 1
    turtleZPosition = 0               # the z position of the turtle, 0 = on ground, 1 = picked up
    difficulty = 0                    # the difficulty setting of the game
    riverChance = 7                   # the preset chance of rivers spawning (water tiles covering one x-wise lane)
    seagullChance = 7                 # the preset chance of seagulls spawning
    pickupChance = 8                  # the preset chance of a pickup spawning

    def __init__(self, _difficulty):
        self.difficulty = _difficulty+1                            # set initial difficulty
        self.riverChance = self.riverChance * self.difficulty      # update river chance according to given difficulty
        self.seagullChance = self.seagullChance * self.difficulty  # update seagull chance according to given difficulty
        for i in range(self.sizeX):
            # always override the bottom row to be grass tiles
            self.fieldArray.append([0] * self.sizeY)

    def move_turtle(self, index):
        """Move the turtle to provided position

        This method safeguards from out-of-bounds exceptions by not allowing movement outside of provided boundaries"""

        if index >= self.sizeX:
            # if the provided index is further to the right than allowed, default to the right-most tile
            self.turtleXPosition = self.sizeX - 1
        elif index < 0:
            # if the provided index is further to the left than allowed, defualt to the left-most tile
            self.turtleXPosition = 0
        else:
            # otherwise, move the turtle according to the provided index
            self.turtleXPosition = index

    def move_field(self):
        """Moves all fields and generates a new row at the top"""

        # move all rows down by one
        for x in range(self.sizeX):
            self.fieldArray[x][0] = 0
        for x in range(self.sizeX):
            for y in range(1, self.sizeY):
                self.fieldArray[x][y - 1] = self.fieldArray[x][y]
        self.generate_row()  # generate the new row

    def generate_row(self):
        """Generates a new row

        This method generates a new row to go on top of the game field list, after the tiles have been moved over."""

        # generate new tiles semi-randomly
        chance = random.randint(0, 100)
        if chance < self.riverChance and self.fieldArray[0][self.sizeY-2] != 3:
            # generate new row as a river, if a river was rolled
            for x in range(len(self.fieldArray)):
                self.fieldArray[x][self.sizeY - 1] = 3
        else:
            # roll for individual tiles
            for x in range(len(self.fieldArray)):
                chance = random.randint(self.riverChance, 100)
                if chance < self.riverChance+self.seagullChance and ((self.fieldArray[x-1][self.sizeY-1] != 2) if x > 0 else True) and ((self.fieldArray[x+1][self.sizeY-1] != 2) if x < self.sizeX-1 else True) and (self.fieldArray[x][self.sizeY-2] != 2 and self.fieldArray[x][self.sizeY-3] != 2):
                    # a pickup was rolled
                    self.fieldArray[x][self.sizeY - 1] = 2
                elif chance < self.riverChance+self.seagullChance+self.pickupChance:
                    # a seagull was rolled
                    self.fieldArray[x][self.sizeY - 1] = 1
                else:
                    # a plain grass tile was rolled
                    self.fieldArray[x][self.sizeY - 1] = 0

        self.check_turtle_field()  # check the turtle position

    def check_turtle_field(self):
        """Checks the turtle position agains the tile that it currently stands on

        If the turtle sands on a pickup, it will gain points, if it collides with a seagull or a river, it will reset
        it's streak. Otherwise, in the case of a grass tile, nothing will happen."""

        turtle_tile_type = self.fieldArray[self.turtleXPosition][1]  # the tile type that the turtle inhabits
        if turtle_tile_type == 2 or turtle_tile_type == 3:
            # if the turtle collides with a seagull or a river, reset it's streak
            if self.turtleZPosition == 0:
                Game.currentStreak = 0
        elif turtle_tile_type == 1:
            if self.turtleZPosition == 0:
                # if the turtle stands on a carrot, increase it's points and streak
                Game.currentStreak += 1
                Game.currentPoints += 10
                self.fieldArray[self.turtleXPosition][1] = 0

    def display(self):
        """Display the current layout of tiles in the game field list

        NOTE: THIS MEHTOD IS ONLY FOR DEBUGGING PURPOSES"""

        # perform logic for drawing the two-dimensional array
        for y in range(self.sizeY-1, -1, -1):
            print("[", end='')
            for x in range(self.sizeX):
                print(self.fieldArray[x][y], end=' ')
            print("]")
        print("")

    def setup(self):
        """Setup the game field

        This is done by moving the field an generating a new row for the number of vertical rows"""
        for x in range(self.sizeY):
            # move the game field over by one and generate a new row
            self.move_field()
            self.generate_row()


class Game(GestureEngine):  # please see tests/test_game for how to test your code
    """
        THE CLASS THAT HANDLES THE GAME LOGIC, USING GESTURE ENGINE AND GAME FIELD
    """

    currentStreak = 0               # the accumulated streak during a game session
    currentPoints = 0               # the accumulated points during a game session
    difficulty = 1                  # difficulty (the higher the harder, 1 to 5 (can maybe go higher (don't try)))
    speed = 4                       # how many seconds in between movements
    field = GameField(difficulty)   # the game field containing and managing the tiles
    last_is_holding_turtle = False  # whether or not the user was holding the turtle on the last game update
    hand_tile = -2                  # an arbitrary value that keeps the turtle off the screen

    def __init__(self):
        super(Game, self).__init__()  # calling GestureEngine constructor
        self.hasFinished = True       # start the game off as finished
        self.update_time = 0          # used to keep time between specific game updates
        self.play_time = 0            # used to keep track of user play time

    def start(self):
        """Starts the game"""

        self.hasFinished = False        # game has no longer finished, because it is starting!
        self.field.setup()              # setup game field, generating a new list of tiles
        self.update_time = time.time()  # timestamp for further reference
        self.play_time = time.time()    # timestamp for further reference

    def stop(self):
        """Stops the game"""

        self.hasFinished = True  # declare the game as finished
        self.currentPoints = 0   # reset points
        self.currentStreak = 0   # reset streaks

    def change_difficulty(self, value):
        """Changes the difficulty of the game

        NOTE: this method does not safeguard the provided values, which means they must be verified by the caller!

        :param value: the new difficulty value, between 0 and 5
        """

        self.difficulty = value                  # set difficulty to new value
        self.field.difficulty = self.difficulty  # propagate this change to the game field aswell

    def get_elapsed_play_time(self):
        """Retrieves the how long the user has been playing the game

        :return: Seconds of playtime as an Integer value
        """

        return round(time.time() - self.play_time)

    def update(self, frame):
        """Updates the game state and gesture input

        :param frame: a new frame to analyze for gesture input
        """

        self.process_frame(frame)  # process gesture input

        if self.two_hands_in_frame:  # don't draw anything if there's no hands in the frame

            # track if the turtle is picked up or not
            self.hand_tile = floor((3 / 550) * self.middle_point[0])
            if not self.last_is_holding_turtle and self.is_holding_turtle:  # register turtle pickup
                if self.hand_tile == self.field.turtleXPosition:
                    self.field.turtleZPosition = 1  # 1 means the turtle picked up, and will not collide with obstacles
            if self.last_is_holding_turtle and not self.is_holding_turtle:  # register turtle drop
                self.field.move_turtle(self.hand_tile)  # move the turtle to where it was pit down
                self.field.turtleZPosition = 0  # trutle is no longer picked up, and can now collide with obstacles
            self.last_is_holding_turtle = self.is_holding_turtle is True  # force assignment by value

            # update playing field after a specific amount of time
            if time.time() - self.update_time >= self.speed:
                self.update_time = time.time()
                self.field.move_field()
