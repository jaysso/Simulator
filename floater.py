# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage


from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey):
    radius = 5
    def __init__(self, x, y):
        Prey.randomize_angle(self)  # Ball for random angles
        Prey.__init__(self, x, y, 10, 10, Prey.get_angle(self), 5)

    def update(self, model):
        if random() > .8:
            speed = 5*random()
            if speed < 3:
                speed = 3
            elif speed > 7:
                speed = 7
            angle = random() - random()
            if angle > 0.5:
                angle = 0.5
            elif angle < -0.5:
                angle = 0.5
            Prey.set_speed(self,speed)
            Prey.set_angle(self,Prey.get_angle(self)+angle)
        Prey.move(self)

    def display(self, canvas):
        x, y = self.get_location()
        canvas.create_oval(x - Floater.radius, y - Floater.radius,
                           x + Floater.radius, y + Floater.radius,
                           fill="red")
