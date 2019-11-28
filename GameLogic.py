class Turtle:
    isHeld = False
    xPosition = 0
    yPosition = 0
    zPosition = 0
    speed = 0

    def turtleMove(this,movetype = "forward"):
        if movetype == "forward": this.yPosition = this.yPosition + 1
        elif movetype == "left": this.xPosition = this.xPosition - 1
        elif movetype == "right": this.xPosition = this.xPosition + 1
        elif movetype == "up": this.zPosition = this.zPosition + 1


class GameObject:
    xPosition = 0
    yPosition = 0
    zPosition = 0
    isWide = False
    isPickup = False
    pointsWorth = 0

    def objectFunction (this,Bila):
         if this.isWide == True:
            if this.yPosition == Bila.yPosition and this.zPosition == Bila.zPosition:
                GameScreen.currentStreak = 0
         else:
            if this.xPosition == Bila.xPosition and this.yPosition == Bila.yPosition and this.zPosition == Bila.zPosition:
                if this.isPickup == True:
                   GameScreen.currentStreak +=1
                   GameScreen.currentPoints += this.pointsWorth

                else: GameScreen.currentStreak = 0

class GameScreen:
    currentStreak = 0
    currentPoints = 0