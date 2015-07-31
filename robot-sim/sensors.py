"""Sensors provides a number of methods to check if sensors are broken
"""

import time

from sr.robot import *
R = Robot()

class Sensor(object):
    "Genral class for interaction with sensors"

    def __init__(self,R,sensorIndex,ardinoIndex=0):
        self.R = R
        self.ardinoIndex = ardinoIndex
        self.sensorIndex = sensorIndex
        self.R.ruggeduinos[ardinoIndex].pin_mode(sensorIndex, INPUT)

    def getReading(self):
        return self.R.ruggeduinos[self.ardinoIndex].analogue_read(self.sensorIndex)


class BumpSensor(Sensor):
    "Class to deal with bump sensors"
    def isBump(self):
        return (self.getReading() > 2)
        
class LightSensor(Sensor):
    "Class to deal with light sensors"
    def isBroken(self):
        return (self.getReading() > 2.84)



class Sensors(object):

    def __init__(self,R):
        """Set the robot
        """

        self.lightSensor = LightSensor(R,0)
        self.rightBump = BumpSensor(R,3)
        self.leftBump = BumpSensor(R,2)
        self.centreBump = BumpSensor(R,1)

    def __repr__(self):

        output = ""
        output += "LightSensor: {} ({}) - ".format(self.lightSensor.isBroken(),self.lightSensor.getReading())
        output += "RightBump: {} ({}) - ".format(self.rightBump.isBump(),self.rightBump.getReading())
        output += "LeftBump: {} ({})".format(self.leftBump.isBump(),self.leftBump.getReading())
        output += "CentreBump: {} ({})".format(self.centreBump.isBump(),self.centreBump.getReading())
        return output

sensors = Sensors(R)

# t check if if lishg sensor browken
sensors.lightSensor.isBroken()

#check if bump switch hit
sensors.rightBump.isBump()

while True:
    print(sensors)

    time.sleep(0.2)
