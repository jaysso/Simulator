
# Hunter gone ROGUE! Same features of shrinking as normal hunters, however, it can
# Eat anything smaller than it and changes color (light blue/pink) every 20 cycles!



from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2

class Special(Pulsator, Mobile_Simulton):
        #changing size of balls
        def __init__(self, x, y):
            self.count = 40
            Mobile_Simulton.randomize_angle(self)
            Pulsator.__init__(self, x, y)
            Mobile_Simulton.set_speed(self, 12)


        def update(self, model):
            self.count -= 1
            Pulsator.update(self, model)
            nearbyPrey = model.find(lambda x: self.is_larger(x) and self.distance((x.get_location())) <= 200)
            toSort = []
            for prey in nearbyPrey:
                toSort.append((prey, self.distance((prey.get_location()))))
            if toSort != []:
                prey_to_chase = min(toSort, key=lambda x: x[1])
                xp, yp = prey_to_chase[0].get_location()
                xh, yh = self.get_location()
                diff_y = yp - yh
                diff_x = xp - xh
                self.set_angle(atan2(diff_y, diff_x))
            self.move()
            w, h = self.get_dimension()
            for prey in nearbyPrey:
                if self.distance((prey.get_location())) < w / 2:  # width == height
                    model.controller.the_canvas.delete(prey)
                    model.sim.remove(prey)
                    self.eatenSet.add(prey)
                    self.eaten += 1
            if self.count == 0:
                self.count = 40


        def display(self, canvas):
                x, y = self.get_location()
                w, h = self.get_dimension()

                if self.count >= 20:
                    canvas.create_oval(x - w / 2, y - h / 2,
                                       x + w / 2, y + h / 2,
                                       fill="LightBlue2")
                elif self.count < 20:
                    canvas.create_oval(x - w / 2, y - h / 2,
                                       x + w / 2, y + h / 2,
                                       fill="pink")


        def is_larger(self, x):
            xh, yh = self.get_dimension()
            xp, yp = x.get_dimension()
            return xh > xp and yh > yp