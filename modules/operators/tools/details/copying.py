import bpy

from functools import reduce
from operator import sub, add

from math import sqrt, asin, sin, cos, atan, pi

from fashion_project.modules.draw.points import get_all_points
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.lines import is_one_of_lines, get_line_length, selection_is_contour
from fashion_project.modules.utils import get_point_abs_location as loc
from fashion_project.modules.utils.fp_expression import location_to_expression, expression_to_value
from fashion_project.modules.utils.mathlib import rad2deg, deg2rad, get_distance
from fashion_project.modules.draw.points import get_angle


MODELING_MONITOR = False
TARGET_MONITOR = False
MODELING_BUFFER = set()


def is_modeling():
  return MODELING_MONITOR or TARGET_MONITOR

def get_modeling_buffer():
  return MODELING_BUFFER[::]


class FP_Copying(bpy.types.Operator):
  bl_idname = "fp.copying"
  bl_label = "FP Copying"
  
  @classmethod
  def poll(cls, context):
    return not MODELING_MONITOR and not TARGET_MONITOR
    
  def execute(self, context):
    global  MODELING_MONITOR, MODELING_BUFFER
    MODELING_MONITOR = True
    MODELING_BUFFER = set()
    for item in bpy.data.objects:
      item.select = False
    context.window_manager.modal_handler_add(self)
    return {'RUNNING_MODAL'}
    
  def modal(self, context, event):
    if not MODELING_MONITOR:
      return {'FINISHED'}
    if len(MODELING_BUFFER) == 0 or context.active_object.fp_id not in MODELING_BUFFER:
      self._buffer_add_recur(context.active_object)
    for obj in [obj for obj in bpy.data.objects if obj.fp_id in MODELING_BUFFER]:
      obj.select = True
    return {'PASS_THROUGH'}
    
  def _buffer_add_recur(self, obj):
    MODELING_BUFFER.add(obj.fp_id)
    [
      self._buffer_add_recur(dep) 
      for dep in bpy.data.objects
      if dep.fp_id > 0 and (dep.fp_id in obj.fp_deps or obj.parent == dep)
    ]


class FP_CopyingStop(bpy.types.Operator):
  bl_idname = 'fp.copying_stop'
  bl_label = 'FP Copying Stop'
  
  @classmethod
  def poll(cls, context):
    return MODELING_MONITOR
    
  def execute(self, context):
    global MODELING_MONITOR
    MODELING_MONITOR = False
    return {'FINISHED'}
    
    
class FP_CopyingTarget(bpy.types.Operator):
  bl_idname = 'fp.copying_target'
  bl_label = 'FP Copying Target'
  
  _moving_line = None
  _target_line = None
  
  @classmethod
  def poll(cls, context):
    return (
      MODELING_MONITOR
      and
      is_one_of_lines(context.active_object)
    )
    
  def execute(self, context):
    global MODELING_MONITOR, TARGET_MONITOR
    MODELING_MONITOR = False
    TARGET_MONITOR = True
    context.window_manager.modal_handler_add(self)
    self._moving_line = context.active_object
    return {'RUNNING_MODAL'}
  
  def modal(self, context, event):
    global TARGET_MONITOR
    if (
      is_one_of_lines(context.active_object)
      and
      context.active_object.fp_id not in MODELING_BUFFER
      and
      get_line_length(self._moving_line) == get_line_length(context.active_object)
    ):
      self._target_line = context.active_object
      self._move()
      TARGET_MONITOR = False
      RESULTSET = {'FINISHED'}
    else:
      RESULTSET = {'PASS_THROUGH'}
    for obj in [obj for obj in bpy.data.objects if obj.fp_id in MODELING_BUFFER]:
      obj.select = True
    return RESULTSET
  
  def _move(self):
    ml = self._moving_line
    tl = self._target_line
    ml_ps = [obj for obj in bpy.data.objects if obj.fp_id in ml.fp_deps and obj.fp_id != 0]
    tl_ps = [obj for obj in bpy.data.objects if obj.fp_id in tl.fp_deps and obj.fp_id != 0]
    pairs = [(i,j) for i in ml_ps for j in tl_ps]
    nearest = reduce(lambda rslt, pair: pair if ((loc(pair[1])[0] - loc(pair[0])[0])**2 + (loc(pair[1])[1] - loc(pair[0])[1])**2) < ((loc(rslt[1])[0] - loc(rslt[0])[0])**2 + (loc(rslt[1])[1] - loc(rslt[0])[1])**2) else rslt, pairs)
    farest = reduce(lambda r, p: p if (nearest[0] not in p and nearest[1] not in p) else r, pairs)
    nearest[0].fp_expression = nearest[1].fp_expression 
    nearest[0].fp_angle = nearest[1].fp_angle
    fdiff = -sub(*[p.fp_angle for p in farest])
    self._rotate_recur(farest[0], fdiff)
    farest[0].fp_expression = farest[1].fp_expression
    [
      self._rotate_recur(obj, fdiff)
      for obj in bpy.data.objects
      if (nearest[0].fp_id in obj.fp_deps) or (obj.parent == nearest[0]) 
    ]
    
  def _rotate_recur(self, point, angle_diff_deg):
    point.fp_angle += angle_diff_deg
    [
      self._rotate_recur(obj, angle_diff_deg)
      for obj in bpy.data.objects
      if (point.fp_id in obj.fp_deps) or (obj.parent == point) 
    ]
    

