# Description: Intersections
import bpy

from math import pi, ceil, sqrt, tan, acos, asin, sin, cos, degrees

from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.utils.point2D import *
from fashion_project.modules.utils.polynomial import *
from fashion_project.modules.utils.fp_expression import expression_to_value

from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.arcs.arc import Arc
from fashion_project.modules.draw.curves.bezier_curve import BezierCurve


def elements_intersection(element1, element2):
	if element1.fp_type == Line.FP_TYPE and element2.fp_type == Line.FP_TYPE:
		collection_of_line1_points = ([d for d in bpy.data.objects if (d.fp_id == element1.fp_deps[0] or d.fp_id == element1.fp_deps[1]) and d.fp_id > 0])
		collection_of_line2_points = ([d for d in bpy.data.objects if (d.fp_id == element2.fp_deps[0] or d.fp_id == element2.fp_deps[1]) and d.fp_id > 0])
		locations1 = [get_point_abs_location(point) for point in collection_of_line1_points]
		locations2 = [get_point_abs_location(point) for point in collection_of_line2_points]
		return line_to_line({ "x": locations1[0][0], "y": locations1[0][1] },{ "x": locations1[1][0], "y": locations1[1][1] },{ "x": locations2[0][0], "y": locations2[0][1] },{ "x": locations2[1][0], "y": locations2[1][1] })
	elif (element1.fp_type == Line.FP_TYPE and element2.fp_type == Arc.FP_TYPE) or (element1.fp_type == Arc.FP_TYPE and element2.fp_type == Line.FP_TYPE):
		if element1.fp_type == Line.FP_TYPE:
			collection_of_line_points = ([d for d in bpy.data.objects if (d.fp_id == element1.fp_deps[0] or d.fp_id == element1.fp_deps[1]) and d.fp_id > 0])
			angles = element2.fp_angles
			point_center_arc = get_point_abs_location(element2.parent)
			radius_arc = expression_to_value(element2.fp_expression)
			locations = [get_point_abs_location(point) for point in collection_of_line_points]
		else:
			collection_of_line_points = ([d for d in bpy.data.objects if (d.fp_id == element2.fp_deps[0] or d.fp_id == element2.fp_deps[1]) and d.fp_id > 0])
			angles = element1.fp_angles
			point_center_arc = get_point_abs_location(element1.parent)
			radius_arc = expression_to_value(element1.fp_expression)
			locations = [get_point_abs_location(point) for point in collection_of_line_points]
		return line_to_arc({"x": locations[0][0], "y": locations[0][1]},{ "x": locations[1][0], "y": locations[1][1] },point_center_arc, angles[0], angles[1], radius_arc)
	elif (element1.fp_type == Arc.FP_TYPE and element2.fp_type == Arc.FP_TYPE):
		angles_arc1 = element1.fp_angles
		point_center_arc1 = get_point_abs_location(element1.parent)
		radius_arc1 = expression_to_value(element1.fp_expression)
		angles_arc2 = element2.fp_angles
		point_center_arc2 = get_point_abs_location(element2.parent)
		radius_arc2 = expression_to_value(element2.fp_expression)
		return arc_to_arc(point_center_arc1, angles_arc1[0], angles_arc1[1], radius_arc1, point_center_arc2, angles_arc2[0], angles_arc2[1], radius_arc2)
	elif (element1.fp_type == Line.FP_TYPE and element2.fp_type == BezierCurve.FP_TYPE) or (element1.fp_type == BezierCurve.FP_TYPE and element2.fp_type == Line.FP_TYPE):
		if element1.fp_type == Line.FP_TYPE:
			collection_of_line_points = ([d for d in bpy.data.objects if (d.fp_id == element1.fp_deps[0] or d.fp_id == element1.fp_deps[1]) and d.fp_id > 0])
			locations = [get_point_abs_location(point) for point in collection_of_line_points]
			locations_curve = [
				get_point_abs_location(item) for item in bpy.data.objects
				if item.fp_id > 0 and item.fp_id in element2.fp_deps
			]
			handle_left = [element2.data.splines[0].bezier_points[0].handle_right[0] - element2.data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],element2.data.splines[0].bezier_points[0].handle_right[1] - element2.data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
			handle_right = [element2.data.splines[0].bezier_points[1].handle_left[0] - element2.data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],element2.data.splines[0].bezier_points[1].handle_left[1] - element2.data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
		else:
			collection_of_line_points = ([d for d in bpy.data.objects if (d.fp_id == element2.fp_deps[0] or d.fp_id == element2.fp_deps[1]) and d.fp_id > 0])
			locations = [get_point_abs_location(point) for point in collection_of_line_points]
			locations_curve = [
				get_point_abs_location(item) for item in bpy.data.objects
				if item.fp_id > 0 and item.fp_id in element1.fp_deps
			]
			handle_left = [element1.data.splines[0].bezier_points[0].handle_right[0] - element1.data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],element1.data.splines[0].bezier_points[0].handle_right[1] - element1.data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
			handle_right = [element1.data.splines[0].bezier_points[1].handle_left[0] - element1.data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],element1.data.splines[0].bezier_points[1].handle_left[1] - element1.data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
		return line_to_curve({"x": locations[0][0], "y": locations[0][1]},{ "x": locations[1][0], "y": locations[1][1]}, {"x": locations_curve[0][0], "y": locations_curve[0][1]}, {"x": handle_left[0], "y": handle_left[1]}, {"x": handle_right[0], "y": handle_right[1]}, {"x": locations_curve[1][0], "y": locations_curve[1][1]})
	elif (element1.fp_type == Arc.FP_TYPE and element2.fp_type == BezierCurve.FP_TYPE) or (element1.fp_type == BezierCurve.FP_TYPE and element2.fp_type == Arc.FP_TYPE):
		if element1.fp_type == Arc.FP_TYPE:
			angles_arc = element1.fp_angles
			point_center_arc = get_point_abs_location(element1.parent)
			radius_arc = expression_to_value(element1.fp_expression)
			locations_curve = [
				get_point_abs_location(item) for item in bpy.data.objects
				if item.fp_id > 0 and item.fp_id in element2.fp_deps
			]
			handle_left = [element2.data.splines[0].bezier_points[0].handle_right[0] - element2.data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],element2.data.splines[0].bezier_points[0].handle_right[1] - element2.data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
			handle_right = [element2.data.splines[0].bezier_points[1].handle_left[0] - element2.data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],element2.data.splines[0].bezier_points[1].handle_left[1] - element2.data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
		else:
			angles_arc = element2.fp_angles
			point_center_arc = get_point_abs_location(element2.parent)
			radius_arc = expression_to_value(element2.fp_expression)
			locations_curve = [
				get_point_abs_location(item) for item in bpy.data.objects
				if item.fp_id > 0 and item.fp_id in element1.fp_deps
			]
			handle_left = [element1.data.splines[0].bezier_points[0].handle_right[0] - element1.data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],element1.data.splines[0].bezier_points[0].handle_right[1] - element1.data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
			handle_right = [element1.data.splines[0].bezier_points[1].handle_left[0] - element1.data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],element1.data.splines[0].bezier_points[1].handle_left[1] - element1.data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
		return curve_to_arc({"x": locations_curve[0][0], "y": locations_curve[0][1]}, {"x": handle_left[0], "y": handle_left[1]}, {"x": handle_right[0], "y": handle_right[1]}, {"x": locations_curve[1][0], "y": locations_curve[1][1]}, angles_arc[0], angles_arc[1], point_center_arc, radius_arc)
	elif (element1.fp_type == BezierCurve.FP_TYPE and element2.fp_type == BezierCurve.FP_TYPE):
		locations_curve1 = [
			get_point_abs_location(item) for item in bpy.data.objects
			if item.fp_id > 0 and item.fp_id in element2.fp_deps
		]
		handle_curve1_left = [element2.data.splines[0].bezier_points[0].handle_right[0] - element2.data.splines[0].bezier_points[0].co[0] + locations_curve1[0][0],element2.data.splines[0].bezier_points[0].handle_right[1] - element2.data.splines[0].bezier_points[0].co[1] + locations_curve1[0][1],0.0]
		handle_curve1_right = [element2.data.splines[0].bezier_points[1].handle_left[0] - element2.data.splines[0].bezier_points[1].co[0] + locations_curve1[1][0],element2.data.splines[0].bezier_points[1].handle_left[1] - element2.data.splines[0].bezier_points[1].co[1] + locations_curve1[1][1],0.0]
		locations_curve2 = [
			get_point_abs_location(item) for item in bpy.data.objects
			if item.fp_id > 0 and item.fp_id in element1.fp_deps
		]
		handle_curve2_left = [element1.data.splines[0].bezier_points[0].handle_right[0] - element1.data.splines[0].bezier_points[0].co[0] + locations_curve2[0][0],element1.data.splines[0].bezier_points[0].handle_right[1] - element1.data.splines[0].bezier_points[0].co[1] + locations_curve2[0][1],0.0]
		handle_curve2_right = [element1.data.splines[0].bezier_points[1].handle_left[0] - element1.data.splines[0].bezier_points[1].co[0] + locations_curve2[1][0],element1.data.splines[0].bezier_points[1].handle_left[1] - element1.data.splines[0].bezier_points[1].co[1] + locations_curve2[1][1],0.0]
		return curve_to_curve({"x": locations_curve1[0][0], "y": locations_curve1[0][1]}, {"x": handle_curve1_left[0], "y": handle_curve1_left[1]}, {"x": handle_curve1_right[0], "y": handle_curve1_right[1]}, {"x": locations_curve1[1][0], "y": locations_curve1[1][1]}, {"x": locations_curve2[0][0], "y": locations_curve2[0][1]}, {"x": handle_curve2_left[0], "y": handle_curve2_left[1]}, {"x": handle_curve2_right[0], "y": handle_curve2_right[1]}, {"x": locations_curve2[1][0], "y": locations_curve2[1][1]})


