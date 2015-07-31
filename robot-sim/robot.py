from sr.robot import *
# from sensors import Sensors
from challenge import Challenge

class State(object):

    def __init__(self):
        self.home = True
        self.searching = False
        self.homing = False
        self.retrieving = False

    def search(self):
        self.home = False
        self.searching = True
        self.homing = False
        self.retrieving = False

    def home(self):
        self.home = False
        self.searching = True
        self.homing = False
        self.retrieving = False

    def search(self):
        self.home = False
        self.searching = True
        self.homing = False
        self.retrieving = False

R = Robot()