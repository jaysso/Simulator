# The Black_Hole class is derived from Simulton. It updates by finding/removing
#   any class derived from Prey whose center is contained within its radius
#  (returning a set of all eaten simultons), and
#   displays as a black circle with a radius of 10
#   (width/height 20).
# Calling get_dimension for the width/height (for
#   containment and displaying) will facilitate
#   inheritance in Pulsator and Hunter

from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    radius = 10
    def __init__(self, x, y):
        Simulton.set_dimension(self, 20, 20)
        w, h = Simulton.get_dimension(self)
        Simulton.__init__(self,x,y,w,h)
        self.eaten = 0
        self.eatenSet = set()

    def update(self, model):
        allPrey = model.find(lambda x: isinstance(x, Prey))
        w,h = self.get_dimension()
        for prey in allPrey:
            if self.distance((Simulton.get_location(prey))) < w/2: # width == height
                model.controller.the_canvas.delete(prey)
                model.sim.remove(prey)
                self.eatenSet.add(prey)
                self.eaten += 1
        return self.eatenSet

    def display(self, canvas):
        x, y = self.get_location()
        w, h = self.get_dimension()
        canvas.create_oval(x - w/2, y - h/2,
                           x + w/2, y + h/2,
                           fill="black")

    def __contains__(self, item):
        return self.distance((Simulton.get_location(item))) < Black_Hole.radius


