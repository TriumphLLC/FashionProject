import bpy

from math import pi, sqrt
from functools import reduce

from fashion_project.modules.draw.points.point_on_line import PointOnLine
from fashion_project.modules.utils import mouse, get_point_abs_location, fp_expression
from fashion_project.modules.operators.wires.proto import FP_WireProto


TARGET_LOCATION = (0.0,0.0,0.0)

''' One at a Time Lock '''
OAAT_LOCK = False


class FP_PointOnLine(bpy.types.Operator):
  '''
  Инструмент точка на линии:
  создает новую точку на линии между двумя точками.

  Требует двух выделенных точек.
  '''
  bl_idname = "fp.point_on_line"
  bl_label = "FP_PointOnLine"

  @classmethod
  def poll(cls, context):
    return (not OAAT_LOCK) and PointOnLine().poll(context)

  def execute(self, context):
    PointOnLine().create(context)
    return {'FINISHED'}
    

class FP_BetweenPointsWire(bpy.types.Operator, FP_WireProto):
  '''
  Оператор рисования направляющей между двумя точками.
  '''
  bl_idname = 'fp.draw_wire_between_points'
  bl_label = 'Draw wire between two point to mark new point location'
  
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
    parent_location = get_point_abs_location(bpy.context.active_object)
    rel_loc = fp_expression.location_to_expression([TARGET_LOCATION[i] - parent_location[i] for i,_c in enumerate(TARGET_LOCATION)])
    PointOnLine.DEFAULT_EXPRESSION = rel_loc
    OAAT_LOCK = False
    
  def draw_callback(self, context):
    global TARGET_LOCATION
    mouse_coords_2 = mouse.get_rel_coords_region_2d()
    mouse_coords_3 = mouse.get_coords_location_3d()
    if (
          (not mouse_coords_3) 
          or 
          (not mouse_coords_3[2] == 0.0)
      ): 
      return
    if (mouse.is_window_event() or True):
      first = get_point_abs_location(context.active_object)
      second = self._get_second_location(context, mouse_coords_3, first)
      self.draw_line(context, (first, second))
      self.draw_point(context, (second,))
      TARGET_LOCATION = second
      
  def _get_second_location(self, context, mouse_coords_3, loc1):
    loc2 = [
      get_point_abs_location(obj)
      for obj in context.selected_objects
      if obj.fp_id != context.active_object.fp_id
    ][0]
    loc3 = mouse_coords_3
    diff_a = [loc1[i] - loc2[i] for i in range(3)]
    a = sqrt(diff_a[0]**2 + diff_a[1]**2)
    diff_b = [loc1[i] - loc3[i] for i in range(3)]
    b = sqrt(diff_b[0]**2 + diff_b[1]**2)
    diff_c = [loc3[i] - loc2[i] for i in range(3)]
    c = sqrt(diff_c[0]**2 + diff_c[1]**2)
    p = (a+b+c)/2
    s = sqrt(p*(p-a)*(p-b)*(p-c))
    h = 2*s/a
    cos_b = h/b
    sin_b = sqrt(1 - cos_b**2)
    a1 = b * sin_b
    a2 = a - a1
    k = a2/a
    if (k < 0 or k > 1):
      k = 0
    if self._mouse_not_in_square(mouse_coords_3, (loc1, loc2)):
      k = 1
    loc = [coord*k + loc2[i] for i,coord in enumerate(diff_a)]
    return loc
    
  def _mouse_not_in_square(self, mouse_coords_3, locs):
    max_x = reduce(lambda r, i: i if i > r else r, [loc[0] for loc in locs])
    max_y = reduce(lambda r, i: i if i > r else r, [loc[1] for loc in locs])
    min_x = reduce(lambda r, i: i if i < r else r, [loc[0] for loc in locs])
    min_y = reduce(lambda r, i: i if i < r else r, [loc[1] for loc in locs])
    return (
      (mouse_coords_3[0] > max_x and mouse_coords_3[1] > max_y)
      or
      (mouse_coords_3[0] < min_x and mouse_coords_3[1] < min_y)
    )


class FP_PointOnLineW(bpy.types.Macro):
  '''
  Позволяет построить точку 
  на линии

  Требует двух выбранных точек
  '''
  bl_idname = "fp_point_on_line_wire"
  bl_label = "Wired point on line"


def define_macros():
  FP_PointOnLineW.define('FP_OT_draw_wire_between_points')
  FP_PointOnLineW.define('FP_OT_point_on_line')
  

clss = [
  FP_BetweenPointsWire,
  FP_PointOnLine,
  FP_PointOnLineW,
]
  
def register():
  for cls in clss:
    bpy.utils.register_class(cls)
  define_macros()

def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)
