"""Plotting is used to display a very basic map of the environment
"""

import time
import math

class Item(object):
    
    def __init__(self,x,y,marker,code):
        self.x = x
        self.y = y
        self.marker = marker
        self.code = code

    def __eq__(self,other):
        return self.code == other.code

    def __ne__(self,other):
        return self.code != other.code

class Plotting(object):

    def __init__(self):
        self.clearPlot()

    def clearPlot(self):
        """Clear all items from the plotting environment"""

        self.xMax = 0
        self.yMax = 0
        self.items = set([])

    def addItem(self,x,y,marker='o',code=None):
        """Add an item to the plotting environment"""

        if (code is None):
            code = time.time()

        if (x > self.xMax): self.xMax = x
        if (y > self.yMax): self.yMax = y

        self.items.add(Item(x,y,marker,code))

    def addMarkers(self):
        """Add a line of a particular length
        """

        marker = 'x'
        gap = 1000
        walls = [
            [0,0,0],
            [0,0,math.pi/2],
            [0,8000,0],
            [8000,0,math.pi/2]
        ]

        for wall in walls:
            for step in range(1,8):
                x = wall[0] + math.cos(wall[2]) * gap * step
                y = wall[1] + math.sin(wall[2]) * gap * step
                # print(x,y)
                self.addItem(x,y,marker)

    def plot(self,width=80,height=40):
        """Plot all items in memmory onto a 
        """

        plotMap = []
        plotMap += [['_'] * (width + 1)]

        for i in range(height-1):
            plotMap += [['|'] + ([' '] * (width - 1)) + ['|']]

        plotMap += [['_'] * (width + 1)]

        for item in self.items:
            line = int(height * (self.yMax - item.y) / self.yMax )
            char = int(width * (item.x / self.xMax))
            plotMap[line][char] = item.marker

        for line in plotMap:
            print(''.join(line))


if (__name__ == "__main__"):

    plot = Plotting()
    plot.addMarkers()
    plot.plot()