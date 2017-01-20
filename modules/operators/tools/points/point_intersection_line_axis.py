import bpy

from math import pi, sqrt, degrees, atan
from functools import reduce

from fashion_project.modules.draw.points.point_intersection_line_axis import IntersectionLineAndAxis
from fashion_project.modules.utils import mouse, get_point_abs_location, fp_expression
from fashion_project.modules.operators.wires.proto import FP_WireProto
from fashion_project.modules.utils.intersections import line_to_line
from fashion_project.modules.draw.lines.line import Line

TARGET_LOCATION = (0.0, 0.0, 0.0)
OAAT_LOCK = False
ANGLE = 0.0


class FP_IntersectionLineAndAxis(bpy.types.Operator):
  '''
     Инструмент пересечение
     линии и оси
     Требует выделенную линию и точку
  '''

  bl_idname = "fp.intersection_line_and_axis"
  bl_label = "FP_IntersectionLineAndAxis"

  @classmethod
  def poll(cls, context):
    return (not OAAT_LOCK) and IntersectionLineAndAxis().poll(context)

  def execute(self, context):
    IntersectionLineAndAxis().create(context)
    return {'FINISHED'}


class FP_IntersectionLineAndAxisWire(bpy.types.Operator, FP_WireProto):
  '''
  Оператор рисования направляющей между двумя точками.
  '''
  bl_idname = 'fp.draw_point_intersection_line_and_axis'
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
    self.color3f = (0.3, 0.8, 0.1)
    self.point_poly = 4
    self.point_radius = 7
    self.point_angle_ammend = pi/4


  def on_before_modal(self):
    global OAAT_LOCK
    OAAT_LOCK = True


  def on_before_finish(self):
    global OAAT_LOCK
    IntersectionLineAndAxis.DEFAULT_LOCATION = TARGET_LOCATION
    IntersectionLineAndAxis.ANGLE = ANGLE
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
      if first_object.fp_type == Line.FP_TYPE:
        collection_of_line1_points = ([d for d in bpy.data.objects if (d.fp_id == first_object.fp_deps[0] or d.fp_id == first_object.fp_deps[1]) and d.fp_id > 0])
        locations1 = [get_point_abs_location(point) for point in collection_of_line1_points]
        locations = get_point_abs_location(second_object[0])
      else:
        collection_of_line1_points = ([d for d in bpy.data.objects if (d.fp_id == second_object[0].fp_deps[0] or d.fp_id == second_object[0].fp_deps[1]) and d.fp_id > 0])
        locations1 = [get_point_abs_location(point) for point in collection_of_line1_points]
        locations = get_point_abs_location(first_object)

      coef_k = (mouse_coords_3[1] - locations[1]) / (mouse_coords_3[0] - locations[0])
      if locations[0] < mouse_coords_3[0]:
        ANGLE = 180 + degrees(atan(coef_k))
      else:
        ANGLE = degrees(atan(coef_k))

      line_length = sqrt((locations[0] - mouse_coords_3[0]) ** 2 + (locations[1] - mouse_coords_3[1]) ** 2)
      proportion = 10000 / line_length
      def_loc_point = [locations[i] - mouse_coords_3[i] for i in range(3)]
      def_loc_mouse = [mouse_coords_3[i] - locations[i] for i in range(3)]

      location = [[0, 0], [0, 0]]
      location[0][0] = def_loc_point[0] * proportion + mouse_coords_3[0]
      location[0][1] = def_loc_point[1] * proportion + mouse_coords_3[1]
      location[1][0] = def_loc_mouse[0] * proportion + mouse_coords_3[0]
      location[1][1] = def_loc_mouse[1] * proportion + mouse_coords_3[1]

      self.draw_line(context, ((location[0][0], location[0][1], 0.0), (location[1][0], location[1][1], 0.0)))

      coords_points = line_to_line({ "x": locations1[0][0], "y": locations1[0][1] },{ "x": locations1[1][0], "y": locations1[1][1] },{ "x": locations[0], "y": locations[1] },{ "x": mouse_coords_3[0], "y": mouse_coords_3[1] })
      vector_coords_point = (coords_points["points"][0]["x"], coords_points["points"][0]["y"], 0.0)
      self.draw_point(context, (vector_coords_point,))
      TARGET_LOCATION = vector_coords_point


class FP_IntersectionLineAndAxisW(bpy.types.Macro):
  '''
  Позволяет построить точку на
  пересечении линии и 
  оси

  Требует выбранной точки и линии
  '''
  bl_idname = "fp_intersection_line_and_axis_wire"
  bl_label = "Wired point intersection"

def define_macros():
  FP_IntersectionLineAndAxisW.define('FP_OT_draw_point_intersection_line_and_axis')
  FP_IntersectionLineAndAxisW.define('FP_OT_intersection_line_and_axis')


clss = [
  FP_IntersectionLineAndAxisWire,
  FP_IntersectionLineAndAxis,
  FP_IntersectionLineAndAxisW,
]

def register():
  for cls in clss:
    bpy.utils.register_class(cls)
  define_macros()

def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)
