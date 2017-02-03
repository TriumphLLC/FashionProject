import bpy

from math import pi, sqrt, degrees, atan
from functools import reduce

from fashion_project.modules.draw.curves.intersection_beziers_curve_and_axis import IntersectionBeziersCurveAndAxis
from fashion_project.modules.utils import mouse, get_point_abs_location, fp_expression
from fashion_project.modules.operators.wires.proto import FP_WireProto
from fashion_project.modules.utils.intersections import line_to_curve
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.curves.bezier_curve import BezierCurve


TARGET_LOCATION = (0.0,0.0,0.0)
ANGLE = 0.0

''' One at a Time Lock '''
OAAT_LOCK = False


class FP_IntersectionBeziersCurveAndAxis(bpy.types.Operator):
  '''
  Инструмент пересечение 
  кривой Безье и оси

  Требует выделенную кривую Безье и ось.
  '''
  bl_idname = "fp.intersection_beziers_curve_and_axis"
  bl_label = "FP_IntersectionBeziersCurveAndAxis"

  @classmethod
  def poll(cls, context):
    return (not OAAT_LOCK) and IntersectionBeziersCurveAndAxis().poll(context)

  def execute(self, context):
    IntersectionBeziersCurveAndAxis().create(context)
    return {'FINISHED'}


class FP_PointIntersectionCurveAndAxisWire(bpy.types.Operator, FP_WireProto):
  '''
  Оператор рисования направляющей между двумя точками.
  '''
  bl_idname = 'fp.draw_point_intersection_curve_and_axis'
  bl_label = 'Draw point'

  
  @classmethod
  def poll(cls, context):
    return (
      context.area.type == 'VIEW_3D'
      and
      context.active_object
      and
      len([
        oth for oth in context.selected_objects
        if oth.fp_id > 0 and oth.fp_id != context.active_object.fp_id
      ]) == 1
    )


  def __init__(self):
    self.color3f = (0.3,0.8,0.1)
    self.point_poly = 4
    self.point_radius = 7
    self.point_angle_ammend = pi/4


  def on_before_modal(self):
    global OAAT_LOCK
    OAAT_LOCK = True


  def on_before_finish(self):
    global OAAT_LOCK
    IntersectionBeziersCurveAndAxis.DEFAULT_LOCATION = TARGET_LOCATION
    IntersectionBeziersCurveAndAxis.ANGLE = ANGLE
    OAAT_LOCK = False

  def draw_callback(self, context):
    global TARGET_LOCATION
    global ANGLE
    mouse_coords_3 = mouse.get_coords_location_3d()
    first_object = context.active_object
    second_object = [oth for oth in context.selected_objects if oth.fp_id > 0 and oth.fp_id != context.active_object.fp_id]
    if (
          (not mouse_coords_3) 
          or 
          (not mouse_coords_3[2] == 0.0)
      ): 
      return
    if (mouse.is_window_event() or True):
      if first_object.fp_type == BezierCurve.FP_TYPE:
        locations_curve = [
          get_point_abs_location(item) for item in bpy.data.objects
          if item.fp_id > 0 and item.fp_id in first_object.fp_deps
        ]
        handle_left = [first_object.data.splines[0].bezier_points[0].handle_right[0] - first_object.data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],first_object.data.splines[0].bezier_points[0].handle_right[1] - first_object.data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
        handle_right = [first_object.data.splines[0].bezier_points[1].handle_left[0] - first_object.data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],first_object.data.splines[0].bezier_points[1].handle_left[1] - first_object.data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
        locations = get_point_abs_location(second_object[0])
      else:
        locations_curve = [
          get_point_abs_location(item) for item in bpy.data.objects
          if item.fp_id > 0 and item.fp_id in second_object[0].fp_deps
        ]
        handle_left = [second_object[0].data.splines[0].bezier_points[0].handle_right[0] - second_object[0].data.splines[0].bezier_points[0].co[0] + locations_curve[0][0],second_object[0].data.splines[0].bezier_points[0].handle_right[1] - second_object[0].data.splines[0].bezier_points[0].co[1] + locations_curve[0][1],0.0]
        handle_right = [second_object[0].data.splines[0].bezier_points[1].handle_left[0] - second_object[0].data.splines[0].bezier_points[1].co[0] + locations_curve[1][0],second_object[0].data.splines[0].bezier_points[1].handle_left[1] - second_object[0].data.splines[0].bezier_points[1].co[1] + locations_curve[1][1],0.0]
        locations = get_point_abs_location(first_object)

      coef_k = (mouse_coords_3[1] - locations[1])/(mouse_coords_3[0] - locations[0])
      # COEF_B = -coef_k * locations[0] + locations[1]
      if locations[0] < mouse_coords_3[0]:
        ANGLE = 180 + degrees(atan(coef_k))
      else:
        ANGLE = degrees(atan(coef_k))

      line_length = sqrt((locations[0]-mouse_coords_3[0]) ** 2 + (locations[1]-mouse_coords_3[1]) ** 2)
      proportion = 10000/line_length
      def_loc_point = [locations[i] - mouse_coords_3[i] for i in range(3)]
      def_loc_mouse = [mouse_coords_3[i] - locations[i] for i in range(3)]

      location = [[0,0],[0,0]]
      location[0][0] = def_loc_point[0] * proportion + mouse_coords_3[0]
      location[0][1] = def_loc_point[1] * proportion + mouse_coords_3[1]
      location[1][0] = def_loc_mouse[0] * proportion + mouse_coords_3[0]
      location[1][1] = def_loc_mouse[1] * proportion + mouse_coords_3[1]

      self.draw_line(context, ((location[0][0], location[0][1], 0.0), (location[1][0], location[1][1], 0.0)))
      
      coords_points = line_to_curve({"x": location[0][0], "y": location[0][1]},{"x": location[1][0], "y": location[1][1]}, {"x": locations_curve[0][0], "y": locations_curve[0][1]}, {"x": handle_left[0], "y": handle_left[1]}, {"x": handle_right[0], "y": handle_right[1]}, {"x": locations_curve[1][0], "y": locations_curve[1][1]})
      for coords_point in coords_points["points"]:
        vector_coords_point = (coords_point["x"], coords_point["y"], 0.0)
        if vector_coords_point[0] != -10000:
          self.draw_point(context, (vector_coords_point,))

      TARGET_LOCATION = vector_coords_point


class FP_PointIntersectionCurveAndAxisW(bpy.types.Macro):
  '''
  Инструмент пересечение 
  кривой Безье и оси

  Требует выделенную кривую Безье 
  и точку.
  '''
  bl_idname = "fp_intersection_beziers_curve_and_axis_wire"
  bl_label = "Wired point intersection"

def define_macros():
  FP_PointIntersectionCurveAndAxisW.define('FP_OT_draw_point_intersection_curve_and_axis')
  FP_PointIntersectionCurveAndAxisW.define('FP_OT_intersection_beziers_curve_and_axis')


clss = [
  FP_PointIntersectionCurveAndAxisWire,
  FP_IntersectionBeziersCurveAndAxis,
  FP_PointIntersectionCurveAndAxisW,
]
  
def register():
  for cls in clss:
    bpy.utils.register_class(cls)
  define_macros()

def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)