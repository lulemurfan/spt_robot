from sr.robot import Robot

class Motion(object):

    def __init__(self):

        self.driveSpeed = 60
        self.turnSpeed = 40

        self.R = Robot()

    def setPower(self,powerL,powerR):
        """Set the motor power
        """

        R.motors[0].m0.power = powerL
        R.motors[1].m1.power = powerR

    def driveDistance(self,distance):
        """Drive a certain distance in milimeters and then return flow
        of control to parent, return True if drive complete else return
        False is collision
        """

    
        time = distance / 10.0

        steps = 10
        for tick in range(steps):
            powerL = float( tick * speed ) / steps
            powerR = float( tick * speed ) / steps
            self.setPower(powerL,powerR)
            time.sleep(1.0/steps)

        time.sleep(time - 1)
        self.setPower(0,0)

    def turnAngle(angle):
        """Turn by a particular angle in RADIANS where clockwise is
        positive, return True if turn complete else return False if
        there is a collision
        """

        steps = 10
        for tick in range(steps):
            powerL = float( tick * speed ) / steps
            powerR = float( tick * speed ) / steps
            self.setPower(powerL,powerR)
            time.sleep(1.0/steps)

        time.sleep(seconds)
        self.setPower(0,0)