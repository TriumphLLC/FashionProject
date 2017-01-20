'''
Утилиты для работы со всеми типами точек.
'''

import bpy

from math import atan

def is_one_of_points(obj):
  return obj.fp_type.startswith('fp.draw.points.')

def get_all_points():
  return tuple(
    obj for obj in bpy.data.objects
    if is_one_of_points(obj)
  )

def get_root_point(obj):
  if obj.parent:
    return get_root_point(obj.parent)
  else:
    return obj

def get_angle(coords_point1, coords_point2):
	if abs(round(coords_point1[0], 3) - round(coords_point2[0], 3)) < 0.001:
		if coords_point1[1] < coords_point2[1]:
			return 90
		else:
			return -90
	elif abs(round(coords_point1[1], 3) - round(coords_point2[1], 3)) < 0.001:
		if coords_point1[0] < coords_point2[0]:
			return 0
		else: 
			return 180
	else:
		k = (round(coords_point1[1], 3) - round(coords_point2[1], 3))/(round(coords_point1[0], 3) - round(coords_point2[0], 3))
		if coords_point1[1] < coords_point2[1] and coords_point1[0] < coords_point2[0]:
			new_angle = atan(k)*57.2958 
		elif coords_point1[1] < coords_point2[1] and coords_point1[0] > coords_point2[0]:
			new_angle = atan(k)*57.2958 + 180
		elif coords_point1[1] > coords_point2[1] and coords_point1[0] < coords_point2[0]:
			new_angle = atan(k)*57.2958 
		elif coords_point1[1] > coords_point2[1] and coords_point1[0] > coords_point2[0]:
			new_angle = atan(k)*57.2958 + 180
		return new_angle

def get_absolute_angle(coords_point1, coords_point2):
	if abs(round(coords_point1[0], 3) - round(coords_point2[0], 3)) < 0.001:
		if coords_point1[1] < coords_point2[1]:
			return 90
		else:
			return -90
	elif abs(round(coords_point1[1], 3) - round(coords_point2[1], 3)) < 0.001:
		if coords_point1[0] < coords_point2[0]:
			return 0
		else: 
			return 180
	else:
		k = (round(coords_point1[1], 3) - round(coords_point2[1], 3))/(round(coords_point1[0], 3) - round(coords_point2[0], 3))
		if coords_point1[0] < coords_point2[0] and coords_point1[1] < coords_point2[1]:
			new_angle = atan(k)*57.2958 
		elif coords_point1[0] > coords_point2[0] and coords_point1[1] < coords_point2[1]:
			new_angle = atan(k)*57.2958 + 180
		elif coords_point1[0] > coords_point2[0] and coords_point1[1] > coords_point2[1]:
			new_angle = atan(k)*57.2958 + 180
		elif coords_point1[0] < coords_point2[0] and coords_point1[1] > coords_point2[1]:
			new_angle = atan(k)*57.2958 + 360
		return new_angle