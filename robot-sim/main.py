from sr.robot import *
from random import random

import time

SEARCHING, DRIVING = range(2)
movement = []
MARKER_TYPE = 0
ZONES = {0: [0,27], 1:[6,7], 2: [13,14], 3: [20,21]}

R = Robot()

token_filter = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER)
token_filter_g = lambda m: m.info.marker_type == "token_gold"
token_filter_s = lambda m: m.info.marker_type == "token_silver"
arena_filter = lambda m: m.info.marker_type in (MARKER_ARENA)
home_filter = lambda m: m.info.code in ZONES[R.zone]



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

def getMarkers():
	print MARKER_TYPE
	if MARKER_TYPE == 0:
		return filter(token_filter, R.see())
	if MARKER_TYPE == "token_silver":
		return filter(token_filter_s, R.see())
	elif MARKER_TYPE == "token_gold":
		return filter(token_filter_g, R.see())
		
def getHomeMarkers():
	return nearestMarker(filter(home_filter,filter(arena_filter, R.see())))


def nearestMarker(markers):
	'''
	Find the nearest marker
	'''
	if markers == None or len(markers) == 0:
		raise ValueError('It was zero')
	if len(markers) == 1:
		return markers[0]
	if str(type(markers)) == "<class 'sr.robot.vision.Marker'>":
		return markers
	minDist = markers[0].dist
	minMarker = 0
	i = 0
	for m in markers:
		if m.dist < minDist:
			minDist = m.dist
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
	
def rotateToHomeMarker(speed,sec,err):
	m = getHomeMarkers()
	print nearestMarker(m)
	if nearestMarker(m).centre.polar.rot_y > err:
		while (nearestMarker(m).centre.polar.rot_y > err):
			m = getHomeMarkers()
			print nearestMarker(m).centre.polar.rot_y
			turn(speed,sec)
	elif nearestMarker(m).centre.polar.rot_y < -err:
		while (nearestMarker(m).centre.polar.rot_y < -err):
			m = getHomeMarkers()
			print nearestMarker(m).centre.polar.rot_y
			turn(-speed,sec)
	return nearestMarker(m)

def collect():
	'''
	Now token is in range pick it up
	'''
	global MARKER_TYPE
	MARKER_TYPE = rotateToNearest(5,0.01,04.05).info.marker_type
	print "Looking for", MARKER_TYPE
	drive(100,0.1)
	
def rotateToHome():
	while True:
		try:
			home_marker = getHomeMarkers()
			rotateToHomeMarker(25,0.01,10)
			break
		except ValueError:
			turn(25,0.1)

def go():
	print "here"
	tmp = True
	i = 0
	while tmp:
		try:
			while nearestMarker(getMarkers()).dist > 0.5:
				print "Found"
				rotateToNearest(25,0.01,0.5)
				print "F to",nearestMarker(getMarkers()).info.code, " - Distance", nearestMarker(getMarkers()).dist
				drive(100,0.5)
				tmp = False
				print "Found marker"
			collect()
			print movement
			print "Going Home"
			rotateToHome()
			#while bumper not pressed
			drive(100,2)
			print ">>>>>>>>>>I am home"
			drive(-100,0.2)
		except:
			print "Cant find anything" , i
			i+=1
			if i > 10:
				print "I'm bored I'm going for it"
				drive(100,2)
				break
			turn(25,random())
			continue
	
	
	
while True:
	go()

print "END"	
exit()