def line_to_line(a1,a2,b1,b2):
  '''
    Пересечение линий
  '''
  result = { "info": "", "points": [] }
  if (a1["x"] == a2["x"] and b1["x"] == b2["x"]) or (a1["y"] == a2["y"] and b1["y"] == b2["y"]):
    result["info"] = "Parallel"
    result["points"].append({"x": -10000, "y": -10000})
    return result
  elif a1["x"] == a2["x"]:
    ub_k = (b2["y"] - b1["y"]) / (b2["x"] - b1["x"])
    ub_b = -ub_k * b1["x"] + b1["y"]
    x = a1["x"]
    y = ub_k * x + ub_b
    result["info"] = "Intersection"
    result["points"].append({"x": x, "y": y})
    return result
  elif b1["x"] == b2["x"]:
    ua_k = (a2["y"] - a1["y"]) / (a2["x"] - a1["x"])
    ua_b = -ua_k * a1["x"] + a1["y"]
    x = b1["x"]
    y = ua_k * x + ua_b
    result["info"] = "Intersection"
    result["points"].append({"x": x, "y": y})
    return result
  else:
    ua_k = (a2["y"] - a1["y"])/(a2["x"] - a1["x"])
    ub_k = (b2["y"] - b1["y"])/(b2["x"] - b1["x"])
    ua_b = -ua_k * a1["x"] + a1["y"]
    ub_b = -ub_k * b1["x"] + b1["y"]
    x = (ub_b - ua_b)/(ua_k - ub_k)
    y = ua_k * x + ua_b
    result["info"] = "Intersection"
    result["points"].append({"x": x, "y": y})
    return result


def line_to_axis(line1, axis):
  '''
    Пересечение линии и оси
  '''
  pass


def line_to_curve(a1, a2, p1, p2, p3, p4):
	'''
	Пересечение линии и кривой
	'''
	result = { "info": "No intersection", "points": [] }

	min_point_a = min_point(a1, a2)
	max_point_a = max_point(a1, a2)

	a = multiply(p1, -1)
	b = multiply(p2, 3)
	c = multiply(p3, -3)
	d = add(p4, c)
	d = add(b, d)
	d = add(a, d)
	c3 = d

	a = multiply(p1, 3)
	b = multiply(p2, -6)
	c = multiply(p3, 3)
	d = add(b, c)
	d = add(a, d)
	c2 = d

	a = multiply(p1, -3)
	b = multiply(p2, 3)
	c = add(a, b)
	c1 = c

	c0 = p1

	n = {"x": a1["y"] - a2["y"], "y": a2["x"] - a1["x"]}
	cl = a1["x"]*a2["y"] - a2["x"]*a1["y"]
	coefs = [dot(n, c3), dot(n, c2), dot(n, c1), dot(n, c0) + cl]
	roots = get_roots(coefs)
	i = 0
	while i < 3:
		if i < len(roots):
			t = roots[i]
			i += 1 
			if t <= 1 and t >= 0:
				p5 = lerp(p1, p2, t)
				p6 = lerp(p2, p3, t)
				p7 = lerp(p3, p4, t)
				p8 = lerp(p5, p6, t)
				p9 = lerp(p6, p7, t)
				p10 = lerp(p8, p9, t)
				if p10["x"] >= min_point_a["x"] and p10["x"] <= max_point_a["x"] and p10["y"] >= min_point_a["y"] and p10["y"] <= max_point_a["y"]:
					result["points"].append({"x": p10["x"], "y": p10["y"]})
				else:
					result["points"].append({"x": -10000, "y": -10000})
			else:
				result["points"].append({"x": -10000, "y": -10000})
		else:
			result["points"].append({"x": -10000, "y": -10000})
			i += 1
	return result


def line_to_arc(a1, a2, point_center_arc, ang1, ang2, radius_arc):
  '''
    Пересечение линии и дигу
  '''
  result = { "info": "", "points": [] }
  min_point_a = min(a1["x"], a2["x"])
  max_point_a = max(a1["x"], a2["x"]) 
  x = point_center_arc[0] + radius_arc * cos(0*pi/180)
  y = point_center_arc[1] + radius_arc * sin(0*pi/180)
  if abs(a1["x"] - a2["x"]) < 0.0001:
  	a_polynomial = 1
  	b_polynomial = -2 * point_center_arc[1]
  	c_polynomial = point_center_arc[1] * point_center_arc[1] + a1["x"] * a1["x"] - 2 * a1["x"] * point_center_arc[0] + point_center_arc[0] * point_center_arc[0] - radius_arc * radius_arc
  	deter = b_polynomial * b_polynomial - 4 * a_polynomial * c_polynomial
  	if deter < 0:
  		result["info"] = "No intersection"
  		result["points"].append({"x": -10000, "y": -10000})
  		result["points"].append({"x": -10000, "y": -10000})
  	else:
  		result["info"] = "Intersection"
	  	x1 = a1["x"]
	  	y1 = (-b_polynomial + sqrt(deter))/(2 * a_polynomial)
	  	x2 = a1["x"]
	  	y2 = (-b_polynomial - sqrt(deter))/(2 * a_polynomial)
	  	ac_side1 = sqrt((point_center_arc[0] - x1)*(point_center_arc[0] - x1) + (point_center_arc[1] - y1)*(point_center_arc[1] - y1)) 
	  	ab_side1 = sqrt((point_center_arc[0] - x)*(point_center_arc[0] - x) + (point_center_arc[1] - y)*(point_center_arc[1] - y)) 
	  	bc_side1 = sqrt((x1 - x)*(x1 - x) + (y1 - y)*(y1 - y)) 
	  	ac_side2 = sqrt((point_center_arc[0] - x2)*(point_center_arc[0] - x2) + (point_center_arc[1] - y2)*(point_center_arc[1] - y2)) 
	  	ab_side2 = sqrt((point_center_arc[0] - x)*(point_center_arc[0] - x) + (point_center_arc[1] - y)*(point_center_arc[1] - y)) 
	  	bc_side2 = sqrt((x2 - x)*(x2 - x) + (y2 - y)*(y2 - y)) 
	  	alfa1 = (ac_side1 * ac_side1 + ab_side1 * ab_side1 - bc_side1 * bc_side1)/(2 * ac_side1 * ab_side1)
	  	alfa2 = (ac_side2 * ac_side2 + ab_side2 * ab_side2 - bc_side2 * bc_side2)/(2 * ac_side2 * ab_side2)
	  	angle_point = [0, 0]
	  	if y1 < point_center_arc[1]:
	  	  	angle_point[0] = 360 - degrees(acos(alfa1))
	  	else:
	  		angle_point[0] = degrees(acos(alfa1))
	  	if y2 < point_center_arc[1]:
	  	  	angle_point[1] = 360 - degrees(acos(alfa2))
	  	else:
	  		angle_point[1] = degrees(acos(alfa2))
	  	if angle_point[0] >= ang1 and angle_point[0] <= ang2 and x1 >= min_point_a and x1 <= max_point_a:
	  		result["points"].append({"x": x1, "y": y1})
	  	else:
	  		result["points"].append({"x": -10000, "y": -10000})
	  	if angle_point[1] >= ang1 and angle_point[1] <= ang2 and x2 >= min_point_a and x2 <= max_point_a:
	  		result["points"].append({"x": x2, "y": y2})
	  	else:
	  		result["points"].append({"x": -10000, "y": -10000})
  else: 
  	k = (a2["y"] - a1["y"])/(a2["x"] - a1["x"])
  	b = -k * a1["x"] + a1["y"]
  	a_polynomial = k * k + 1
  	b_polynomial = 2 * k * b - 2 * point_center_arc[1] * k - 2 * point_center_arc[0] 
  	c_polynomial = b * b - 2 * point_center_arc[1] * b + point_center_arc[1] * point_center_arc[1] + point_center_arc[0] * point_center_arc[0] - radius_arc * radius_arc
  	deter = b_polynomial * b_polynomial - 4 * a_polynomial * c_polynomial
  	if deter < 0:
  		result["info"] = "No intersection"
  		result["points"].append({"x": -10000, "y": -10000})
  		result["points"].append({"x": -10000, "y": -10000})
  	else:
  		result["info"] = "Intersection"
	  	x1 = (-b_polynomial + sqrt(deter))/(2 * a_polynomial)
	  	y1 = k * x1 + b
	  	x2 = (-b_polynomial - sqrt(deter))/(2 * a_polynomial)
	  	y2 = k * x2 + b
	  	ac_side1 = sqrt((point_center_arc[0] - x1)*(point_center_arc[0] - x1) + (point_center_arc[1] - y1)*(point_center_arc[1] - y1)) 
	  	ab_side1 = sqrt((point_center_arc[0] - x)*(point_center_arc[0] - x) + (point_center_arc[1] - y)*(point_center_arc[1] - y)) 
	  	bc_side1 = sqrt((x1 - x)*(x1 - x) + (y1 - y)*(y1 - y)) 
	  	ac_side2 = sqrt((point_center_arc[0] - x2)*(point_center_arc[0] - x2) + (point_center_arc[1] - y2)*(point_center_arc[1] - y2)) 
	  	ab_side2 = sqrt((point_center_arc[0] - x)*(point_center_arc[0] - x) + (point_center_arc[1] - y)*(point_center_arc[1] - y)) 
	  	bc_side2 = sqrt((x2 - x)*(x2 - x) + (y2 - y)*(y2 - y)) 
	  	alfa1 = (ac_side1 * ac_side1 + ab_side1 * ab_side1 - bc_side1 * bc_side1)/(2 * ac_side1 * ab_side1)
	  	alfa2 = (ac_side2 * ac_side2 + ab_side2 * ab_side2 - bc_side2 * bc_side2)/(2 * ac_side2 * ab_side2)
	  	angle_point = [0, 0]
	  	if y1 < point_center_arc[1]:
	  	  	angle_point[0] = 360 - degrees(acos(alfa1))
	  	else:
	  		angle_point[0] = degrees(acos(alfa1))
	  	if y2 < point_center_arc[1]:
	  	  	angle_point[1] = 360 - degrees(acos(alfa2))
	  	else:
	  		angle_point[1] = degrees(acos(alfa2))
	  	if angle_point[0] >= ang1 and angle_point[0] <= ang2 and x1 >= min_point_a and x1 <= max_point_a:
	  		result["points"].append({"x": x1, "y": y1})
	  	else:
	  		result["points"].append({"x": -10000, "y": -10000})
	  	if angle_point[1] >= ang1 and angle_point[1] <= ang2 and x2 >= min_point_a and x2 <= max_point_a:
	  		result["points"].append({"x": x2, "y": y2})
	  	else:
	  		result["points"].append({"x": -10000, "y": -10000})
  return result



