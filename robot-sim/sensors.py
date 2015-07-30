"""Sensors provides a number of methods to check if sensors are broken
"""

import time
DEBUG = True

class Sensor(object):
    "Genral class for interaction with sensors"

    def __init__(self,R,sensorIndex,ardinoIndex=0):
        self.R = R
        self.ardinoIndex = ardinoIndex
        self.sensorIndex = sensorIndex

    def getReading(self):
        reading =  R.ruggeduinos[0].analogue_read(0)
        if DEBUG: 
            print('Sensor {} reading is {} ({})'.format(
                self.sensorIndex,
                reading,
                self.__class__))
        return reading


class BumpSensor(Sensor):
    "Class to deal with bump sensors"
    def isBump(self):
        return (self.getReading > 2)
        
class LightSensor(Sensor):
    "Class to deal with light sensors"
    def isBroken(self):
        return (self.getReading > 2)



class Sensors(object):

    def __init__(self,R):
        """Set the robot
        """

        self.lightSensor = LightSensor(R,0)
        self.rightBump = BumpSensor(R,1)
        self.leftBump = BumpSensor(R,2)

    def __repr__(self):

        output = ""
        output += "LightSensor: {} ({}) - ".format(self.lightSensor.isBroken(),self.lightSensor.getReading())
        output += "RightBump: {} ({}) - ".format(self.rightBump.isBumped(),self.rightBump.getReading())
        output += "LeftBump: {} ({})".format(self.leftBump.isBumped(),self.leftBump.getReading())
        return output

def test():
    from sr.robot import *
    global R
    R = Robot()
    sensors = Sensors(R)
    while True:
        print(sensors)
        time.sleep(0.2)


# This is HACKEY
try:
    test()
except Exception as error:
    print error