##INPUT 0 IR


from sr.robot import *
from random import random

import time

SEARCHING, DRIVING = range(2)
movement = []
MARKER_TYPE = 0
ZONES = {0: [0,27], 1:[6,7], 2: [13,14], 3: [20,21]}
my_tokens = []

R = Robot()

token_filter = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER)
token_filter_g = lambda m: m.info.marker_type == "token_gold"
token_filter_s = lambda m: m.info.marker_type == "token_silver"
arena_filter = lambda m: m.info.marker_type in (MARKER_ARENA)
home_filter = lambda m: m.info.code in ZONES[R.zone]
my_token_filters = None

def refreshFilter(code):
	global my_token_filters
	global my_tokens
	my_tokens.append(code)
	my_token_filters = lambda m: m.info.code not in my_tokens

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

def getMarkers(all=False):
	if MARKER_TYPE == 0 or all:
		return filter(token_filter, R.see())
	if MARKER_TYPE == "token_silver":
		return filter(my_token_filters,filter(token_filter_s, R.see()))
	elif MARKER_TYPE == "token_gold":
		return filter(my_token_filters,filter(token_filter_g, R.see()))
		
def getInvMarkers():
	if MARKER_TYPE == "token_silver":
		return filter(token_filter_g, R.see())
	elif MARKER_TYPE == "token_gold":
		return filter(token_filter_s, R.see())

def correct(mtype):
		return mtype == MARKER_TYPE
		
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
	print "Rotate to Nearest"
	m = getMarkers()
	if nearestMarker(m).centre.polar.rot_y > err:
		while (nearestMarker(m).centre.polar.rot_y > err):
			m = getMarkers()
			print nearestMarker(m).centre.polar.rot_y, "turning towards", nearestMarker(m).info.code
			turn(speed,sec)
	elif nearestMarker(m).centre.polar.rot_y < -err:
		while (nearestMarker(m).centre.polar.rot_y < -err):
			m = getMarkers()
			print nearestMarker(m).centre.polar.rot_y, "turning towards", nearestMarker(m).info.code
			turn(-speed,sec)
	return nearestMarker(m)
	
def rotateToHomeMarker(speed,sec,err):
	print "Rotate to home marker"
	m = getHomeMarkers()
	print nearestMarker(m)
	if nearestMarker(m).centre.polar.rot_y > err:
		while (nearestMarker(m).centre.polar.rot_y > err):
			m = getHomeMarkers()
			print nearestMarker(m).centre.polar.rot_y, "turning towards", nearestMarker(m).info.code, " - HOME"
			turn(speed,sec)
	elif nearestMarker(m).centre.polar.rot_y < -err:
		while (nearestMarker(m).centre.polar.rot_y < -err):
			m = getHomeMarkers()
			print nearestMarker(m).centre.polar.rot_y, "turning towards", nearestMarker(m).info.code, " - HOME"
			turn(-speed,sec)
	return nearestMarker(m)

def collect():
	'''
	Now token is in range pick it up
	'''
	global MARKER_TYPE
	tmp = rotateToNearest(5,0.01,0.05)
	MARKER_TYPE = tmp.info.marker_type
	print "Looking for", MARKER_TYPE
	drive(100,0.1)
	refreshFilter(tmp.info.code)
	return tmp
	
def rotateToHome():
	while True:
		try:
			home_marker = getHomeMarkers()
			rotateToHomeMarker(25,0.01,0.1)
			break
		except ValueError:
			turn(25,0.1)

def go():
	print "New loop"
	tmp = True
	i = 0
	while tmp:
		try:
			while nearestMarker(getMarkers()).dist > 0.5:
				print "Found"
				rotateToNearest(25,0.01,0.5)
				print "F to",nearestMarker(getMarkers()).info.code, " - Distance", nearestMarker(getMarkers()).dist
				near = nearestMarker(getMarkers(True))
				if not correct(near.info.marker_type) and near.dist < 0.5:
					#STOP!!!!
					print "Wrong type - run away"
					turn(50,0.2)
					break
				else:
					print "It's ok", near.info.marker_type, near.dist
				drive(100,0.5)
				tmp = False
				print "Found marker"
			collect()
			print "Going Home"
			rotateToHome()
			#while bumper not pressed
			home = nearestMarker(getHomeMarkers())
			print "I am", home.dist, "away from home heading for", home.info.code
			while home.dist > 0.2: # WHILE BUMPER NOT PRESS HERE
				try:
					tmp = nearestMarker(getInvMarkers())
					if (not correct(tmp.info.marker_type)) and tmp.dist < 0.4:
						#STOP!!!!
						print "Wrong type - run away", 
						turn(50,0.2)
						continue
					else:
						print "It's ok", tmp.info.marker_type, tmp.dist
						break
				except:
					#Nothing in front
					print "F to home, I am", home.dist, "away from", home.info.code
					drive(100,0.01)
					home = nearestMarker(getHomeMarkers())
					#continue
					if home.dist<0.4:
						tmp = False
						break
		except:
			print "Cant find anything" , i
			i+=1
			if i > 5:
				print "I'm bored I'm going for it"
				drive(100,2)
				break
			turn(25,random())
			continue
		

	
while True:
	go()
	print ">>>>>>>>>>I am home"
	drive(-100,0.5)

print "END"	
exit()