class FP_CopyingContourTarget(bpy.types.Operator):
  bl_idname = "fp.copying_contour_target"
  bl_label = "FP Copying Contour Target"
  
  _moving_line = None
  _moving_contour = []
  _target_line = None
  
  _point = Point()
  _line = Line()
  
  @classmethod
  def poll(cls, context):
    return selection_is_contour()
  
  def execute(self, context):
    self._moving_contour = []
    self._moving_line = context.active_object
    # self._moving_contour = context.selected_objects[:]
    self._moving_contour.append(context.active_object)
    obj_in_contour = context.active_object
    for i in range(len(context.selected_objects)-1):
      for obj in context.selected_objects:
        object_in_contour = False
        if (obj_in_contour.fp_deps[0] == obj.fp_deps[1] or obj_in_contour.fp_deps[0] == obj.fp_deps[0] or obj_in_contour.fp_deps[1] == obj.fp_deps[0] or obj_in_contour.fp_deps[1] == obj.fp_deps[1]) and obj != obj_in_contour:
          for ob in self._moving_contour:
            if obj == ob:
              object_in_contour = True
              break
          if not object_in_contour:
            self._moving_contour.append(obj)
            obj_in_contour = obj
            break
    context.window_manager.modal_handler_add(self)
    return {'RUNNING_MODAL'}
    
  def modal(self, context, event):
    if (
      is_one_of_lines(context.active_object)
      and
      context.active_object not in self._moving_contour
      and
      get_line_length(self._moving_line) == get_line_length(context.active_object)
    ):
      self._target_line = context.active_object
      self._move(context)
      return {'FINISHED'}
    else:
      return {'PASS_THROUGH'}

  def dependencies_in_contour(self, points):
    dependencies = points
    depends = False
    for point in dependencies:
      if point.parent == None:
        continue
      for dependence in dependencies:
        if point.parent != dependence and point.parent != None:
          depends = True
        else:
          depends = False
          break
      if depends:
        dependencies.append(point.parent)
    return dependencies
      
  def _move(self, context):
    ml = self._moving_line
    tl = self._target_line
    ml_ps = [obj for obj in bpy.data.objects if obj.fp_id in ml.fp_deps and obj.fp_id != 0]
    tl_ps = [obj for obj in bpy.data.objects if obj.fp_id in tl.fp_deps and obj.fp_id != 0]
    pairs = [(i,j) for i in ml_ps for j in tl_ps]
    nearest = reduce(lambda rslt, pair: pair if ((loc(pair[1])[0] - loc(pair[0])[0])**2 + (loc(pair[1])[1] - loc(pair[0])[1])**2) < ((loc(rslt[1])[0] - loc(rslt[0])[0])**2 + (loc(rslt[1])[1] - loc(rslt[0])[1])**2) else rslt, pairs)
    center = nearest[0]
    cocenter = reduce(lambda res, item: item if item != center else res, ml_ps, None)
    farest = reduce(lambda r, p: p if (nearest[0] not in p and nearest[1] not in p) else r, pairs)
    tl_ang_deg = self._get_angle_deg_points2(tl_ps)
    ml_ang_deg = self._get_angle_deg_points2(ml_ps)
    diff_ang_deg = tl_ang_deg - ml_ang_deg
    diff_ang_rad = deg2rad(diff_ang_deg)
    diff_loc = [round(loc(nearest[1])[i] - loc(nearest[0])[i], 2) for i in range(3)] # ?????
    diff_quat = [(loc(tl_ps[1])[i] - loc(tl_ps[0])[i]) >= 0 for i in range(2)]

    print("ml =   ", ml)
    print("tl =   ", tl)
    print("ml_ps =   ", ml_ps)
    print("tl_ps =   ", tl_ps)
    print("pairs =   ", pairs)
    print("nearest =   ", nearest)
    print("center =   ", center)
    print("cocenter =   ", cocenter)
    print("farest =   ", farest)
    print("self._moving_contour", self._moving_contour)
    print("--------------------------------------")

    pairs = []
    coincidence = False

    for obj_ml in ml_ps:
      for obj_tl in tl_ps:
        if obj_ml == obj_tl:
          coincidence = True
          break
      if coincidence:
        break
    if not coincidence:
      if tl_ps[0].location[0] >= tl_ps[1].location[0] and ml_ps[0].location[0] >= ml_ps[1].location[0]:
        pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]
      elif tl_ps[0].location[0] < tl_ps[1].location[0] and ml_ps[0].location[0] >= ml_ps[1].location[0]:
        pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]
      elif tl_ps[0].location[0] >= tl_ps[1].location[0] and ml_ps[0].location[0] < ml_ps[1].location[0]:
        pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]
      elif tl_ps[1].location[0] >= tl_ps[0].location[0] and ml_ps[1].location[0] >= ml_ps[0].location[0]:
        pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]

    for obj in bpy.context.selected_objects:
      obj.select = False
    bpy.context.scene.objects.active = None
    one_objects_of_ml = [obj for obj in bpy.data.objects if obj.fp_id in self._moving_contour[1].fp_deps and obj.fp_id != 0]
    for obj_ml in one_objects_of_ml:
      for obj_ml_ps in ml_ps:
        if obj_ml_ps == obj_ml:
          for i in range(len(pairs)):
            if pairs[i][0] == obj_ml:
              pairs[i][1].select = True
    new_points = []
    for i in range(len(self._moving_contour) - 2):
      coincidence = False
      new_points.append(self._point.create(bpy.context))
      print("pairs", pairs)
      for obj in pairs:
        print("obj", obj)
        print("-----")
        print("obj[0].fp_id", obj[0].fp_id)
        print("self._moving_contour[i+1].fp_deps[0]", self._moving_contour[i+1].fp_deps[0])
        print("-----")
        if obj[0].fp_id == self._moving_contour[i+1].fp_deps[0]:
          pair = [ob for ob in bpy.data.objects if ob.fp_id == self._moving_contour[i+1].fp_deps[1] and ob.fp_id != 0]
          pairs += [(pair[0], new_points[i])]
          coincidence = True
          break
      if not coincidence:
        pair = [ob for ob in bpy.data.objects if ob.fp_id == self._moving_contour[i+1].fp_deps[0] and ob.fp_id != 0]
        pairs += [(pair[0], new_points[i])]

    # print("pairs", pairs)
    for obj in bpy.data.objects:
      obj.select = False
    for i in range(len(self._moving_contour) - 1):
      for obj in bpy.data.objects:
        obj.select = False
      draw_line = Line()
      if i == len(self._moving_contour)-2:
        pairs[i+1][1].select = True
        pairs[0][1].select = True
      else:
        pairs[i+1][1].select = True
        pairs[i+2][1].select = True
      draw_line.create(context)

    for i in range(len(pairs)-2):
      print("pairs[i+1]", pairs[i+1])
      print("pairs[i+2]", pairs[i+2])
      new_angle = get_angle(loc(pairs[i+1][0]), loc(pairs[i+2][0]))
      print("new_angle", new_angle)
      old_angle = get_angle(loc(ml_ps[0]), loc(ml_ps[1]))
      print("old_angle", old_angle)
      start_line_angle = get_angle(loc(tl_ps[0]), loc(tl_ps[1]))
      print("start_line_angle", start_line_angle)
      if old_angle == start_line_angle:
        pairs[i+2][1].fp_angle = new_angle
      else:
        pairs[i+2][1].fp_angle = -new_angle - old_angle + start_line_angle 
      print("distance", get_distance(loc(pairs[i+1][0]), loc(pairs[i+2][0])))
      pairs[i+2][1].fp_expression = str(get_distance(loc(pairs[i+1][0]), loc(pairs[i+2][0])))
    
    print("-____________-")
    print("pairs", pairs)



    # print("self._moving_contour =   ", self._moving_contour)
    # points_in_contour = []
    # for ob in bpy.data.objects:
    #   for obj in self._moving_contour:
    #     if (obj.fp_deps[0] == ob.fp_id or obj.fp_deps[1] == ob.fp_id):
    #       points_in_contour.append(ob)
    #       break

    # print("points_in_contour =   ", points_in_contour)

    # points_all = self.dependencies_in_contour(points_in_contour)

    # # sort points_all (dependencies_in_contour)
    # for i in range(len(points_all)-1):
    #   for j in range(i,len(points_all)-1):
    #     if points_all[i].fp_id > points_all[j+1].fp_id:
    #       tmp = points_all[i]
    #       points_all[i] = points_all[j+1]
    #       points_all[j+1] = tmp

    # print("points_all =   ", points_all)


    # new_angle = get_angle(loc(points_all[0]), loc(nearest[1]))
    # print("new_angle =   ", new_angle)
    # print("distance", get_distance(loc(points_all[0]), loc(nearest[1])))



    
    
    # pairs = []
    # coincidence = False


    # for obj_ml in ml_ps:
    #   for obj_tl in tl_ps:
    #     if obj_ml == obj_tl:
    #       coincidence = True
    #       break
    #   if coincidence:
    #     break
    # if not coincidence:
    #   if tl_ps[0].location[0] >= tl_ps[1].location[0] and ml_ps[0].location[0] >= ml_ps[1].location[0]:
    #     pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]
    #   elif tl_ps[0].location[0] < tl_ps[1].location[0] and ml_ps[0].location[0] >= ml_ps[1].location[0]:
    #     pairs = [(ml_ps[0], tl_ps[1]), (ml_ps[1], tl_ps[0])]
    #   elif tl_ps[0].location[0] >= tl_ps[1].location[0] and ml_ps[0].location[0] < ml_ps[1].location[0]:
    #     pairs = [(ml_ps[1], tl_ps[0]), (ml_ps[0], tl_ps[1])]
    #   elif tl_ps[1].location[0] >= tl_ps[0].location[0] and ml_ps[1].location[0] >= ml_ps[0].location[0]:
    #     pairs = [(ml_ps[0], tl_ps[0]), (ml_ps[1], tl_ps[1])]


    # for obj in bpy.context.selected_objects:
    #   obj.select = False
    # bpy.context.scene.objects.active = None
    # one_objects_of_ml = [obj for obj in bpy.data.objects if obj.fp_id in self._moving_contour[1].fp_deps and obj.fp_id != 0]
    # for obj_ml in one_objects_of_ml:
    #   for obj_ml_ps in ml_ps:
    #     if obj_ml_ps == obj_ml:
    #       for i in range(len(pairs)):
    #         if pairs[i][0] == obj_ml:
    #           pairs[i][1].select = True
    # new_points = []
    # for i in range(len(self._moving_contour) - 2):
    #   # length_line = get_line_length(self._moving_contour[i+1])
    #   # obj_point_of_line = [obj for obj in bpy.data.objects if (obj.fp_id == self._moving_contour[i+1].fp_deps[0] or obj.fp_id == self._moving_contour[i+1].fp_deps[1])]
    #   # new_angle = get_angle(loc(obj_point_of_line[0]), loc(obj_point_of_line[1]))
    #   # for obj in bpy.data.objects:
    #   #   if expression_to_value(obj.fp_expression) == length_line:
    #   #     fp_expression = obj.fp_expression
    #   #     break
    #   coincidence = False
    #   new_points.append(self._point.create(bpy.context))
    #   # new_points[i].fp_expression = fp_expression
    #   # if new_angle > 0:
    #   #   new_points[i].fp_angle = -new_angle + new_points[i].parent.fp_angle
    #   # else:
    #   #   new_points[i].fp_angle = +new_angle - new_points[i].parent.fp_angle
    #   for obj in pairs:
    #     if obj[0].fp_id == self._moving_contour[i+1].fp_deps[0]:
    #       pair = [ob for ob in bpy.data.objects if ob.fp_id == self._moving_contour[i+1].fp_deps[1] and ob.fp_id != 0]
    #       pairs += [(pair[0], new_points[i])]
    #       coincidence = True
    #       break
    #   if not coincidence:
    #     pair = [ob for ob in bpy.data.objects if ob.fp_id == self._moving_contour[i+1].fp_deps[0] and ob.fp_id != 0]
    #     pairs += [(pair[0], new_points[i])]

    # for obj in bpy.data.objects:
    #   obj.select = False
    # for i in range(len(self._moving_contour) - 1):
    #   for obj in bpy.data.objects:
    #     obj.select = False
    #   draw_line = Line()
    #   if i == len(self._moving_contour)-2:
    #     pairs[i+1][1].select = True
    #     pairs[0][1].select = True
    #   else:
    #     pairs[i+1][1].select = True
    #     pairs[i+2][1].select = True
    #   draw_line.create(context)


        
    # # for i in range(len(self._moving_contour)):
    # #   print("self._moving_contour", self._moving_contour)
    


    # for i in range(bpy.context.select
    # for line in [line for line in self._moving_contour if line != self._moving_line]:
    #   new_points = []
    #   for index,point in enumerate([p for p in bpy.data.objects if p.fp_id in line.fp_deps and p.fp_id != 0]):
    #     print("index", index)
    #     print("point", point)
    #     diff2 = [loc(point)[i] - loc(center)[i] for i in range(3)]
    #     # print("diff2", diff2)
    #     rad = sqrt(reduce(add, [(loc(point)[i] - loc(center)[i])**2 for i in range(2)]))
    #     # print("rad", rad)
    #     diff_ang_local_deg = diff_ang_deg + self._get_angle_deg_points2((center, point))
    #     if diff_quat[0] == False:
    #       diff_ang_local_deg = 180 - diff_ang_local_deg
    #     diff_ang_local_rad = deg2rad(diff_ang_local_deg)
    #     # print("diff_ang_local_rad", diff_ang_local_rad)
    #     new_loc_rel = (rad*cos(diff_ang_local_rad), rad*sin(diff_ang_local_rad), 0)
    #     print("new_loc_rel", new_loc_rel)
    #     new_loc_abs = [new_loc_rel[i] + loc(center)[i] + diff_loc[i] for i in range(3)]
    #     print("new_loc_abs", new_loc_abs)
    #     find_point = reduce(lambda res, item: item if all(round(loc(item)[i], 2) == round(new_loc_abs[i], 2) for i in range(2)) else res, get_all_points(), None)
    #     if find_point:
    #       new_points.append(find_point)
    #     else:
    #       new_points.append(self._point.create(bpy.context))
    #       if new_points[index].parent == None:
    #         new_points[index].fp_expression = location_to_expression(new_loc_abs)
    #       else:
    #         new_points[index].fp_expression = location_to_expression([new_loc_abs[i] - new_points[index].parent.location[i] for i in range(3)])
    #       new_points[index].fp_angle = rad2deg(atan(new_loc_abs[1]/new_loc_abs[0])) if new_loc_abs[0] != 0 else 0
    #     bpy.context.scene.objects.active = None
    #   new_line = self._line.create(bpy.context, new_points)
    #   new_lines.append(new_line)
    # for line in new_lines:
    #   line.select = True
    # self._target_line.select = True
        
    
  def _get_angle_deg_points2(self, points):
    diffs = [(loc(points[1])[i] - loc(points[0])[i]) for i in range(2)]
    hyp = sqrt(reduce(add, [diff**2 for diff in diffs]))
    return round(rad2deg(asin(diffs[1]/hyp)), 2) if hyp else 0
    
  def _point_by_fp_id(self, fp_id):
    return reduce(lambda res, obj: obj if obj.fp_id == fp_id else res, bpy.data.objects)


class FP_CopyingReflection(bpy.types.Operator):
  bl_idname = "fp.copying_reflection"
  bl_label = "FP Copying Reflection"

  @classmethod
  def poll(cls, context):
    return selection_is_contour() and is_one_of_lines(context.active_object)

  def execute(self, context):
    pivot = context.active_object
    pivot_points = self._get_line_points(pivot)
    contour = context.selected_objects[:]
    for line in contour:
      pass
    return {"FINISHED"}

  def _get_obj_by_fp_id(self, fp_id):
    for obj in bpy.data.objects:
      if obj.fp_id == fp_id:
        return obj

  def _get_line_point_ids(self, line):
    return tuple(fp_id for fp_id in line.fp_deps if fp_id != 0)

  def _get_line_points(self, line):
    return tuple(self._get_obj_by_fp_id(fp_id) for fp_id in self._get_line_point_ids(line))


clss = [
  FP_Copying, 
  FP_CopyingStop,
  FP_CopyingTarget,
  FP_CopyingContourTarget,
  FP_CopyingReflection,
]

def register():
  for cls in clss:
    bpy.utils.register_class(cls)

def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)