def curve_to_curve(a1, a2, a3 , a4, b1, b2, b3, b4):
	result = { "info": "No intersection", "points": [] }
	
	a = multiply(a1, -1)
	b = multiply(a2, 3)
	c = multiply(a3, -3)
	d = add(a4, c)
	d = add(b, d)
	d = add(a, d)
	c13 = d

	a = multiply(a1, 3)
	b = multiply(a2, -6)
	c = multiply(a3, 3)
	d = add(b, c)
	d = add(a, d)
	c12 = d

	a = multiply(a1, -3)
	b = multiply(a2, 3)
	c = add(a, b)
	c11 = c

	c10 = a1

	a = multiply(b1, -1)
	b = multiply(b2, 3)
	c = multiply(b3, -3)
	d = add(b4, c)
	d = add(b, d)
	d = add(a, d)
	c23 = d

	a = multiply(b1, 3)
	b = multiply(b2, -6)
	c = multiply(b3, 3)
	d = add(b, c)
	d = add(a, d)
	c22 = d

	a = multiply(b1, -3)
	b = multiply(b2, 3)
	c = add(a, b)
	c21 = c

	c20 = b1

	c10x2 = c10["x"]*c10["x"]
	c10x3 = c10["x"]*c10["x"]*c10["x"]
	c10y2 = c10["y"]*c10["y"]
	c10y3 = c10["y"]*c10["y"]*c10["y"]
	c11x2 = c11["x"]*c11["x"]
	c11x3 = c11["x"]*c11["x"]*c11["x"]
	c11y2 = c11["y"]*c11["y"]
	c11y3 = c11["y"]*c11["y"]*c11["y"]
	c12x2 = c12["x"]*c12["x"]
	c12x3 = c12["x"]*c12["x"]*c12["x"]
	c12y2 = c12["y"]*c12["y"]
	c12y3 = c12["y"]*c12["y"]*c12["y"]
	c13x2 = c13["x"]*c13["x"]
	c13x3 = c13["x"]*c13["x"]*c13["x"]
	c13y2 = c13["y"]*c13["y"]
	c13y3 = c13["y"]*c13["y"]*c13["y"]
	c20x2 = c20["x"]*c20["x"]
	c20x3 = c20["x"]*c20["x"]*c20["x"]
	c20y2 = c20["y"]*c20["y"]
	c20y3 = c20["y"]*c20["y"]*c20["y"]
	c21x2 = c21["x"]*c21["x"]
	c21x3 = c21["x"]*c21["x"]*c21["x"]
	c21y2 = c21["y"]*c21["y"]
	c22x2 = c22["x"]*c22["x"]
	c22x3 = c22["x"]*c22["x"]*c22["x"]
	c22y2 = c22["y"]*c22["y"]
	c23x2 = c23["x"]*c23["x"]
	c23x3 = c23["x"]*c23["x"]*c23["x"]
	c23y2 = c23["y"]*c23["y"]
	c23y3 = c23["y"]*c23["y"]*c23["y"]

	coefs = [
		-c13x3*c23y3 + c13y3*c23x3 - 3*c13["x"]*c13y2*c23x2*c23["y"] +
            3*c13x2*c13["y"]*c23["x"]*c23y2,

        -6*c13["x"]*c22["x"]*c13y2*c23["x"]*c23["y"] + 6*c13x2*c13["y"]*c22["y"]*c23["x"]*c23["y"] + 3*c22["x"]*c13y3*c23x2 -
            3*c13x3*c22["y"]*c23y2 - 3*c13["x"]*c13y2*c22["y"]*c23x2 + 3*c13x2*c22["x"]*c13["y"]*c23y2,

        -6*c21["x"]*c13["x"]*c13y2*c23["x"]*c23["y"] - 6*c13["x"]*c22["x"]*c13y2*c22["y"]*c23["x"] + 6*c13x2*c22["x"]*c13["y"]*c22["y"]*c23["y"] +
            3*c21["x"]*c13y3*c23x2 + 3*c22x2*c13y3*c23["x"] + 3*c21["x"]*c13x2*c13["y"]*c23y2 - 3*c13["x"]*c21["y"]*c13y2*c23x2 -
            3*c13["x"]*c22x2*c13y2*c23["y"] + c13x2*c13["y"]*c23["x"]*(6*c21["y"]*c23["y"] + 3*c22y2) + c13x3*(-c21["y"]*c23y2 -
            2*c22y2*c23["y"] - c23["y"]*(2*c21["y"]*c23["y"] + c22y2)),

        c11["x"]*c12["y"]*c13["x"]*c13["y"]*c23["x"]*c23["y"] - c11["y"]*c12["x"]*c13["x"]*c13["y"]*c23["x"]*c23["y"] + 6*c21["x"]*c22["x"]*c13y3*c23["x"] +
            3*c11["x"]*c12["x"]*c13["x"]*c13["y"]*c23y2 + 6*c10["x"]*c13["x"]*c13y2*c23["x"]*c23["y"] - 3*c11["x"]*c12["x"]*c13y2*c23["x"]*c23["y"] -
            3*c11["y"]*c12["y"]*c13["x"]*c13["y"]*c23x2 - 6*c10["y"]*c13x2*c13["y"]*c23["x"]*c23["y"] - 6*c20["x"]*c13["x"]*c13y2*c23["x"]*c23["y"] +
            3*c11["y"]*c12["y"]*c13x2*c23["x"]*c23["y"] - 2*c12["x"]*c12y2*c13["x"]*c23["x"]*c23["y"] - 6*c21["x"]*c13["x"]*c22["x"]*c13y2*c23["y"] -
            6*c21["x"]*c13["x"]*c13y2*c22["y"]*c23["x"] - 6*c13["x"]*c21["y"]*c22["x"]*c13y2*c23["x"] + 6*c21["x"]*c13x2*c13["y"]*c22["y"]*c23["y"] +
            2*c12x2*c12["y"]*c13["y"]*c23["x"]*c23["y"] + c22x3*c13y3 - 3*c10["x"]*c13y3*c23x2 + 3*c10["y"]*c13x3*c23y2 +
            3*c20["x"]*c13y3*c23x2 + c12y3*c13["x"]*c23x2 - c12x3*c13["y"]*c23y2 - 3*c10["x"]*c13x2*c13["y"]*c23y2 +
            3*c10["y"]*c13["x"]*c13y2*c23x2 - 2*c11["x"]*c12["y"]*c13x2*c23y2 + c11["x"]*c12["y"]*c13y2*c23x2 - c11["y"]*c12["x"]*c13x2*c23y2 +
            2*c11["y"]*c12["x"]*c13y2*c23x2 + 3*c20["x"]*c13x2*c13["y"]*c23y2 - c12["x"]*c12y2*c13["y"]*c23x2 -
            3*c20["y"]*c13["x"]*c13y2*c23x2 + c12x2*c12["y"]*c13["x"]*c23y2 - 3*c13["x"]*c22x2*c13y2*c22["y"] +
            c13x2*c13["y"]*c23["x"]*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) + c13x2*c22["x"]*c13["y"]*(6*c21["y"]*c23["y"] + 3*c22y2) +
            c13x3*(-2*c21["y"]*c22["y"]*c23["y"] - c20["y"]*c23y2 - c22["y"]*(2*c21["y"]*c23["y"] + c22y2) - c23["y"]*(2*c20["y"]*c23["y"] + 2*c21["y"]*c22["y"])),

        6*c11["x"]*c12["x"]*c13["x"]*c13["y"]*c22["y"]*c23["y"] + c11["x"]*c12["y"]*c13["x"]*c22["x"]*c13["y"]*c23["y"] + c11["x"]*c12["y"]*c13["x"]*c13["y"]*c22["y"]*c23["x"] -
            c11["y"]*c12["x"]*c13["x"]*c22["x"]*c13["y"]*c23["y"] - c11["y"]*c12["x"]*c13["x"]*c13["y"]*c22["y"]*c23["x"] - 6*c11["y"]*c12["y"]*c13["x"]*c22["x"]*c13["y"]*c23["x"] -
            6*c10["x"]*c22["x"]*c13y3*c23["x"] + 6*c20["x"]*c22["x"]*c13y3*c23["x"] + 6*c10["y"]*c13x3*c22["y"]*c23["y"] + 2*c12y3*c13["x"]*c22["x"]*c23["x"] -
            2*c12x3*c13["y"]*c22["y"]*c23["y"] + 6*c10["x"]*c13["x"]*c22["x"]*c13y2*c23["y"] + 6*c10["x"]*c13["x"]*c13y2*c22["y"]*c23["x"] +
            6*c10["y"]*c13["x"]*c22["x"]*c13y2*c23["x"] - 3*c11["x"]*c12["x"]*c22["x"]*c13y2*c23["y"] - 3*c11["x"]*c12["x"]*c13y2*c22["y"]*c23["x"] +
            2*c11["x"]*c12["y"]*c22["x"]*c13y2*c23["x"] + 4*c11["y"]*c12["x"]*c22["x"]*c13y2*c23["x"] - 6*c10["x"]*c13x2*c13["y"]*c22["y"]*c23["y"] -
            6*c10["y"]*c13x2*c22["x"]*c13["y"]*c23["y"] - 6*c10["y"]*c13x2*c13["y"]*c22["y"]*c23["x"] - 4*c11["x"]*c12["y"]*c13x2*c22["y"]*c23["y"] -
            6*c20["x"]*c13["x"]*c22["x"]*c13y2*c23["y"] - 6*c20["x"]*c13["x"]*c13y2*c22["y"]*c23["x"] - 2*c11["y"]*c12["x"]*c13x2*c22["y"]*c23["y"] +
            3*c11["y"]*c12["y"]*c13x2*c22["x"]*c23["y"] + 3*c11["y"]*c12["y"]*c13x2*c22["y"]*c23["x"] - 2*c12["x"]*c12y2*c13["x"]*c22["x"]*c23["y"] -
            2*c12["x"]*c12y2*c13["x"]*c22["y"]*c23["x"] - 2*c12["x"]*c12y2*c22["x"]*c13["y"]*c23["x"] - 6*c20["y"]*c13["x"]*c22["x"]*c13y2*c23["x"] -
            6*c21["x"]*c13["x"]*c21["y"]*c13y2*c23["x"] - 6*c21["x"]*c13["x"]*c22["x"]*c13y2*c22["y"] + 6*c20["x"]*c13x2*c13["y"]*c22["y"]*c23["y"] +
            2*c12x2*c12["y"]*c13["x"]*c22["y"]*c23["y"] + 2*c12x2*c12["y"]*c22["x"]*c13["y"]*c23["y"] + 2*c12x2*c12["y"]*c13["y"]*c22["y"]*c23["x"] +
            3*c21["x"]*c22x2*c13y3 + 3*c21x2*c13y3*c23["x"] - 3*c13["x"]*c21["y"]*c22x2*c13y2 - 3*c21x2*c13["x"]*c13y2*c23["y"] +
            c13x2*c22["x"]*c13["y"]*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) + c13x2*c13["y"]*c23["x"]*(6*c20["y"]*c22["y"] + 3*c21y2) +
            c21["x"]*c13x2*c13["y"]*(6*c21["y"]*c23["y"] + 3*c22y2) + c13x3*(-2*c20["y"]*c22["y"]*c23["y"] - c23["y"]*(2*c20["y"]*c22["y"] + c21y2) -
            c21["y"]*(2*c21["y"]*c23["y"] + c22y2) - c22["y"]*(2*c20["y"]*c23["y"] + 2*c21["y"]*c22["y"])),

        c11["x"]*c21["x"]*c12["y"]*c13["x"]*c13["y"]*c23["y"] + c11["x"]*c12["y"]*c13["x"]*c21["y"]*c13["y"]*c23["x"] + c11["x"]*c12["y"]*c13["x"]*c22["x"]*c13["y"]*c22["y"] -
            c11["y"]*c12["x"]*c21["x"]*c13["x"]*c13["y"]*c23["y"] - c11["y"]*c12["x"]*c13["x"]*c21["y"]*c13["y"]*c23["x"] - c11["y"]*c12["x"]*c13["x"]*c22["x"]*c13["y"]*c22["y"] -
            6*c11["y"]*c21["x"]*c12["y"]*c13["x"]*c13["y"]*c23["x"] - 6*c10["x"]*c21["x"]*c13y3*c23["x"] + 6*c20["x"]*c21["x"]*c13y3*c23["x"] +
            2*c21["x"]*c12y3*c13["x"]*c23["x"] + 6*c10["x"]*c21["x"]*c13["x"]*c13y2*c23["y"] + 6*c10["x"]*c13["x"]*c21["y"]*c13y2*c23["x"] +
            6*c10["x"]*c13["x"]*c22["x"]*c13y2*c22["y"] + 6*c10["y"]*c21["x"]*c13["x"]*c13y2*c23["x"] - 3*c11["x"]*c12["x"]*c21["x"]*c13y2*c23["y"] -
            3*c11["x"]*c12["x"]*c21["y"]*c13y2*c23["x"] - 3*c11["x"]*c12["x"]*c22["x"]*c13y2*c22["y"] + 2*c11["x"]*c21["x"]*c12["y"]*c13y2*c23["x"] +
            4*c11["y"]*c12["x"]*c21["x"]*c13y2*c23["x"] - 6*c10["y"]*c21["x"]*c13x2*c13["y"]*c23["y"] - 6*c10["y"]*c13x2*c21["y"]*c13["y"]*c23["x"] -
            6*c10["y"]*c13x2*c22["x"]*c13["y"]*c22["y"] - 6*c20["x"]*c21["x"]*c13["x"]*c13y2*c23["y"] - 6*c20["x"]*c13["x"]*c21["y"]*c13y2*c23["x"] -
            6*c20["x"]*c13["x"]*c22["x"]*c13y2*c22["y"] + 3*c11["y"]*c21["x"]*c12["y"]*c13x2*c23["y"] - 3*c11["y"]*c12["y"]*c13["x"]*c22x2*c13["y"] +
            3*c11["y"]*c12["y"]*c13x2*c21["y"]*c23["x"] + 3*c11["y"]*c12["y"]*c13x2*c22["x"]*c22["y"] - 2*c12["x"]*c21["x"]*c12y2*c13["x"]*c23["y"] -
            2*c12["x"]*c21["x"]*c12y2*c13["y"]*c23["x"] - 2*c12["x"]*c12y2*c13["x"]*c21["y"]*c23["x"] - 2*c12["x"]*c12y2*c13["x"]*c22["x"]*c22["y"] -
            6*c20["y"]*c21["x"]*c13["x"]*c13y2*c23["x"] - 6*c21["x"]*c13["x"]*c21["y"]*c22["x"]*c13y2 + 6*c20["y"]*c13x2*c21["y"]*c13["y"]*c23["x"] +
            2*c12x2*c21["x"]*c12["y"]*c13["y"]*c23["y"] + 2*c12x2*c12["y"]*c21["y"]*c13["y"]*c23["x"] + 2*c12x2*c12["y"]*c22["x"]*c13["y"]*c22["y"] -
            3*c10["x"]*c22x2*c13y3 + 3*c20["x"]*c22x2*c13y3 + 3*c21x2*c22["x"]*c13y3 + c12y3*c13["x"]*c22x2 +
            3*c10["y"]*c13["x"]*c22x2*c13y2 + c11["x"]*c12["y"]*c22x2*c13y2 + 2*c11["y"]*c12["x"]*c22x2*c13y2 -
            c12["x"]*c12y2*c22x2*c13["y"] - 3*c20["y"]*c13["x"]*c22x2*c13y2 - 3*c21x2*c13["x"]*c13y2*c22["y"] +
            c12x2*c12["y"]*c13["x"]*(2*c21["y"]*c23["y"] + c22y2) + c11["x"]*c12["x"]*c13["x"]*c13["y"]*(6*c21["y"]*c23["y"] + 3*c22y2) +
            c21["x"]*c13x2*c13["y"]*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) + c12x3*c13["y"]*(-2*c21["y"]*c23["y"] - c22y2) +
            c10["y"]*c13x3*(6*c21["y"]*c23["y"] + 3*c22y2) + c11["y"]*c12["x"]*c13x2*(-2*c21["y"]*c23["y"] - c22y2) +
            c11["x"]*c12["y"]*c13x2*(-4*c21["y"]*c23["y"] - 2*c22y2) + c10["x"]*c13x2*c13["y"]*(-6*c21["y"]*c23["y"] - 3*c22y2) +
            c13x2*c22["x"]*c13["y"]*(6*c20["y"]*c22["y"] + 3*c21y2) + c20["x"]*c13x2*c13["y"]*(6*c21["y"]*c23["y"] + 3*c22y2) +
            c13x3*(-2*c20["y"]*c21["y"]*c23["y"] - c22["y"]*(2*c20["y"]*c22["y"] + c21y2) - c20["y"]*(2*c21["y"]*c23["y"] + c22y2) -
            c21["y"]*(2*c20["y"]*c23["y"] + 2*c21["y"]*c22["y"])),

        -c10["x"]*c11["x"]*c12["y"]*c13["x"]*c13["y"]*c23["y"] + c10["x"]*c11["y"]*c12["x"]*c13["x"]*c13["y"]*c23["y"] + 6*c10["x"]*c11["y"]*c12["y"]*c13["x"]*c13["y"]*c23["x"] -
            6*c10["y"]*c11["x"]*c12["x"]*c13["x"]*c13["y"]*c23["y"] - c10["y"]*c11["x"]*c12["y"]*c13["x"]*c13["y"]*c23["x"] + c10["y"]*c11["y"]*c12["x"]*c13["x"]*c13["y"]*c23["x"] +
            c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["x"]*c23["y"] - c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["y"]*c23["x"] + c11["x"]*c20["x"]*c12["y"]*c13["x"]*c13["y"]*c23["y"] +
            c11["x"]*c20["y"]*c12["y"]*c13["x"]*c13["y"]*c23["x"] + c11["x"]*c21["x"]*c12["y"]*c13["x"]*c13["y"]*c22["y"] + c11["x"]*c12["y"]*c13["x"]*c21["y"]*c22["x"]*c13["y"] -
            c20["x"]*c11["y"]*c12["x"]*c13["x"]*c13["y"]*c23["y"] - 6*c20["x"]*c11["y"]*c12["y"]*c13["x"]*c13["y"]*c23["x"] - c11["y"]*c12["x"]*c20["y"]*c13["x"]*c13["y"]*c23["x"] -
            c11["y"]*c12["x"]*c21["x"]*c13["x"]*c13["y"]*c22["y"] - c11["y"]*c12["x"]*c13["x"]*c21["y"]*c22["x"]*c13["y"] - 6*c11["y"]*c21["x"]*c12["y"]*c13["x"]*c22["x"]*c13["y"] -
            6*c10["x"]*c20["x"]*c13y3*c23["x"] - 6*c10["x"]*c21["x"]*c22["x"]*c13y3 - 2*c10["x"]*c12y3*c13["x"]*c23["x"] + 6*c20["x"]*c21["x"]*c22["x"]*c13y3 +
            2*c20["x"]*c12y3*c13["x"]*c23["x"] + 2*c21["x"]*c12y3*c13["x"]*c22["x"] + 2*c10["y"]*c12x3*c13["y"]*c23["y"] - 6*c10["x"]*c10["y"]*c13["x"]*c13y2*c23["x"] +
            3*c10["x"]*c11["x"]*c12["x"]*c13y2*c23["y"] - 2*c10["x"]*c11["x"]*c12["y"]*c13y2*c23["x"] - 4*c10["x"]*c11["y"]*c12["x"]*c13y2*c23["x"] +
            3*c10["y"]*c11["x"]*c12["x"]*c13y2*c23["x"] + 6*c10["x"]*c10["y"]*c13x2*c13["y"]*c23["y"] + 6*c10["x"]*c20["x"]*c13["x"]*c13y2*c23["y"] -
            3*c10["x"]*c11["y"]*c12["y"]*c13x2*c23["y"] + 2*c10["x"]*c12["x"]*c12y2*c13["x"]*c23["y"] + 2*c10["x"]*c12["x"]*c12y2*c13["y"]*c23["x"] +
            6*c10["x"]*c20["y"]*c13["x"]*c13y2*c23["x"] + 6*c10["x"]*c21["x"]*c13["x"]*c13y2*c22["y"] + 6*c10["x"]*c13["x"]*c21["y"]*c22["x"]*c13y2 +
            4*c10["y"]*c11["x"]*c12["y"]*c13x2*c23["y"] + 6*c10["y"]*c20["x"]*c13["x"]*c13y2*c23["x"] + 2*c10["y"]*c11["y"]*c12["x"]*c13x2*c23["y"] -
            3*c10["y"]*c11["y"]*c12["y"]*c13x2*c23["x"] + 2*c10["y"]*c12["x"]*c12y2*c13["x"]*c23["x"] + 6*c10["y"]*c21["x"]*c13["x"]*c22["x"]*c13y2 -
            3*c11["x"]*c20["x"]*c12["x"]*c13y2*c23["y"] + 2*c11["x"]*c20["x"]*c12["y"]*c13y2*c23["x"] + c11["x"]*c11["y"]*c12y2*c13["x"]*c23["x"] -
            3*c11["x"]*c12["x"]*c20["y"]*c13y2*c23["x"] - 3*c11["x"]*c12["x"]*c21["x"]*c13y2*c22["y"] - 3*c11["x"]*c12["x"]*c21["y"]*c22["x"]*c13y2 +
            2*c11["x"]*c21["x"]*c12["y"]*c22["x"]*c13y2 + 4*c20["x"]*c11["y"]*c12["x"]*c13y2*c23["x"] + 4*c11["y"]*c12["x"]*c21["x"]*c22["x"]*c13y2 -
            2*c10["x"]*c12x2*c12["y"]*c13["y"]*c23["y"] - 6*c10["y"]*c20["x"]*c13x2*c13["y"]*c23["y"] - 6*c10["y"]*c20["y"]*c13x2*c13["y"]*c23["x"] -
            6*c10["y"]*c21["x"]*c13x2*c13["y"]*c22["y"] - 2*c10["y"]*c12x2*c12["y"]*c13["x"]*c23["y"] - 2*c10["y"]*c12x2*c12["y"]*c13["y"]*c23["x"] -
            6*c10["y"]*c13x2*c21["y"]*c22["x"]*c13["y"] - c11["x"]*c11["y"]*c12x2*c13["y"]*c23["y"] - 2*c11["x"]*c11y2*c13["x"]*c13["y"]*c23["x"] +
            3*c20["x"]*c11["y"]*c12["y"]*c13x2*c23["y"] - 2*c20["x"]*c12["x"]*c12y2*c13["x"]*c23["y"] - 2*c20["x"]*c12["x"]*c12y2*c13["y"]*c23["x"] -
            6*c20["x"]*c20["y"]*c13["x"]*c13y2*c23["x"] - 6*c20["x"]*c21["x"]*c13["x"]*c13y2*c22["y"] - 6*c20["x"]*c13["x"]*c21["y"]*c22["x"]*c13y2 +
            3*c11["y"]*c20["y"]*c12["y"]*c13x2*c23["x"] + 3*c11["y"]*c21["x"]*c12["y"]*c13x2*c22["y"] + 3*c11["y"]*c12["y"]*c13x2*c21["y"]*c22["x"] -
            2*c12["x"]*c20["y"]*c12y2*c13["x"]*c23["x"] - 2*c12["x"]*c21["x"]*c12y2*c13["x"]*c22["y"] - 2*c12["x"]*c21["x"]*c12y2*c22["x"]*c13["y"] -
            2*c12["x"]*c12y2*c13["x"]*c21["y"]*c22["x"] - 6*c20["y"]*c21["x"]*c13["x"]*c22["x"]*c13y2 - c11y2*c12["x"]*c12["y"]*c13["x"]*c23["x"] +
            2*c20["x"]*c12x2*c12["y"]*c13["y"]*c23["y"] + 6*c20["y"]*c13x2*c21["y"]*c22["x"]*c13["y"] + 2*c11x2*c11["y"]*c13["x"]*c13["y"]*c23["y"] +
            c11x2*c12["x"]*c12["y"]*c13["y"]*c23["y"] + 2*c12x2*c20["y"]*c12["y"]*c13["y"]*c23["x"] + 2*c12x2*c21["x"]*c12["y"]*c13["y"]*c22["y"] +
            2*c12x2*c12["y"]*c21["y"]*c22["x"]*c13["y"] + c21x3*c13y3 + 3*c10x2*c13y3*c23["x"] - 3*c10y2*c13x3*c23["y"] +
            3*c20x2*c13y3*c23["x"] + c11y3*c13x2*c23["x"] - c11x3*c13y2*c23["y"] - c11["x"]*c11y2*c13x2*c23["y"] +
            c11x2*c11["y"]*c13y2*c23["x"] - 3*c10x2*c13["x"]*c13y2*c23["y"] + 3*c10y2*c13x2*c13["y"]*c23["x"] - c11x2*c12y2*c13["x"]*c23["y"] +
            c11y2*c12x2*c13["y"]*c23["x"] - 3*c21x2*c13["x"]*c21["y"]*c13y2 - 3*c20x2*c13["x"]*c13y2*c23["y"] + 3*c20y2*c13x2*c13["y"]*c23["x"] +
            c11["x"]*c12["x"]*c13["x"]*c13["y"]*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) + c12x3*c13["y"]*(-2*c20["y"]*c23["y"] - 2*c21["y"]*c22["y"]) +
            c10["y"]*c13x3*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) + c11["y"]*c12["x"]*c13x2*(-2*c20["y"]*c23["y"] - 2*c21["y"]*c22["y"]) +
            c12x2*c12["y"]*c13["x"]*(2*c20["y"]*c23["y"] + 2*c21["y"]*c22["y"]) + c11["x"]*c12["y"]*c13x2*(-4*c20["y"]*c23["y"] - 4*c21["y"]*c22["y"]) +
            c10["x"]*c13x2*c13["y"]*(-6*c20["y"]*c23["y"] - 6*c21["y"]*c22["y"]) + c20["x"]*c13x2*c13["y"]*(6*c20["y"]*c23["y"] + 6*c21["y"]*c22["y"]) +
            c21["x"]*c13x2*c13["y"]*(6*c20["y"]*c22["y"] + 3*c21y2) + c13x3*(-2*c20["y"]*c21["y"]*c22["y"] - c20y2*c23["y"] -
            c21["y"]*(2*c20["y"]*c22["y"] + c21y2) - c20["y"]*(2*c20["y"]*c23["y"] + 2*c21["y"]*c22["y"])),

        -c10["x"]*c11["x"]*c12["y"]*c13["x"]*c13["y"]*c22["y"] + c10["x"]*c11["y"]*c12["x"]*c13["x"]*c13["y"]*c22["y"] + 6*c10["x"]*c11["y"]*c12["y"]*c13["x"]*c22["x"]*c13["y"] -
            6*c10["y"]*c11["x"]*c12["x"]*c13["x"]*c13["y"]*c22["y"] - c10["y"]*c11["x"]*c12["y"]*c13["x"]*c22["x"]*c13["y"] + c10["y"]*c11["y"]*c12["x"]*c13["x"]*c22["x"]*c13["y"] +
            c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["x"]*c22["y"] - c11["x"]*c11["y"]*c12["x"]*c12["y"]*c22["x"]*c13["y"] + c11["x"]*c20["x"]*c12["y"]*c13["x"]*c13["y"]*c22["y"] +
            c11["x"]*c20["y"]*c12["y"]*c13["x"]*c22["x"]*c13["y"] + c11["x"]*c21["x"]*c12["y"]*c13["x"]*c21["y"]*c13["y"] - c20["x"]*c11["y"]*c12["x"]*c13["x"]*c13["y"]*c22["y"] -
            6*c20["x"]*c11["y"]*c12["y"]*c13["x"]*c22["x"]*c13["y"] - c11["y"]*c12["x"]*c20["y"]*c13["x"]*c22["x"]*c13["y"] - c11["y"]*c12["x"]*c21["x"]*c13["x"]*c21["y"]*c13["y"] -
            6*c10["x"]*c20["x"]*c22["x"]*c13y3 - 2*c10["x"]*c12y3*c13["x"]*c22["x"] + 2*c20["x"]*c12y3*c13["x"]*c22["x"] + 2*c10["y"]*c12x3*c13["y"]*c22["y"] -
            6*c10["x"]*c10["y"]*c13["x"]*c22["x"]*c13y2 + 3*c10["x"]*c11["x"]*c12["x"]*c13y2*c22["y"] - 2*c10["x"]*c11["x"]*c12["y"]*c22["x"]*c13y2 -
            4*c10["x"]*c11["y"]*c12["x"]*c22["x"]*c13y2 + 3*c10["y"]*c11["x"]*c12["x"]*c22["x"]*c13y2 + 6*c10["x"]*c10["y"]*c13x2*c13["y"]*c22["y"] +
            6*c10["x"]*c20["x"]*c13["x"]*c13y2*c22["y"] - 3*c10["x"]*c11["y"]*c12["y"]*c13x2*c22["y"] + 2*c10["x"]*c12["x"]*c12y2*c13["x"]*c22["y"] +
            2*c10["x"]*c12["x"]*c12y2*c22["x"]*c13["y"] + 6*c10["x"]*c20["y"]*c13["x"]*c22["x"]*c13y2 + 6*c10["x"]*c21["x"]*c13["x"]*c21["y"]*c13y2 +
            4*c10["y"]*c11["x"]*c12["y"]*c13x2*c22["y"] + 6*c10["y"]*c20["x"]*c13["x"]*c22["x"]*c13y2 + 2*c10["y"]*c11["y"]*c12["x"]*c13x2*c22["y"] -
            3*c10["y"]*c11["y"]*c12["y"]*c13x2*c22["x"] + 2*c10["y"]*c12["x"]*c12y2*c13["x"]*c22["x"] - 3*c11["x"]*c20["x"]*c12["x"]*c13y2*c22["y"] +
            2*c11["x"]*c20["x"]*c12["y"]*c22["x"]*c13y2 + c11["x"]*c11["y"]*c12y2*c13["x"]*c22["x"] - 3*c11["x"]*c12["x"]*c20["y"]*c22["x"]*c13y2 -
            3*c11["x"]*c12["x"]*c21["x"]*c21["y"]*c13y2 + 4*c20["x"]*c11["y"]*c12["x"]*c22["x"]*c13y2 - 2*c10["x"]*c12x2*c12["y"]*c13["y"]*c22["y"] -
            6*c10["y"]*c20["x"]*c13x2*c13["y"]*c22["y"] - 6*c10["y"]*c20["y"]*c13x2*c22["x"]*c13["y"] - 6*c10["y"]*c21["x"]*c13x2*c21["y"]*c13["y"] -
            2*c10["y"]*c12x2*c12["y"]*c13["x"]*c22["y"] - 2*c10["y"]*c12x2*c12["y"]*c22["x"]*c13["y"] - c11["x"]*c11["y"]*c12x2*c13["y"]*c22["y"] -
            2*c11["x"]*c11y2*c13["x"]*c22["x"]*c13["y"] + 3*c20["x"]*c11["y"]*c12["y"]*c13x2*c22["y"] - 2*c20["x"]*c12["x"]*c12y2*c13["x"]*c22["y"] -
            2*c20["x"]*c12["x"]*c12y2*c22["x"]*c13["y"] - 6*c20["x"]*c20["y"]*c13["x"]*c22["x"]*c13y2 - 6*c20["x"]*c21["x"]*c13["x"]*c21["y"]*c13y2 +
            3*c11["y"]*c20["y"]*c12["y"]*c13x2*c22["x"] + 3*c11["y"]*c21["x"]*c12["y"]*c13x2*c21["y"] - 2*c12["x"]*c20["y"]*c12y2*c13["x"]*c22["x"] -
            2*c12["x"]*c21["x"]*c12y2*c13["x"]*c21["y"] - c11y2*c12["x"]*c12["y"]*c13["x"]*c22["x"] + 2*c20["x"]*c12x2*c12["y"]*c13["y"]*c22["y"] -
            3*c11["y"]*c21x2*c12["y"]*c13["x"]*c13["y"] + 6*c20["y"]*c21["x"]*c13x2*c21["y"]*c13["y"] + 2*c11x2*c11["y"]*c13["x"]*c13["y"]*c22["y"] +
            c11x2*c12["x"]*c12["y"]*c13["y"]*c22["y"] + 2*c12x2*c20["y"]*c12["y"]*c22["x"]*c13["y"] + 2*c12x2*c21["x"]*c12["y"]*c21["y"]*c13["y"] -
            3*c10["x"]*c21x2*c13y3 + 3*c20["x"]*c21x2*c13y3 + 3*c10x2*c22["x"]*c13y3 - 3*c10y2*c13x3*c22["y"] + 3*c20x2*c22["x"]*c13y3 +
            c21x2*c12y3*c13["x"] + c11y3*c13x2*c22["x"] - c11x3*c13y2*c22["y"] + 3*c10["y"]*c21x2*c13["x"]*c13y2 -
            c11["x"]*c11y2*c13x2*c22["y"] + c11["x"]*c21x2*c12["y"]*c13y2 + 2*c11["y"]*c12["x"]*c21x2*c13y2 + c11x2*c11["y"]*c22["x"]*c13y2 -
            c12["x"]*c21x2*c12y2*c13["y"] - 3*c20["y"]*c21x2*c13["x"]*c13y2 - 3*c10x2*c13["x"]*c13y2*c22["y"] + 3*c10y2*c13x2*c22["x"]*c13["y"] -
            c11x2*c12y2*c13["x"]*c22["y"] + c11y2*c12x2*c22["x"]*c13["y"] - 3*c20x2*c13["x"]*c13y2*c22["y"] + 3*c20y2*c13x2*c22["x"]*c13["y"] +
            c12x2*c12["y"]*c13["x"]*(2*c20["y"]*c22["y"] + c21y2) + c11["x"]*c12["x"]*c13["x"]*c13["y"]*(6*c20["y"]*c22["y"] + 3*c21y2) +
            c12x3*c13["y"]*(-2*c20["y"]*c22["y"] - c21y2) + c10["y"]*c13x3*(6*c20["y"]*c22["y"] + 3*c21y2) +
            c11["y"]*c12["x"]*c13x2*(-2*c20["y"]*c22["y"] - c21y2) + c11["x"]*c12["y"]*c13x2*(-4*c20["y"]*c22["y"] - 2*c21y2) +
            c10["x"]*c13x2*c13["y"]*(-6*c20["y"]*c22["y"] - 3*c21y2) + c20["x"]*c13x2*c13["y"]*(6*c20["y"]*c22["y"] + 3*c21y2) +
            c13x3*(-2*c20["y"]*c21y2 - c20y2*c22["y"] - c20["y"]*(2*c20["y"]*c22["y"] + c21y2)),

        -c10["x"]*c11["x"]*c12["y"]*c13["x"]*c21["y"]*c13["y"] + c10["x"]*c11["y"]*c12["x"]*c13["x"]*c21["y"]*c13["y"] + 6*c10["x"]*c11["y"]*c21["x"]*c12["y"]*c13["x"]*c13["y"] -
            6*c10["y"]*c11["x"]*c12["x"]*c13["x"]*c21["y"]*c13["y"] - c10["y"]*c11["x"]*c21["x"]*c12["y"]*c13["x"]*c13["y"] + c10["y"]*c11["y"]*c12["x"]*c21["x"]*c13["x"]*c13["y"] -
            c11["x"]*c11["y"]*c12["x"]*c21["x"]*c12["y"]*c13["y"] + c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["x"]*c21["y"] + c11["x"]*c20["x"]*c12["y"]*c13["x"]*c21["y"]*c13["y"] +
            6*c11["x"]*c12["x"]*c20["y"]*c13["x"]*c21["y"]*c13["y"] + c11["x"]*c20["y"]*c21["x"]*c12["y"]*c13["x"]*c13["y"] - c20["x"]*c11["y"]*c12["x"]*c13["x"]*c21["y"]*c13["y"] -
            6*c20["x"]*c11["y"]*c21["x"]*c12["y"]*c13["x"]*c13["y"] - c11["y"]*c12["x"]*c20["y"]*c21["x"]*c13["x"]*c13["y"] - 6*c10["x"]*c20["x"]*c21["x"]*c13y3 -
            2*c10["x"]*c21["x"]*c12y3*c13["x"] + 6*c10["y"]*c20["y"]*c13x3*c21["y"] + 2*c20["x"]*c21["x"]*c12y3*c13["x"] + 2*c10["y"]*c12x3*c21["y"]*c13["y"] -
            2*c12x3*c20["y"]*c21["y"]*c13["y"] - 6*c10["x"]*c10["y"]*c21["x"]*c13["x"]*c13y2 + 3*c10["x"]*c11["x"]*c12["x"]*c21["y"]*c13y2 -
            2*c10["x"]*c11["x"]*c21["x"]*c12["y"]*c13y2 - 4*c10["x"]*c11["y"]*c12["x"]*c21["x"]*c13y2 + 3*c10["y"]*c11["x"]*c12["x"]*c21["x"]*c13y2 +
            6*c10["x"]*c10["y"]*c13x2*c21["y"]*c13["y"] + 6*c10["x"]*c20["x"]*c13["x"]*c21["y"]*c13y2 - 3*c10["x"]*c11["y"]*c12["y"]*c13x2*c21["y"] +
            2*c10["x"]*c12["x"]*c21["x"]*c12y2*c13["y"] + 2*c10["x"]*c12["x"]*c12y2*c13["x"]*c21["y"] + 6*c10["x"]*c20["y"]*c21["x"]*c13["x"]*c13y2 +
            4*c10["y"]*c11["x"]*c12["y"]*c13x2*c21["y"] + 6*c10["y"]*c20["x"]*c21["x"]*c13["x"]*c13y2 + 2*c10["y"]*c11["y"]*c12["x"]*c13x2*c21["y"] -
            3*c10["y"]*c11["y"]*c21["x"]*c12["y"]*c13x2 + 2*c10["y"]*c12["x"]*c21["x"]*c12y2*c13["x"] - 3*c11["x"]*c20["x"]*c12["x"]*c21["y"]*c13y2 +
            2*c11["x"]*c20["x"]*c21["x"]*c12["y"]*c13y2 + c11["x"]*c11["y"]*c21["x"]*c12y2*c13["x"] - 3*c11["x"]*c12["x"]*c20["y"]*c21["x"]*c13y2 +
            4*c20["x"]*c11["y"]*c12["x"]*c21["x"]*c13y2 - 6*c10["x"]*c20["y"]*c13x2*c21["y"]*c13["y"] - 2*c10["x"]*c12x2*c12["y"]*c21["y"]*c13["y"] -
            6*c10["y"]*c20["x"]*c13x2*c21["y"]*c13["y"] - 6*c10["y"]*c20["y"]*c21["x"]*c13x2*c13["y"] - 2*c10["y"]*c12x2*c21["x"]*c12["y"]*c13["y"] -
            2*c10["y"]*c12x2*c12["y"]*c13["x"]*c21["y"] - c11["x"]*c11["y"]*c12x2*c21["y"]*c13["y"] - 4*c11["x"]*c20["y"]*c12["y"]*c13x2*c21["y"] -
            2*c11["x"]*c11y2*c21["x"]*c13["x"]*c13["y"] + 3*c20["x"]*c11["y"]*c12["y"]*c13x2*c21["y"] - 2*c20["x"]*c12["x"]*c21["x"]*c12y2*c13["y"] -
            2*c20["x"]*c12["x"]*c12y2*c13["x"]*c21["y"] - 6*c20["x"]*c20["y"]*c21["x"]*c13["x"]*c13y2 - 2*c11["y"]*c12["x"]*c20["y"]*c13x2*c21["y"] +
            3*c11["y"]*c20["y"]*c21["x"]*c12["y"]*c13x2 - 2*c12["x"]*c20["y"]*c21["x"]*c12y2*c13["x"] - c11y2*c12["x"]*c21["x"]*c12["y"]*c13["x"] +
            6*c20["x"]*c20["y"]*c13x2*c21["y"]*c13["y"] + 2*c20["x"]*c12x2*c12["y"]*c21["y"]*c13["y"] + 2*c11x2*c11["y"]*c13["x"]*c21["y"]*c13["y"] +
            c11x2*c12["x"]*c12["y"]*c21["y"]*c13["y"] + 2*c12x2*c20["y"]*c21["x"]*c12["y"]*c13["y"] + 2*c12x2*c20["y"]*c12["y"]*c13["x"]*c21["y"] +
            3*c10x2*c21["x"]*c13y3 - 3*c10y2*c13x3*c21["y"] + 3*c20x2*c21["x"]*c13y3 + c11y3*c21["x"]*c13x2 - c11x3*c21["y"]*c13y2 -
            3*c20y2*c13x3*c21["y"] - c11["x"]*c11y2*c13x2*c21["y"] + c11x2*c11["y"]*c21["x"]*c13y2 - 3*c10x2*c13["x"]*c21["y"]*c13y2 +
            3*c10y2*c21["x"]*c13x2*c13["y"] - c11x2*c12y2*c13["x"]*c21["y"] + c11y2*c12x2*c21["x"]*c13["y"] - 3*c20x2*c13["x"]*c21["y"]*c13y2 +
            3*c20y2*c21["x"]*c13x2*c13["y"],
            
        c10["x"]*c10["y"]*c11["x"]*c12["y"]*c13["x"]*c13["y"] - c10["x"]*c10["y"]*c11["y"]*c12["x"]*c13["x"]*c13["y"] + c10["x"]*c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["y"] -
            c10["y"]*c11["x"]*c11["y"]*c12["x"]*c12["y"]*c13["x"] - c10["x"]*c11["x"]*c20["y"]*c12["y"]*c13["x"]*c13["y"] + 6*c10["x"]*c20["x"]*c11["y"]*c12["y"]*c13["x"]*c13["y"] +
            c10["x"]*c11["y"]*c12["x"]*c20["y"]*c13["x"]*c13["y"] - c10["y"]*c11["x"]*c20["x"]*c12["y"]*c13["x"]*c13["y"] - 6*c10["y"]*c11["x"]*c12["x"]*c20["y"]*c13["x"]*c13["y"] +
            c10["y"]*c20["x"]*c11["y"]*c12["x"]*c13["x"]*c13["y"] - c11["x"]*c20["x"]*c11["y"]*c12["x"]*c12["y"]*c13["y"] + c11["x"]*c11["y"]*c12["x"]*c20["y"]*c12["y"]*c13["x"] +
            c11["x"]*c20["x"]*c20["y"]*c12["y"]*c13["x"]*c13["y"] - c20["x"]*c11["y"]*c12["x"]*c20["y"]*c13["x"]*c13["y"] - 2*c10["x"]*c20["x"]*c12y3*c13["x"] +
            2*c10["y"]*c12x3*c20["y"]*c13["y"] - 3*c10["x"]*c10["y"]*c11["x"]*c12["x"]*c13y2 - 6*c10["x"]*c10["y"]*c20["x"]*c13["x"]*c13y2 +
            3*c10["x"]*c10["y"]*c11["y"]*c12["y"]*c13x2 - 2*c10["x"]*c10["y"]*c12["x"]*c12y2*c13["x"] - 2*c10["x"]*c11["x"]*c20["x"]*c12["y"]*c13y2 -
            c10["x"]*c11["x"]*c11["y"]*c12y2*c13["x"] + 3*c10["x"]*c11["x"]*c12["x"]*c20["y"]*c13y2 - 4*c10["x"]*c20["x"]*c11["y"]*c12["x"]*c13y2 +
            3*c10["y"]*c11["x"]*c20["x"]*c12["x"]*c13y2 + 6*c10["x"]*c10["y"]*c20["y"]*c13x2*c13["y"] + 2*c10["x"]*c10["y"]*c12x2*c12["y"]*c13["y"] +
            2*c10["x"]*c11["x"]*c11y2*c13["x"]*c13["y"] + 2*c10["x"]*c20["x"]*c12["x"]*c12y2*c13["y"] + 6*c10["x"]*c20["x"]*c20["y"]*c13["x"]*c13y2 -
            3*c10["x"]*c11["y"]*c20["y"]*c12["y"]*c13x2 + 2*c10["x"]*c12["x"]*c20["y"]*c12y2*c13["x"] + c10["x"]*c11y2*c12["x"]*c12["y"]*c13["x"] +
            c10["y"]*c11["x"]*c11["y"]*c12x2*c13["y"] + 4*c10["y"]*c11["x"]*c20["y"]*c12["y"]*c13x2 - 3*c10["y"]*c20["x"]*c11["y"]*c12["y"]*c13x2 +
            2*c10["y"]*c20["x"]*c12["x"]*c12y2*c13["x"] + 2*c10["y"]*c11["y"]*c12["x"]*c20["y"]*c13x2 + c11["x"]*c20["x"]*c11["y"]*c12y2*c13["x"] -
            3*c11["x"]*c20["x"]*c12["x"]*c20["y"]*c13y2 - 2*c10["x"]*c12x2*c20["y"]*c12["y"]*c13["y"] - 6*c10["y"]*c20["x"]*c20["y"]*c13x2*c13["y"] -
            2*c10["y"]*c20["x"]*c12x2*c12["y"]*c13["y"] - 2*c10["y"]*c11x2*c11["y"]*c13["x"]*c13["y"] - c10["y"]*c11x2*c12["x"]*c12["y"]*c13["y"] -
            2*c10["y"]*c12x2*c20["y"]*c12["y"]*c13["x"] - 2*c11["x"]*c20["x"]*c11y2*c13["x"]*c13["y"] - c11["x"]*c11["y"]*c12x2*c20["y"]*c13["y"] +
            3*c20["x"]*c11["y"]*c20["y"]*c12["y"]*c13x2 - 2*c20["x"]*c12["x"]*c20["y"]*c12y2*c13["x"] - c20["x"]*c11y2*c12["x"]*c12["y"]*c13["x"] +
            3*c10y2*c11["x"]*c12["x"]*c13["x"]*c13["y"] + 3*c11["x"]*c12["x"]*c20y2*c13["x"]*c13["y"] + 2*c20["x"]*c12x2*c20["y"]*c12["y"]*c13["y"] -
            3*c10x2*c11["y"]*c12["y"]*c13["x"]*c13["y"] + 2*c11x2*c11["y"]*c20["y"]*c13["x"]*c13["y"] + c11x2*c12["x"]*c20["y"]*c12["y"]*c13["y"] -
            3*c20x2*c11["y"]*c12["y"]*c13["x"]*c13["y"] - c10x3*c13y3 + c10y3*c13x3 + c20x3*c13y3 - c20y3*c13x3 -
            3*c10["x"]*c20x2*c13y3 - c10["x"]*c11y3*c13x2 + 3*c10x2*c20["x"]*c13y3 + c10["y"]*c11x3*c13y2 +
            3*c10["y"]*c20y2*c13x3 + c20["x"]*c11y3*c13x2 + c10x2*c12y3*c13["x"] - 3*c10y2*c20["y"]*c13x3 - c10y2*c12x3*c13["y"] +
            c20x2*c12y3*c13["x"] - c11x3*c20["y"]*c13y2 - c12x3*c20y2*c13["y"] - c10["x"]*c11x2*c11["y"]*c13y2 +
            c10["y"]*c11["x"]*c11y2*c13x2 - 3*c10["x"]*c10y2*c13x2*c13["y"] - c10["x"]*c11y2*c12x2*c13["y"] + c10["y"]*c11x2*c12y2*c13["x"] -
            c11["x"]*c11y2*c20["y"]*c13x2 + 3*c10x2*c10["y"]*c13["x"]*c13y2 + c10x2*c11["x"]*c12["y"]*c13y2 +
            2*c10x2*c11["y"]*c12["x"]*c13y2 - 2*c10y2*c11["x"]*c12["y"]*c13x2 - c10y2*c11["y"]*c12["x"]*c13x2 + c11x2*c20["x"]*c11["y"]*c13y2 -
            3*c10["x"]*c20y2*c13x2*c13["y"] + 3*c10["y"]*c20x2*c13["x"]*c13y2 + c11["x"]*c20x2*c12["y"]*c13y2 - 2*c11["x"]*c20y2*c12["y"]*c13x2 +
            c20["x"]*c11y2*c12x2*c13["y"] - c11["y"]*c12["x"]*c20y2*c13x2 - c10x2*c12["x"]*c12y2*c13["y"] - 3*c10x2*c20["y"]*c13["x"]*c13y2 +
            3*c10y2*c20["x"]*c13x2*c13["y"] + c10y2*c12x2*c12["y"]*c13["x"] - c11x2*c20["y"]*c12y2*c13["x"] + 2*c20x2*c11["y"]*c12["x"]*c13y2 +
            3*c20["x"]*c20y2*c13x2*c13["y"] - c20x2*c12["x"]*c12y2*c13["y"] - 3*c20x2*c20["y"]*c13["x"]*c13y2 + c12x2*c20y2*c12["y"]*c13["x"]
	]

	roots = get_roots_in_interval(coefs, 0, 1)

	# p = []

	# i = 0
	# while i < 9:
	# 	if i < len(roots):
	# 		t = roots[i]
	# 		i += 1
	# 		x = (1 - t)*(1 - t)*(1 - t)*b1["x"] + 3*t*(1-t)*(1-t)*b2["x"] + 3*t*t*(1-t)*b3["x"] + t*t*t*b4["x"]
	# 		y = (1 - t)*(1 - t)*(1 - t)*b1["y"] + 3*t*(1-t)*(1-t)*b2["y"] + 3*t*t*(1-t)*b3["y"] + t*t*t*b4["y"]
	# 		p.append(x)
	# 		result["points"].append({"x": x, "y": y})
	# 	else:
	#   		result["points"].append({"x": -10000, "y": -10000})
	#   		i += 1

	# r_x = [
	# 	-a1["x"]+3*a2["x"]-3*a3["x"]+a4["x"],
	# 	3*a1["x"] - 6*a2["x"] + 3*a3["x"],
	# 	-3*a1["x"] + 3*a2["x"],
	# 	a1["x"] - p[2]
	# ]

	# ro = get_roots(r_x)
	# print(ro)

	res = []

	i = 0
	while i < len(roots):
		s = roots[i]
		i += 1
		x_coefs = [
			c13["x"],
			c12["x"],
			c11["x"],
			c10["x"] - c20["x"] - s*c21["x"] - s*s*c22["x"] - s*s*s*c23["x"]
		]
		x_roots = get_roots(x_coefs)
		y_coefs = [
			c13["y"],
			c12["y"],
			c11["y"],
			c10["y"] - c20["y"] - s*c21["y"] - s*s*c22["y"] - s*s*s*c23["y"]
		]
		y_roots = get_roots(y_coefs)

		if len(x_roots) > 0 and len(y_roots) > 0:
			j = 0
			while j < len(x_roots):
				x_root = x_roots[j]
				j += 1
				if 0 <= x_root and x_root <= 1:
					k = 0
					while k < len(y_roots):
						if abs( x_root - y_roots[k] ) < exp(-4):
							z1 = multiply(c21, s)
							z1 = add(z1, c20)
							z2 = multiply(c22, s*s)
							z2 = add(z2, z1)
							z3 = multiply(c23, s*s*s)
							z3 = add(z3, z2)
							result["points"].append({"x": z3["x"], "y": z3["y"]})
						k += 1
	
	i = len(result["points"])
	while i < 9:
		result["points"].append({"x": -10000, "y": -10000})
		i += 1
	return result


