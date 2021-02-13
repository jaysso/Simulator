from collections import defaultdict

import controller
import model   # Use in update_all to pass update a reference to this module

#Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special

# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running     = False
cycle_count = 0
sim = set()
classType = None
simCount = 0
PreyObj = None
special_on = False
#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running,cycle_count,sim, simCount, classType
    running = False
    cycle_count = 0
    sim = set()
    classType = None
    simCount = 0


#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False


#tep just one update in the simulation
def step ():
    global running
    running = True
    update_all()
    display_all()
    running = False


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global classType, PreyObj, special_on
    allSims = all_sim(Black_Hole.__bases__[0])
    for name in allSims:
        if name.__name__ == kind:
            classType = name
        if name.__name__ == "Prey":
            PreyObj = name
    if kind == "Remove":
        classType = kind
    elif kind == "Special":
        if special_on == False:
            special_on = True
            for s in sim:
                if isinstance(s, Hunter):
                    x, y = s.get_location()
                    w, h = s.get_dimension()
                    specialOb = Special(x, y)
                    specialOb.set_dimension(w,h)
                    sim.add(specialOb)
                    controller.the_canvas.delete(s)
                    sim.remove(s)

        else:
            special_on = False
            for s in sim:
                if isinstance(s, Special):
                    x, y = s.get_location()
                    w, h = s.get_dimension()
                    hunterOb = Hunter(x, y)
                    hunterOb.set_dimension(w,h)
                    sim.add(hunterOb)
                    controller.the_canvas.delete(s)
                    sim.remove(s)


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    #Ball(self,x,y,width,height,angle,speed=5)
    global classType, PreyObj

    if classType == "Remove":
        for item in sim.copy():
            l_x, l_y = Ball.get_location(item)
            if round(x/20)*20 == round(l_x/20)*20 and round(y/20)*20== round(l_y/20)*20:
                # rounded to remove area precision when clicking
                controller.the_canvas.delete(item)
                sim.remove(item)
                remove(1)

    else:
        sim.add(classType(x,y))


#add simulton s to the simulation
def add(s):
    global simCount
    simCount = s
    

# remove simulton s from the simulation    
def remove(s):
    global simCount
    simCount -= s


#find/return a set of simultons that each satisfy predicate p
def find(p):
    simSet = []
    for s in sim:
        if p(s):
                simSet.append(s)
    return simSet


#call update for every simulton in this simulation (passing model to each) 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count, sim, running
    if running:
        cycle_count += 1
        for s in sim.copy():
            s.update(model)


#For animation: (1) delete every simulton on the canvas; (2) call display on
#  each simulton being simulated, adding it back to the canvas, possibly in a
#  new location; (3) update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
        add(o)

    for s in sim:
        s.display(controller.the_canvas)

    controller.the_progress.config(text=str(cycle_count) + " updates/" + str(len(sim)) + " simultons")

def all_sim(cls): # for finding all subclasses of Simultion
    simulations = []
    for sim in cls.__subclasses__():
        simulations.append(sim)
        simulations.extend(all_sim(sim))
    return set(simulations)
