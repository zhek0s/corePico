from picozero import Button

class Buttons:
    
    def __init__(self):
        centerB = Button(22)
        upB = Button(4)
        downB = Button(5)
        leftB = Button(6)
        rightB = Button(7)
        centerB.when_pressed = self.centerPressed
        centerB.when_released = self.centerReleased
        upB.when_pressed = self.upPressed
        upB.when_released = self.upReleased
        downB.when_pressed = self.downPressed
        downB.when_released = self.downReleased
        leftB.when_pressed = self.leftPressed
        leftB.when_released = self.leftReleased
        rightB.when_pressed = self.rightPressed
        rightB.when_released = self.rightReleased
        
    def centerPressed(self):
        print("center pressed")
        
    def centerReleased(self):
        print("center released")
        
    def upPressed(self):
        print("up pressed")
        
    def upReleased(self):
        print("up released")
        
    def downPressed(self):
        print("down pressed")
        
    def downReleased(self):
        print("down released")
        
    def leftPressed(self):
        print("left pressed")
        
    def leftReleased(self):
        print("left released")
        
    def rightPressed(self):
        print("right pressed")
        
    def rightReleased(self):
        print("right released")
        
    def but_p(self):
        print("but")