def curve_to_axis(curve1, axis):
  '''
    Пересечение кривой и оси
  '''
  pass


def curve_to_arc(p1, p2, p3, p4, angle1, angle2, point_center_arc, radius_arc):
	result = { "info": "No intersection", "points": [] }
	finish_result = { "info": "No intersection", "points": [] }
	
	a = multiply(p1, -1)
	b = multiply(p2, 3)
	c = multiply(p3, -3)
	d = add(p4, c)
	d = add(b, d)
	d = add(a, d)
	c3 = d

	a = multiply(p1, 3)
	b = multiply(p2, -6)
	c = multiply(p3, 3)
	d = add(b, c)
	d = add(a, d)
	c2 = d

	a = multiply(p1, -3)
	b = multiply(p2, 3)
	c = add(a, b)
	c1 = c

	c0 = p1

	rxrx = radius_arc*radius_arc
	ryry = radius_arc*radius_arc
	coefs = [
		c3["x"]*c3["x"]*ryry + c3["y"]*c3["y"]*rxrx,
		2*(c3["x"]*c2["x"]*ryry + c3["y"]*c2["y"]*rxrx),
		2*(c3["x"]*c1["x"]*ryry + c3["y"]*c1["y"]*rxrx) + c2["x"]*c2["x"]*ryry + c2["y"]*c2["y"]*rxrx,
		2*c3["x"]*ryry*(c0["x"] - point_center_arc[0]) + 2*c3["y"]*rxrx*(c0["y"] - point_center_arc[1]) + 2*(c2["x"]*c1["x"]*ryry + c2["y"]*c1["y"]*rxrx),
		2*c2["x"]*ryry*(c0["x"] - point_center_arc[0]) + 2*c2["y"]*rxrx*(c0["y"] - point_center_arc[1]) + c1["x"]*c1["x"]*ryry + c1["y"]*c1["y"]*rxrx,
		2*c1["x"]*ryry*(c0["x"] - point_center_arc[0]) + 2*c1["y"]*rxrx*(c0["y"] - point_center_arc[1]),
		c0["x"]*c0["x"]*ryry - 2*c0["y"]*point_center_arc[1]*rxrx - 2*c0["x"]*point_center_arc[0]*ryry + c0["y"]*c0["y"]*rxrx + point_center_arc[0]*point_center_arc[0]*ryry + point_center_arc[1]*point_center_arc[1]*rxrx - rxrx*ryry
	]

	roots = get_roots_in_interval(coefs, 0, 1)
	start_x_arc = point_center_arc[0] + radius_arc * cos(0 * pi / 180)
	start_y_arc = point_center_arc[1] + radius_arc * sin(0 * pi / 180)
	i = 0 
	while i < 6:
		if i < len(roots):
			t = roots[i]
			i += 1
			z1 = multiply(c1, t)
			z1 = add(z1, c0)
			z2 = multiply(c2, t*t)
			z2 = add(z2, z1)
			z3 = multiply(c3, t*t*t)
			z3 = add(z3, z2)
			ac_len = sqrt((point_center_arc[0] - z3["x"])*(point_center_arc[0] - z3["x"]) + (point_center_arc[1] - z3["y"])*(point_center_arc[1] - z3["y"]))
			ab_len = sqrt((point_center_arc[0] - start_x_arc)*(point_center_arc[0] - start_x_arc) + (point_center_arc[1] - start_y_arc)*(point_center_arc[1] - start_y_arc))
			bc_len = sqrt((z3["x"] - start_x_arc)*(z3["x"] - start_x_arc) + (z3["y"] - start_y_arc)*(z3["y"] - start_y_arc))
			alfa = (ac_len*ac_len + ab_len*ab_len - bc_len*bc_len) / (2*ac_len*ab_len)
			if z3["y"] < point_center_arc[1]:
				angle_point = 360 - degrees(acos(alfa))
			else:
				angle_point = degrees(acos(alfa))
			if angle_point >= angle1 and angle_point <= angle2:
				result["points"].append({"x": z3["x"], "y": z3["y"]})
			else:
				result["points"].append({"x": -10000, "y": -10000})
		else:
			result["points"].append({"x": -10000, "y": -10000})
			i += 1


	return result


