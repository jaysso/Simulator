# The Hunter class is derived from Pulsator (1st) and the Mobile_Simulton (2nd).
#   It updates/displays like its Pulsator base, but also moves (either in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.


from prey  import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):
    def __init__(self, x, y):
        Mobile_Simulton.randomize_angle(self)
        Pulsator.__init__(self,x,y)
        Mobile_Simulton.set_speed(self, 5)

    def update(self, model):
        Pulsator.update(self, model)
        nearbyPrey = model.find(lambda x: isinstance(x, Prey) and self.distance((x.get_location())) <= 200)
        toSort = []
        for prey in nearbyPrey:
            toSort.append((prey, self.distance((prey.get_location()))))
        if toSort != []:
            prey_to_chase = min(toSort, key=lambda x:x[1])
            xp, yp = Prey.get_location(prey_to_chase[0])
            xh, yh = self.get_location()
            diff_y = yp-yh
            diff_x = xp-xh
            self.set_angle(atan2(diff_y, diff_x))
        Mobile_Simulton.move(self)


