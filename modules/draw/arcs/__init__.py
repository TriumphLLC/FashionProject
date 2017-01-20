'''
Утилиты для работы с дугами.
'''

import bpy
import math

from fashion_project.modules.draw.arcs.arc import Arc


def is_one_of_arc(obj):
    return obj.fp_type.startswith('fp.draw.arcs.')


def get_arc_origin_point_cords(obj):
	return obj.parent.location


def get_arc_ends_coords(obj):
	root_point = get_arc_origin_point_cords(obj)
	x = root_point[0]
	y = root_point[1]
	r = obj.fp_expression
	angle1 = obj.fp_angles[0]
	angle2 = obj.fp_angles[1]
	x1 = math.cos(math.radians(angle1)) * float(r) + float(x)
	y1 = math.sin(math.radians(angle1)) * float(r) + float(y)
	x2 = math.cos(math.radians(angle2)) * float(r) + float(x)
	y2 = math.sin(math.radians(angle2)) * float(r) + float(y)
	return [(round(x1,6),round(y1, 6),0.0),(round(x2,6),round(y2,6),0.0)]
	
	 	