def arc_to_arc(point_center_arc1, angle1_arc1, angle2_arc1, radius_arc_1, point_center_arc2, angle1_arc2, angle2_arc2, radius_arc_2):
  '''
    Пересечение дуг
  '''
  result = { "info": "", "points": [] }
  if point_center_arc1[0] == point_center_arc2[0] and point_center_arc1[1] == point_center_arc2[1]:
  	result["info"] = "No intersection"
  	result["points"].append({"x": -10000, "y": -10000})
  	result["points"].append({"x": -10000, "y": -10000})
  else:
  	sum_radius = radius_arc_1 + radius_arc_2
  	length_center_to_center = sqrt((point_center_arc1[0]-point_center_arc2[0])*(point_center_arc1[0]-point_center_arc2[0]) + (point_center_arc1[1]-point_center_arc2[1])*(point_center_arc1[1]-point_center_arc2[1]))
  	if sum_radius+0.0001 < length_center_to_center:
  		result["info"] = "No intersection"
  		result["points"].append({"x": -10000, "y": -10000})
  		result["points"].append({"x": -10000, "y": -10000})
  	else:
  		result["info"] = "Intersection"
  		a = (radius_arc_1*radius_arc_1 - radius_arc_2*radius_arc_2 + length_center_to_center*length_center_to_center)/(2*length_center_to_center)
  		h = sqrt(radius_arc_1*radius_arc_1 - a*a)

  		xp2 = point_center_arc1[0] + (a*(point_center_arc2[0]-point_center_arc1[0]))/length_center_to_center
  		yp2 = point_center_arc1[1] + (a*(point_center_arc2[1]-point_center_arc1[1]))/length_center_to_center

  		x1 = xp2 + h*(point_center_arc2[1]-point_center_arc1[1])/length_center_to_center
  		y1 = yp2 - h*(point_center_arc2[0]-point_center_arc1[0])/length_center_to_center
  		x2 = xp2 - h*(point_center_arc2[1]-point_center_arc1[1])/length_center_to_center
  		y2 = yp2 + h*(point_center_arc2[0]-point_center_arc1[0])/length_center_to_center

  		start_x_arc1 = point_center_arc1[0] + radius_arc_1 * cos(0*pi/180)
  		start_y_arc1 = point_center_arc1[1] + radius_arc_1 * sin(0*pi/180)
  		start_x_arc2 = point_center_arc2[0] + radius_arc_2 * cos(0*pi/180)
  		start_y_arc2 = point_center_arc2[1] + radius_arc_2 * sin(0*pi/180)

  		ac_side1_arc1 = sqrt((point_center_arc1[0]-x1)*(point_center_arc1[0]-x1) + (point_center_arc1[1]-y1)*(point_center_arc1[1]-y1))
  		ab_side1_arc1 = sqrt((point_center_arc1[0]-start_x_arc1)*(point_center_arc1[0]-start_x_arc1) + (point_center_arc1[1]-start_y_arc1)*(point_center_arc1[1]-start_y_arc1))
  		bc_side1_arc1 = sqrt((x1-start_x_arc1)*(x1-start_x_arc1) + (y1-start_y_arc1)*(y1-start_y_arc1))
  		ac_side1_arc2 = sqrt((point_center_arc2[0]-x1)*(point_center_arc2[0]-x1) + (point_center_arc2[1]-y1)*(point_center_arc2[1]-y1))
  		ab_side1_arc2 = sqrt((point_center_arc2[0]-start_x_arc2)*(point_center_arc2[0]-start_x_arc2) + (point_center_arc2[1]-start_y_arc2)*(point_center_arc2[1]-start_y_arc2))
  		bc_side1_arc2 = sqrt((x1-start_x_arc2)*(x1-start_x_arc2) + (y1-start_y_arc2)*(y1-start_y_arc2))

  		ac_side2_arc1 = sqrt((point_center_arc1[0]-x2)*(point_center_arc1[0]-x2) + (point_center_arc1[1]-y2)*(point_center_arc1[1]-y2))
  		ab_side2_arc1 = sqrt((point_center_arc1[0]-start_x_arc1)*(point_center_arc1[0]-start_x_arc1) + (point_center_arc1[1]-start_y_arc1)*(point_center_arc1[1]-start_y_arc1))
  		bc_side2_arc1 = sqrt((x2-start_x_arc1)*(x2-start_x_arc1) + (y2-start_y_arc1)*(y2-start_y_arc1))
  		ac_side2_arc2 = sqrt((point_center_arc2[0]-x2)*(point_center_arc2[0]-x2) + (point_center_arc2[1]-y2)*(point_center_arc2[1]-y2))
  		ab_side2_arc2 = sqrt((point_center_arc2[0]-start_x_arc2)*(point_center_arc2[0]-start_x_arc2) + (point_center_arc2[1]-start_y_arc2)*(point_center_arc2[1]-start_y_arc2))
  		bc_side2_arc2 = sqrt((x2-start_x_arc2)*(x2-start_x_arc2) + (y2-start_y_arc2)*(y2-start_y_arc2))

  		alfa1_arc1 = (ac_side1_arc1*ac_side1_arc1 + ab_side1_arc1*ab_side1_arc1 - bc_side1_arc1*bc_side1_arc1)/(2 * ac_side1_arc1 * ab_side1_arc1)
  		alfa1_arc2 = (ac_side1_arc2*ac_side1_arc2 + ab_side1_arc2*ab_side1_arc2 - bc_side1_arc2*bc_side1_arc2)/(2 * ac_side1_arc2 * ab_side1_arc2)

  		alfa2_arc1 = (ac_side2_arc1*ac_side2_arc1 + ab_side2_arc1*ab_side2_arc1 - bc_side2_arc1*bc_side2_arc1)/(2 * ac_side2_arc1 * ab_side2_arc1)
  		alfa2_arc2 = (ac_side2_arc2*ac_side2_arc2 + ab_side2_arc2*ab_side2_arc2 - bc_side2_arc2*bc_side2_arc2)/(2 * ac_side2_arc2 * ab_side2_arc2)

  		angle_point = [[0, 0],[0, 0]]
  		if y1 < point_center_arc1[1]:
  			angle_point[0][0] = 360 - degrees(acos(alfa1_arc1))
  		else:
  			angle_point[0][0] = degrees(acos(alfa1_arc1))
  		if y1 < point_center_arc2[1]:
  			angle_point[0][1] = 360 - degrees(acos(alfa1_arc2))
  		else:
  			angle_point[0][1] = degrees(acos(alfa1_arc2))
  		if y2 < point_center_arc1[1]:
  			angle_point[1][0] = 360 - degrees(acos(alfa2_arc1))
  		else:
  			angle_point[1][0] = degrees(acos(alfa2_arc1))
  		if y2 < point_center_arc2[1]:
  			angle_point[1][1] = 360 - degrees(acos(alfa2_arc2))
  		else:
  			angle_point[1][1] = degrees(acos(alfa2_arc2))

  		if angle_point[0][0] >= angle1_arc1 and angle_point[0][0] <= angle2_arc1 and angle_point[0][1] >= angle1_arc2 and angle_point[0][1] <= angle2_arc2:
  			result["points"].append({"x": x1, "y": y1})
  		else:
  			result["points"].append({"x": -10000, "y": -10000})
  		if angle_point[1][0] >= angle1_arc1 and angle_point[1][0] <= angle2_arc1 and angle_point[1][1] >= angle1_arc2 and angle_point[1][1] <= angle2_arc2:
  			result["points"].append({"x": x2, "y": y2})
  		else:
  			result["points"].append({"x": -10000, "y": -10000})

  return result


def arc_to_axis(arc1, axis):
  '''
    Пересечение дуги и оси
  '''
  pass