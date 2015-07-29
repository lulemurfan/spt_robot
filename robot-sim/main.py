from sr.robot import *
from random import random

import time

SEARCHING, DRIVING = range(2)
movement = []
MARKER_TYPE = 0

R = Robot()

token_filter = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER)
token_filter_g = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD)
token_filter_s = lambda m: m.info.marker_type in (MARKER_TOKEN_SLIVER)


def drive(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
	addMove({'m':"F",'sp':speed, 'sec':seconds})

def turn(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0
	addMove({'m':"t",'sp':speed, 'sec':seconds})

def getMarkers():
	if MARKER_TYPE == 0:
		return filter(token_filter, R.see())
	if MARKER_TYPE == "token_silver":
		return filter(token_filter_s, R.see())
	elif MARKER_TYPE == "token_gold":
		return filter(token_filter_g, R.see())
		



def nearestMarker(markers):
	'''
	Find the nearest marker
	'''
	minDist = markers[0].centre.polar.length
	minMarker = 0
	i = 0
	for m in markers:
		if m.centre.polar.length < minDist:
			minDist = m.centre.polar.length
			minMarker = i
		i+=1
#	print len(markers), i
#	print "Heading towards marker", markers[minMarker].info.code
	return markers[minMarker]


def rotateToNearest(speed,sec,err):
	m = getMarkers()
	if nearestMarker(m).centre.polar.rot_y > err:
		while (nearestMarker(m).centre.polar.rot_y > err):
			m = getMarkers()
			print nearestMarker(m).centre.polar.rot_y
			turn(speed,sec)
	elif nearestMarker(m).centre.polar.rot_y < -err:
		while (nearestMarker(m).centre.polar.rot_y < -err):
			m = getMarkers()
			print nearestMarker(m).centre.polar.rot_y
			turn(-speed,sec)
	return nearestMarker(m)

def collect():
	'''
	Now token is in range pick it up
	'''
	global MARKER_TYPE
	MARKER_TYPE = rotateToNearest(5,0.01,0.05)
	print "Looking for", MARKER_TYPE.info.marker_type
	drive(100,0.1)
	
	
def addMove(move):
	movement.append(move)
	


while nearestMarker(getMarkers()).dist > 0.5:
	rotateToNearest(25,0.01,0.5)
	print "F to",nearestMarker(getMarkers()).info.code, " - Distance", nearestMarker(getMarkers()).dist
	drive(100,0.5)
print "Found marker"
collect()
print movement


print "END"	
exit()
