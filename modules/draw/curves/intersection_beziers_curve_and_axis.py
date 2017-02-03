import bpy

from functools import reduce
from math import tan, radians

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points 
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.curves import is_one_of_bezier_curve
from fashion_project.modules.utils.intersections import line_to_curve
from fashion_project.modules.draw.curves.bezier_curve import BezierCurve


class IntersectionBeziersCurveAndAxis(Base):
  FP_TYPE = 'fp.draw.points.intersection_beziers_curve_and_axis'
  DEFAULT_LOCATION = (0.0, 0.0, 0.0)
  BASE_NAME = 'ТочкаПересеченияКривойИОси'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0.5, 0, 0.9)
  ANGLE = 0.0
  
  def poll(self, context):
    '''
    Требует выделеннeую кривую Безье и ось.
    '''
    return (
      len(context.selected_objects) == 2
      and
      (
        (context.selected_objects[0].fp_type == BezierCurve.FP_TYPE and context.selected_objects[1].fp_type == Point.FP_TYPE)
        or
        (context.selected_objects[1].fp_type == BezierCurve.FP_TYPE and context.selected_objects[0].fp_type == Point.FP_TYPE)
      ) 
    )


  def create(self, context):
    dep_id = tuple([
                     d.fp_id for d in context.selected_objects
                     ] + [0])
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.fp_deps = dep_id

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    mat = bpy.data.materials.new('ЗаливкаТочкиПересеченияКривойИОси')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    obj.location = self.DEFAULT_LOCATION
    obj.fp_angle = self.ANGLE


  def update(self, obj):
    coef_k = tan(radians(obj.fp_angle))
    deps_object = [objects for objects in bpy.data.objects if obj.fp_deps[0] == objects.fp_id or obj.fp_deps[1] == objects.fp_id]
    if deps_object[0].fp_type == BezierCurve.FP_TYPE:
      locations_curve = [
        get_point_abs_location(item) for item in bpy.data.objects
        if item.fp_id > 0 and item.fp_id in deps_object[0].fp_deps
      ]
      handle_left = [deps_object[0].data.splines[0].bezier_points[0].handle_right[0] - deps_object[0].data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],deps_object[0].data.splines[0].bezier_points[0].handle_right[1] - deps_object[0].data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
      handle_right = [deps_object[0].data.splines[0].bezier_points[1].handle_left[0] - deps_object[0].data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],deps_object[0].data.splines[0].bezier_points[1].handle_left[1] - deps_object[0].data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
      coef_b = -coef_k*get_point_abs_location(deps_object[1])[0] + get_point_abs_location(deps_object[1])[1]
      x_point = get_point_abs_location(deps_object[1])[0] * 10000
      y_point = coef_k*x_point + coef_b
      x_mouse = get_point_abs_location(deps_object[1])[0] * -10000
      y_mouse = coef_k*x_mouse + coef_b
    else:
      locations_curve = [
        get_point_abs_location(item) for item in bpy.data.objects
        if item.fp_id > 0 and item.fp_id in deps_object[1].fp_deps
      ]
      handle_left = [deps_object[1].data.splines[0].bezier_points[0].handle_right[0] - deps_object[1].data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],deps_object[1].data.splines[0].bezier_points[0].handle_right[1] - deps_object[1].data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
      handle_right = [deps_object[1].data.splines[0].bezier_points[1].handle_left[0] - deps_object[1].data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],deps_object[1].data.splines[0].bezier_points[1].handle_left[1] - deps_object[1].data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
      coef_b = -coef_k*get_point_abs_location(deps_object[0])[0] + get_point_abs_location(deps_object[0])[1]
      x_point = get_point_abs_location(deps_object[0])[0] * 10000  
      y_point = coef_k*x_point + coef_b
      x_mouse = get_point_abs_location(deps_object[0])[0] * -10000
      y_mouse = coef_k*x_mouse + coef_b

    coords_points = line_to_curve({"x": x_point, "y": y_point},{"x": x_mouse, "y": y_mouse}, {"x": locations_curve[0][0], "y": locations_curve[0][1]}, {"x": handle_left[0], "y": handle_left[1]}, {"x": handle_right[0], "y": handle_right[1]}, {"x": locations_curve[1][0], "y": locations_curve[1][1]})
    for coords_point in coords_points["points"]:
        vector_coords_point = (coords_point["x"], coords_point["y"], 0.0)
        if vector_coords_point[0] != -10000:
          obj.location = vector_coords_point
          break