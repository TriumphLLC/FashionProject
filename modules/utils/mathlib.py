# Fashion Project
# Author: Shkubelev Nikolay
# Description: Mathematical functions

import math

# fp
def setSizeLine(point, size, angle):
	coords = { "x": 0, "y": 0 }
	coords["x"] = float(point["x"]) + float(size) * math.cos(angle)
	coords["y"] = float(point["y"]) + float(size) * math.sin(angle)
	return coords

def deg2rad(angle):
  return angle * math.pi/180

def rad2deg(angle):
    return angle * 180/math.pi

def getAngleBetween3Points(A, B, C):
  AB = math.sqrt(math.pow(B["x"]-A["x"], 2) + math.pow(B["y"]-A["y"], 2))
  BC = math.sqrt(math.pow(B["x"]-C["x"], 2) + math.pow(B["y"]-C["y"], 2))
  AC = math.sqrt(math.pow(C["x"]-A["x"], 2) + math.pow(C["y"]-A["y"], 2))
  return math.acos((BC*BC+AB*AB-AC*AC)/(2*BC*AB))


def get_distance(location1, location2):
  distance = math.sqrt(math.pow(round(location1[0], 7) - round(location2[0], 7), 2) + math.pow(round(location1[1], 7) - round(location2[1], 7), 2))
  return distance
