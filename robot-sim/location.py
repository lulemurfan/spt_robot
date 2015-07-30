"Location is a simple script to test the localisation set of functions"

import time
from localisation.plotting import Plotting

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def plot():
    P.addMarkers()
    P.plot()

P = Plotting()
R = Robot()

drive(10,10)
plot()
exit()