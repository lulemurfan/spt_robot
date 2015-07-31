import time
from sr.robot import *

R = Robot()

def drive(speed, seconds):

    steps = 10
    for tick in range(steps):
        R.motors[0].m0.power = float( tick * speed ) / steps
        R.motors[0].m1.power = float( tick * speed ) / steps
        time.sleep(1.0/steps)

    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def testDrive():
    """This tests different durations at 40 and 60 speed
    """

    for speed in [40,60]:
        for seconds in [2,4,8,16]:
            print("Testing driving straight at speed {} for {} seconds".format(speed,seconds))
            drive(speed, seconds)
            time.sleep(2)
            drive(-speed, seconds)
            time.sleep(1)


def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def testTurn():
    """This tests different durations at 40 and 60 speed
    """

    for speed in [20,40]:
        for seconds in [1,2,4,8]:
            print("Testing turning at speed {} for {} seconds".format(speed,seconds))
            drive(speed, seconds)
            time.sleep(10)
            drive(-speed, seconds)
            time.sleep(5)

testDrive()
print "Sleeping for 20 seconds before turn test"
print "=" * 80
testTurn()