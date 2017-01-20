import bpy

from math import sqrt, asin, sin, cos, atan, pi
from functools import reduce

from fashion_project.modules.draw.lines import is_one_of_lines, get_line_length, selection_is_contour
from fashion_project.modules.draw.lines.line_for_dart import LineForDart
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.points import get_absolute_angle, get_angle, is_one_of_points
from fashion_project.modules.utils import get_point_abs_location, mouse, fp_expression
from fashion_project.modules.utils.mathlib import get_distance


from fashion_project.modules.draw.points.point_on_line import PointOnLine
from fashion_project.modules.operators.wires.proto import FP_WireProto


TARGET_LOCATION = (0.0,0.0,0.0)
DIF = 0
FLAG = True
IMAX = 0
IMIN = 0

_ANGLE = 1

''' One at a Time Lock '''
OAAT_LOCK = False


class FP_Modeling(bpy.types.Operator):
  '''
  Инструмент моделирование

  Требует выделенный контур.
  '''

  bl_idname = "fp.modeling"
  bl_label = "FP Modeling"
  
  @classmethod
  def poll(cls, context):
    return (not OAAT_LOCK)
    
  def execute(self, context):

    return {'FINISHED'}


class FP_UpdateContour(bpy.types.Operator, FP_WireProto):
  '''
  
  '''
  bl_idname = 'fp.draw_update_contour'
  bl_label = 'Draw update contour'

  @classmethod
  def poll(cls, context):
    contour = False
    line_for_dart = []
    for obj in context.selected_objects:
      if obj.fp_type == LineForDart.FP_TYPE:
        line_for_dart += [obj]


    if len(line_for_dart) < 2:
      contour = False
    else:
      if line_for_dart[0].fp_deps[0] == line_for_dart[1].fp_deps[0]:
        point_id = line_for_dart[0].fp_deps[0]
        contour = True
      elif line_for_dart[0].fp_deps[1] == line_for_dart[1].fp_deps[0]:
        point_id = line_for_dart[0].fp_deps[1]
        contour = True
      elif line_for_dart[0].fp_deps[0] == line_for_dart[1].fp_deps[1]:
        point_id = line_for_dart[0].fp_deps[0]
        contour = True
      elif line_for_dart[0].fp_deps[1] == line_for_dart[1].fp_deps[1]:
        point_id = line_for_dart[0].fp_deps[1]
        contour = True
      else:
        contour = False
      if contour:
        for i in range(len(line_for_dart)-2):
          if line_for_dart[i+2].fp_deps[0] == point_id or line_for_dart[i+2].fp_deps[1] == point_id:
            contour = True
          else:
            contour = False
            break
    return (
      contour
      and selection_is_contour()
    )
    
  def on_before_modal(self):
    global OAAT_LOCK
    self.TARGET_LOCATION = mouse.get_coords_location_3d()
    OAAT_LOCK = True
    
  def on_before_finish(self):
    global OAAT_LOCK, FLAG
    FLAG = True
    OAAT_LOCK = False
    
  def draw_callback(self, context):
    global TARGET_LOCATION, _ANGLE, FLAG, IMAX, IMIN
    mouse_coords_3 = mouse.get_coords_location_3d()
    if FLAG:
        TARGET_LOCATION = mouse_coords_3;
    self.DIF = mouse_coords_3[0] - TARGET_LOCATION[0]
    if mouse.get_event()[4] == 'TAB' and FLAG:
        TARGET_LOCATION = mouse_coords_3
        FLAG = False
    TARGET_LOCATION = mouse_coords_3

    _ANGLE = self.DIF * 5

    dart_line = [line for line in context.selected_objects if line.fp_type == LineForDart.FP_TYPE]

    if dart_line[0].fp_deps[0] == dart_line[1].fp_deps[0]:
      for obj in bpy.data.objects:
        if obj.fp_id == dart_line[0].fp_deps[0]:
          center = obj
          break
    elif dart_line[0].fp_deps[0] == dart_line[1].fp_deps[1]:
      for obj in bpy.data.objects:
        if obj.fp_id == dart_line[0].fp_deps[0]:
          center = obj
          break
    else:
      for obj in bpy.data.objects:
        if obj.fp_id == dart_line[0].fp_deps[1]:
          center = obj
          break

    points_on_dart_line = []
    for line in dart_line:
      tmp_pts = [center]
      for obj in bpy.data.objects:
        if (obj.fp_id == line.fp_deps[0] or obj.fp_id == line.fp_deps[1]) and obj != center:
          tmp_pts += [obj]
      points_on_dart_line += [tmp_pts]
    
    angle_dart_line = []
    for points in points_on_dart_line:
      angle_dart_line += [get_absolute_angle(get_point_abs_location(points[0]), get_point_abs_location(points[1]))]

    all_limit_lines = []
    for line in bpy.data.objects:
      if (line.fp_deps[0] == center.fp_id or line.fp_deps[1] == center.fp_id) and line != dart_line[0] and line != dart_line[1]:
        all_limit_lines += [line]

    all_point_on_limit_lines = []
    for line in all_limit_lines:
      tmp_pts = [center]
      for obj in bpy.data.objects:
        if (obj.fp_id == line.fp_deps[0] or obj.fp_id == line.fp_deps[1]) and obj != center:
          tmp_pts += [obj]
      all_point_on_limit_lines += [tmp_pts]
    angle_limit_line = []
    for points in all_point_on_limit_lines:
      angle_limit_line += [get_absolute_angle(get_point_abs_location(points[0]), get_point_abs_location(points[1]))]


    angle_limit = []
    limit_lines = []
    tmp_min = 10000
    tmp_max = -10000
    if angle_dart_line[0] < angle_dart_line[1]:
      for angle in angle_limit_line:
        if angle > tmp_max and angle <= angle_dart_line[0]:
          tmp_max = angle
      if tmp_max == -10000:
        angle_limit += [min(angle_limit_line)]
      else:
        angle_limit += [tmp_max]
      for angle in angle_limit_line:
        if angle < tmp_min and angle >= angle_dart_line[1]:
          tmp_min = angle 
      if tmp_min == 10000:
        angle_limit += [max(angle_limit_line)]
      else:
        angle_limit += [tmp_min]
    else:
      for angle in angle_limit_line:
        if angle < tmp_min and angle >= angle_dart_line[0]:
          tmp_min = angle
      if tmp_min == 10000:
        angle_limit += [max(angle_limit_line)]
      else:
        angle_limit += [tmp_min]
      for angle in angle_limit_line:
        if angle > tmp_max and angle <= angle_dart_line[1]:
          tmp_max = angle 
      if tmp_max == -10000:
        angle_limit += [min(angle_limit_line)]
      else:
        angle_limit += [tmp_max]
    for angle in angle_limit:
      for i in range(len(all_limit_lines)):
        if angle_limit_line[i] == angle:
          limit_lines += [all_limit_lines[i]]
          break


    dif_angle = [round(angle_dart_line[i]-angle_limit[i], 1) for i in range(len(angle_limit))]
    if FLAG:
        if dif_angle[0] > 0:
            IMAX = 0
            IMIN = 1
        else:
            IMAX = 1
            IMIN = 0
    for i in range(len(dif_angle)):
        if i == IMAX:
            print("_ANGLE", _ANGLE)
            if _ANGLE < 0 and dif_angle[i] < 0.9:
                _ANGLE = 0
        if i == IMIN:
            print("_ANGLE", _ANGLE)
            if _ANGLE > 0 and dif_angle[i] > -0.9:
                _ANGLE = 0


    points_deps_for_update = []
    points_parent_for_update = []    
    point_start_for_update = []
    all_points_of_select = []    
    for obj in context.selected_objects:
      count = 0
      for point in bpy.data.objects:
        if (obj.fp_deps[0] == point.fp_id or obj.fp_deps[1] == point.fp_id) and is_one_of_points(point) and all(point != p for p in all_points_of_select):
          all_points_of_select += [point]
          count += 1
        if count == 2:
          break
    for point in all_points_of_select:
      if point.fp_id == 1:
        point_start_for_update += [point]
        continue
      for obj in bpy.data.objects:
        if obj.parent == point and all(obj != p for p in all_points_of_select):
          points_deps_for_update += [obj]
        if point.parent == obj and all(obj != p for p in all_points_of_select) and point != center:
          points_parent_for_update += [point]

    if len(points_deps_for_update) > 0:
      old_location = []
      for point in points_deps_for_update:
        old_location += [get_point_abs_location(point)]

    if len(point_start_for_update) > 0:
      R = round(get_distance(get_point_abs_location(point_start_for_update[0]), get_point_abs_location(center)), 3)
      angle = round(get_absolute_angle(get_point_abs_location(center), get_point_abs_location(point_start_for_update[0])), 1)
      location_center = get_point_abs_location(center)
      angle += _ANGLE
      new_location = []
      new_location += [location_center[0] + R*cos(angle*pi/180)]
      new_location += [location_center[1] + R*sin(angle*pi/180)]
      distance = round(get_distance([0,0], new_location), 3)
      new_angle = round(get_angle([0,0], new_location), 1)


      point_start_for_update[0].fp_expression = str(distance)
      point_start_for_update[0].fp_angle = new_angle

      if center.parent == point_start_for_update[0]:
        center.fp_angle += _ANGLE
    elif len(points_parent_for_update) > 0:
      R = round(get_distance(get_point_abs_location(points_parent_for_update[0]), get_point_abs_location(center)), 3)
      angle = round(get_absolute_angle(get_point_abs_location(center), get_point_abs_location(points_parent_for_update[0])), 1)
      location_center = get_point_abs_location(center)
      angle += _ANGLE
      new_location = []
      new_location += [location_center[0] + R*cos(angle*pi/180)]
      new_location += [location_center[1] + R*sin(angle*pi/180)]
      distance = round(get_distance(get_point_abs_location(points_parent_for_update[0].parent), new_location), 3)
      new_angle = round(get_angle(get_point_abs_location(points_parent_for_update[0].parent), new_location), 1)

      points_parent_for_update[0].fp_expression = str(distance)
      points_parent_for_update[0].fp_angle = new_angle

      if center.parent == points_parent_for_update[0]:
        center.fp_angle += _ANGLE

    for point in all_points_of_select:
      if point != center and all(point != obj for obj in point_start_for_update) and all(point != obj for obj in points_parent_for_update) and all(point != obj for obj in points_deps_for_update):
        point.fp_angle += _ANGLE

    if len(points_deps_for_update) > 0:
      new_location_parent = []
      for point in points_deps_for_update:
        new_location_parent += [get_point_abs_location(point.parent)]
      for i in range(len(points_deps_for_update)):
        distance = round(get_distance(new_location_parent[i], old_location[i]), 3)
        new_angle = round(get_angle(new_location_parent[i], old_location[i]), 1)
        points_deps_for_update[i].fp_expression = str(distance)
        points_deps_for_update[i].fp_angle = new_angle


class FP_ModalModeling(bpy.types.Macro):
  bl_idname = "fp_modal_modeling"
  bl_label = "Modal Modeling"


def define_macros():
  FP_ModalModeling.define('FP_OT_draw_update_contour')
  FP_ModalModeling.define('FP_OT_modeling')


clss = [
  FP_UpdateContour,
  FP_Modeling,
  FP_ModalModeling
]


def register():
  for cls in clss:
    bpy.utils.register_class(cls)
  define_macros()

def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)