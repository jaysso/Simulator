# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions


from blackhole import Black_Hole


class Pulsator(Black_Hole):
    count = 30
    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.counter = Pulsator.count
        self.eatenNum = 0 # to keep previous size

    def update(self, model):
        self.counter -= 1
        Black_Hole.update(self, model)
        if self.counter == 0:
            self.change_dimension(-1,-1)
            w, h = self.get_dimension()
            self.counter = 30
            if w == 0 and h == 0:
                model.controller.the_canvas.delete(self)
                model.sim.remove(self)


        elif self.eatenNum < self.eaten:
            ate = self.eaten - self.eatenNum
            self.eatenNum = self.eaten
            Black_Hole.change_dimension(self, ate, ate)
            self.counter = 30
