import bpy

from functools import reduce

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.detail import PointsForCreateDetail
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.lines import is_one_of_lines, get_contours, get_line_ends
from fashion_project.modules.draw.arcs import get_arc_ends_coords, is_one_of_arc
from fashion_project.modules.draw.curves import is_one_of_bezier_curve, get_curve_ends
from fashion_project.modules.utils import get_point_abs_location, mouse, fp_expression
from mathutils import Vector

from xpattern.modules import obj_utils
from xpattern.modules import helpers

import math
import copy


class ToolDetail(Base):
	FP_TYPE = 'fp.draw.detail.tool_detail'
	CURVE_DIMS = '3D'
	CURVE_BEVEL_DEPTH = 0.01
	CURVE_FILL_MODE = 'FULL'
	STROKE_COLOR = (0.2, 0.7, 0.7)
	GUIDE_COLOR = (0.9, 0.1, 0.1)
	HANDLE_COLOR = (0.8, 0.0, 0.0)
	HANDLE_RADIUS = 0.05
	POINTS = []
	USEDPOINTS=[]
	def poll(self, context):
		'''
		Требует более двух выделенных элементов
		замкнутых в контур.
		'''
		return (
			len(context.selected_objects) >= 2
		)

	def create(self, context):
		locations = [];
		f_ids = [];
		self.create_countur(context.selected_objects)

		deps = []

		curve = bpy.data.curves.new(name="Деталь", type='CURVE')
		curve.dimensions = '3D'
		curve.resolution_u = 2
		curve.dimensions = self.CURVE_DIMS
		curve.bevel_depth = self.CURVE_BEVEL_DEPTH
		curve.bevel_resolution = 12
		curve.fill_mode = self.CURVE_FILL_MODE
		curve_mat = bpy.data.materials.new('ОбводкаДетали')
		curve_mat.diffuse_color = self.STROKE_COLOR
		curve.materials.append(curve_mat)

		bpyObj = bpy.data.objects.new("Деталь", curve)
		# new_scene = bpy.data.scenes.new(bpyObj.name)
		Counter.register(bpyObj, self.FP_TYPE)
		bpyObj.location = (0,0,0)
		bpyObj.show_name = True
		# new_scene.objects.link(bpyObj)
		context.scene.objects.link(bpyObj)
		spline = bpyObj.data.splines.new('BEZIER')
		spline.use_cyclic_u = True
		points = spline.bezier_points
		points.add(len(self.POINTS) - 1)

		for index,point in enumerate(points):
			point.co = self.POINTS[index].pos
			point.handle_left = self.POINTS[index].hl
			point.handle_right = self.POINTS[index].hr

		bpyObj.layers[1] = True
		bpyObj.layers[0] = False
		curve.fill_mode = 'BACK'
		curve.dimensions = '2D'

		deps = [e for e in self.USEDPOINTS if e not in deps and not deps.append(e)]
		for i in range(30-len(deps)):
			deps.append(0)

		bpyObj.fp_deps30 = deps

		# integration to the XPettern plugin
		points = [x.pos for x in self.POINTS]
		bpy_obj = obj_utils.create_object()
		location = Vector((0, 0, 0))
		for point in points:
			location = location + point
		bpy_obj.location = location / len(points)
		curve = helpers.Curve.fromPoints(points)
		helpers.Wrapper(curve).toBpy(bpy_obj)

		# reset points
		self.POINTS = []
		self.USEDPOINTS = []


	def create_countur(self,objects):
		lines  = [ob for ob in objects if is_one_of_lines(ob)]
		# points = [ob for ob in objects if is_one_of_points(ob)]
		arcs   = [ob for ob in objects if is_one_of_arc(ob)]
		curves = [ob for ob in objects if is_one_of_bezier_curve(ob)]

		objs = [ob for ob in objects if not is_one_of_points(ob)]

		for o in objects:
				self.find_ob_ends(o)

		ob = objs[0]
		for o in range(0,len(objs)-1):
			self.coords_for_bezier(ob)
			self.USEDPOINTS.append(ob.fp_id)
			point1 = ob.end1
			point2 = ob.end2
			ob = self.find_line_for_point(ob,objects,ob.end2)
			if(o == len(objects)-2):
				self.coords_for_bezier(ob)
			if (Vector(ob.end1)==Vector(point2)):
				point1 = Vector(ob.end1)
				point2 = Vector(ob.end2)
				if(is_one_of_arc(ob)):
					ob.order = 0
			else:
				point1 = Vector(ob.end2)
				point2 = Vector(ob.end1)
				if(is_one_of_arc(ob)):
					ob.order = 1

			ob.end1=Vector(point1)
			ob.end2=Vector(point2)


	def find_element_in_list(self,element, list_element):
		try:
			index_element = list_element.index(element)
			return index_element
		except ValueError:
			return None

	def find_line_for_point(self,ob,objects,point):
			for o in objects:
				if(o.fp_id != ob.fp_id):
					if(self.find_element_in_list(o.fp_id, self.USEDPOINTS) == None):
						if((Vector((round(o.end1[0],4),round(o.end1[1],4),0.0)) == Vector((round(point[0],4),round(point[1],4),0.0))) or (Vector((round(o.end2[0],4),round(o.end2[1],4),0.0)) == Vector((round(point[0],4),round(point[1],4),0.0)))):
							self.USEDPOINTS.append(o.fp_id)
							return o
						else:
							continue
			return point


	def find_ob_ends(self,obj):
			if(is_one_of_arc(obj)):
				coordsmas = get_arc_ends_coords(obj)
				obj.end1 = Vector(coordsmas[0])
				obj.end2 = Vector(coordsmas[1])
			elif(is_one_of_lines(obj)):
				coords = get_line_ends(obj)
				x = coords[0]
				y = coords[1]
				obj.end1 = Vector(x)
				obj.end2 = Vector(y)
			elif(is_one_of_bezier_curve(obj)):
				coords = get_curve_ends(obj)
				x = coords[0]
				y = coords[1]
				obj.end1 = Vector(x)
				obj.end2 = Vector(y)


	def coords_for_bezier(self,obj):
		if(is_one_of_arc(obj)):
			coords1 = obj.end1
			coords2 = obj.end2
			pointX = self.check_points(coords1, obj.fp_id)
			pointY = self.check_points(coords2, obj.fp_id)
			pointX.fp_angles = obj.fp_angles
			pointY.fp_angles = obj.fp_angles
			self.make_line_new_type(obj, pointX,pointY,"arc")
		elif(is_one_of_lines(obj)):
			x = obj.end1
			y = obj.end2
			nx = self.check_points(x, obj.fp_id)
			ny = self.check_points(y, obj.fp_id)
			self.make_line_new_type(obj, nx,ny,"line")
		elif(is_one_of_bezier_curve(obj)):
			x = obj.end1
			y = obj.end2
			nx = self.check_points(x, obj.fp_id)
			ny = self.check_points(y, obj.fp_id)
			self.make_line_new_type(obj, nx,ny,"curve")
		else:
			pass

	def check_points(self,coord, obj_id):
			check_points_mas = set()
			for p in self.POINTS:
				check_points_mas.add((tuple(p.pos)[0],tuple(p.pos)[1],tuple(p.pos)[2]))

			if(len(self.POINTS) == 0):
				new_point = PointsForCreateDetail(pos = coord, fp_id = obj_id)
				self.POINTS.append(new_point)
				return new_point
			else:
				for p in self.POINTS:
					if(round(tuple(p.pos)[0],6) == round(coord[0],6) and round(tuple(p.pos)[1],6) == round(coord[1],6)):
						return p
				new_point = PointsForCreateDetail(pos = coord, fp_id = obj_id)
				self.POINTS.append(new_point)
				return new_point


	def make_line_new_type(self, obj, point1, point2,type):
		x = point1.pos
		y = point2.pos
		x1 = x[0]
		y1 = x[1]
		x2 = y[0]
		y2 = y[1]
		if(type == 'line'):
			if(point1.hr != point1.pos):
				point1.hl = self._lerp(x,y, 2 / 3)
				point2.hr = self._lerp(x,y, 1 / 3)
			else:
				point2.hl = self._lerp(x,y, 2 / 3)
				point1.hr = self._lerp(x,y, 1 / 3)
		elif(type == 'arc'):
			if(point1.hr != point1.pos):
				point1.hl = Vector((1*math.cos(math.radians(90.0+point1.fp_angles[0]))+x1, 1 * math.sin(math.radians(90.0+point1.fp_angles[0])) + y1, 0))
				point2.hr = Vector((1*math.cos(math.radians(-90.0+point2.fp_angles[1]))+x2, 1 * math.sin(math.radians(-90.0+point2.fp_angles[1])) + y2, 0))
			else:
				point1.hr = Vector((1*math.cos(math.radians(90.0+point1.fp_angles[0]))+x1, 1 * math.sin(math.radians(90.0+point1.fp_angles[0])) + y1, 0))
				point2.hl = Vector((1*math.cos(math.radians(-90.0+point2.fp_angles[1]))+x2, 1 * math.sin(math.radians(-90.0+point2.fp_angles[1])) + y2, 0))
		if(type == 'curve'):
			if(point1.hr != point1.pos):
				point1.hl = obj.data.splines[0].bezier_points[0].handle_right + obj.location
				point2.hr = obj.data.splines[0].bezier_points[1].handle_left + obj.location
			else:
				point1.hr = obj.data.splines[0].bezier_points[0].handle_right + obj.location
				point2.hl = obj.data.splines[0].bezier_points[1].handle_left + obj.location


	def _lerp(self,p1, p2, t):
		return (1 - t) * Vector(p1) + t * Vector(p2)


	def update(self, obj, context):
		self.POINTS = []
		self.USEDPOINTS = []
		for ob in bpy.data.objects:
			for i in range(30):
				if ob.fp_id > 0 and obj.fp_deps30[i] == ob.fp_id:
					ob.select = True

		self.create_countur(context.selected_objects)
		for ob in bpy.data.objects:
			if context.active_object != ob:
				ob.select = False

		spline = obj.data.splines[0]
		points = spline.bezier_points
		for index,point in enumerate(points):
			point.co = self.POINTS[index].pos
			point.handle_left = self.POINTS[index].hl
			point.handle_right = self.POINTS[index].hr

		# bpy.data.objects[name_obj].select = True



			# deps = []
			# locations = []
			# for x in obj.fp_deps_c:
			# 		deps.append(int(x.value))

			# for d in deps:
			# 	for item in bpy.data.objects:
			# 		if(item.fp_id == d):
			# 				locations.append(Vector(get_point_abs_location(item)))

			# locations.append(locations[0])


			# pass
