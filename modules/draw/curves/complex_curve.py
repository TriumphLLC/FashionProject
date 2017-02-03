import bpy

from functools import reduce

from mathutils import Vector

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.detail import PointsForCreateDetail
from fashion_project.modules.draw.points import is_one_of_points 
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.curves import is_one_of_complex_curve
from fashion_project.modules.draw.curves.separation_complex_curve import SeparationComplexCurve


class ComplexCurve(Base):
  FP_TYPE = 'fp.draw.curves.complex_curve'
  FP_TYPE_CONTROL_POINT = 'fp.draw.curves.complex_curve.control_point'
  FP_TYPE_CONTROL_GUIDE = 'fp.draw.curves.complex_curve.control_guide'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0.2, 0.7, 0.7)
  GUIDE_COLOR = (0.9, 0.1, 0.1)
  HANDLE_COLOR = (0.8, 0.0, 0.0)
  HANDLE_RADIUS = 0.075
  DRAW_SEPARATION_CC = SeparationComplexCurve()

  POINTS = []
  
  def poll(self, context):
    '''
    Требует более двух выделенных точек.
    '''
    return (
      context.active_object
      and is_one_of_points(context.active_object)
      and len(context.selected_objects) > 2
      and all(is_one_of_points(item) for item in context.selected_objects)
    )
    
  def create(self, context):
    self.POINTS = []
    for point in bpy.context.selected_objects:
      point_location = list(get_point_abs_location(point))
      handle_left = [0,0,0]
      handle_right = [0,0,0]
      for i in range(len(point_location)):
        if i == 1:
          handle_left[i] = point_location[i] + 1
          handle_right[i] = point_location[i] - 1
        else:
          handle_left[i] = point_location[i]
          handle_right[i] = point_location[i]

      new_point = PointsForCreateDetail(pos = point_location, hl = handle_left, hr = handle_right)
      self.POINTS.append(new_point)

    dep_custom = [0]*30
    len_selected_obj = len(context.selected_objects) - 1
    for i in range(30):
      if i <= len_selected_obj:
        dep_custom[i] = context.selected_objects[i].fp_id
      else:
        dep_custom[i] = 0

    dep_id = tuple(dep_custom)
    curve = bpy.data.curves.new(name="Сложная кривая", type='CURVE')  
    curve.dimensions = self.CURVE_DIMS
    curve.bevel_depth = self.CURVE_BEVEL_DEPTH
    curve.bevel_resolution = 12
    curve.fill_mode = self.CURVE_FILL_MODE
    curve_mat = bpy.data.materials.new('ОбводкаСложнойКривой')
    curve_mat.diffuse_color = self.STROKE_COLOR
    curve.materials.append(curve_mat)
    bpyObj = bpy.data.objects.new("Сложная кривая", curve)
    bpyObj.location = (0,0,0) 
    bpyObj.lock_location = (True, True, True)
    bpyObj.show_name = True
    bpy.context.scene.objects.link(bpyObj)     
    Counter.register(bpyObj, self.FP_TYPE)
    bpyObj.fp_deps30 = dep_id
    spline = bpyObj.data.splines.new('BEZIER')
    curve.resolution_u = 32
    points = spline.bezier_points
    points.add(len(self.POINTS) - 1)
    locations = [
      get_point_abs_location(item) for item in bpy.data.objects
      if item.fp_id > 0 and item.fp_id in bpyObj.fp_deps30
    ]
    loc_x = 0
    loc_y = 0
    for i in range(len(locations)):
      loc_x += locations[i][0]/len(locations)
    for i in range(len(locations)):
      loc_y += locations[i][1]/len(locations)
    bpyObj.location = (loc_x, loc_y, 0.0)

    for index,loc in enumerate(locations):
      point_loc = [loc[i] - bpyObj.location[i] for i in range(3)]
      bpyObj.data.splines[0].bezier_points[index].co = point_loc 
      bpyObj.data.splines[0].bezier_points[index].handle_left = [(point_loc[i] - 1.0 if i == 1 else point_loc[i]) for i in range(3)]
      bpyObj.data.splines[0].bezier_points[index].handle_right = [(point_loc[i] + 1.0 if i == 1 else point_loc[i]) for i in range(3)]


  def update(self, obj, context):
    locations = [
      get_point_abs_location(item) for item in bpy.data.objects
      if item.fp_id > 0 and item.fp_id in obj.fp_deps30
    ]
    loc_x = 0
    loc_y = 0
    for i in range(len(locations)):
      loc_x += locations[i][0]/len(locations)
    for i in range(len(locations)):
      loc_y += locations[i][1]/len(locations)
    for index, loc in enumerate(locations):
      point_loc = [loc[i] - obj.location[i] for i in range(3)]
      obj.data.splines[0].bezier_points[index].co = point_loc

        
  def add_guides(self, obj):
    count = 0
    for x in obj.fp_deps30:
      if not x == 0:
        count += 1
    chs = bpy.data.curves.new('Управляющие', type='CURVE')
    chs.dimensions = self.CURVE_DIMS
    chs.bevel_depth = self.CURVE_BEVEL_DEPTH/1.0
    chs.bevel_resolution = 12
    chs.fill_mode = self.CURVE_FILL_MODE
    chs_mat = bpy.data.materials.new('ОбводкаУправляющей')
    chs_mat.diffuse_color = self.GUIDE_COLOR
    chs.materials.append(chs_mat)
    hobj = bpy.data.objects.new("Сложная кривая", chs)
    hobj.location = obj.location
    hobj.lock_location = (True, True, True)
    hobj.show_name = False
    hobj.hide_select = True
    hobj.fp_type = self.FP_TYPE_CONTROL_GUIDE
    bpy.context.scene.objects.link(hobj)

    for spline_index in range(count):
      spline_first = chs.splines.new('POLY')
      spline_first.points.add(1)
      spline_second = chs.splines.new('POLY')
      spline_second.points.add(1)
      bpoint = obj.data.splines[0].bezier_points[spline_index]

      if spline_index % 2 == 0:
        spline_first.points[0].co = list(obj.data.splines[0].bezier_points[spline_index].co) + [0.001]
        spline_first.points[1].co = list(bpoint.handle_right) + [0.001]
        spline_second.points[0].co = list(obj.data.splines[0].bezier_points[spline_index].co) + [0.001]
        spline_second.points[1].co = list(bpoint.handle_left) + [0.001]
      else:
        spline_first.points[0].co = list(bpoint.handle_left) + [0.001]
        spline_first.points[1].co = list(obj.data.splines[0].bezier_points[spline_index].co) + [0.001]
        spline_second.points[0].co = list(bpoint.handle_right) + [0.001]
        spline_second.points[1].co = list(obj.data.splines[0].bezier_points[spline_index].co) + [0.001]

    for wing_index in range(count):
      wing = obj.data.splines[0].bezier_points[wing_index]
      for handle_index in range(2):
        handle_loc = [wing.handle_left, wing.handle_right][handle_index]
        target_loc = [handle_loc[i] + obj.location[i] for i in range(3)]
        hcurv = bpy.data.curves.new("КонтрольнаяТочка", type="CURVE")
        hcurv.dimensions = "2D"
        hcurv.bevel_depth = self.CURVE_BEVEL_DEPTH/1.0
        hcurv.bevel_resolution = 12
        hcurv.fill_mode = "BOTH"
        hcurv_mat = bpy.data.materials.new('ЗаливкаКонтрольнойТочки')
        hcurv_mat.diffuse_color = self.HANDLE_COLOR
        hcurv.materials.append(hcurv_mat)
        pobj = bpy.data.objects.new("КонтрольнаяТочка.000", hcurv)
        pobj.lock_location = (False, False, True)
        pobj.show_name = False
        Counter.register(pobj, self.FP_TYPE_CONTROL_POINT)
        pobj.fp_deps = [obj.fp_id, wing_index, handle_index]
        bpy.context.scene.objects.link(pobj)

        pobj.location = target_loc
        spl = hcurv.splines.new('NURBS')
        spl.points.add(3)
        spl.use_cyclic_u = True
        for j in range(4):
          spl.points[j].co = (
            self.HANDLE_RADIUS if j in [1,2] else -self.HANDLE_RADIUS,
            self.HANDLE_RADIUS if j in [0,1] else -self.HANDLE_RADIUS,
            0.0,
            0.001
          )
    chs.resolution_u = 12
    
  def remove_guides(self):
    for obj in [
      obj for obj in bpy.data.objects 
      if obj.fp_type == self.FP_TYPE_CONTROL_POINT or obj.fp_type == self.FP_TYPE_CONTROL_GUIDE
    ]:
      bpy.context.scene.objects.unlink(obj)
      bpy.data.objects.remove(obj)
      
  def update_active(self, pobj):
    obj = reduce(lambda r, i: i if i.fp_id == pobj.fp_deps[0] else r, bpy.data.objects, None)
    bpoint = obj.data.splines[0].bezier_points[pobj.fp_deps[1]]
    new_loc_first = [pobj.location[i] - obj.location[i]  for i in range(3)]
    if pobj.fp_deps[2] == 0:
      bpoint.handle_left = new_loc_first
    elif pobj.fp_deps[2] == 1:
      bpoint.handle_right = new_loc_first
    gobj = [item for item in bpy.data.objects if item.fp_type == self.FP_TYPE_CONTROL_GUIDE][0]
    if pobj.fp_deps[1] % 2 == 0:
      if pobj.fp_deps[2] == 1:
        gobj.data.splines[pobj.fp_deps[1] * 2].points[1].co = new_loc_first + [0.001]
        new_loc = gobj.data.splines[pobj.fp_deps[1] * 2].points[0].co
      else:
        gobj.data.splines[pobj.fp_deps[1] * 2 + 1].points[1].co = new_loc_first + [0.001]
        new_loc = gobj.data.splines[pobj.fp_deps[1] * 2 + 1].points[0].co
    else:
      gobj.data.splines[pobj.fp_deps[1] * 2 + pobj.fp_deps[2]].points[0].co = new_loc_first + [0.001]
      new_loc = gobj.data.splines[pobj.fp_deps[1] * 2 + pobj.fp_deps[2]].points[1].co
    items = [item for item in bpy.data.objects if pobj.fp_type == item.fp_type and pobj.fp_deps[1] == item.fp_deps[1] and pobj.fp_deps[2] != item.fp_deps[2]]
    new_loc_second = []
    for i in range(3):
      tmp_location = new_loc[i] - new_loc_first[i]
      new_loc_second.append(new_loc[i] + tmp_location)  
    if pobj.fp_deps[2] == 0:
      bpoint.handle_right = new_loc_second
    elif pobj.fp_deps[2] == 1:
      bpoint.handle_left = new_loc_second
    if pobj.fp_deps[1] % 2 == 0:
      if pobj.fp_deps[2] == 1:
        gobj.data.splines[pobj.fp_deps[1] * 2 + 1].points[1].co = new_loc_second + [0.001]
      else:
        gobj.data.splines[pobj.fp_deps[1] * 2].points[1].co = new_loc_second + [0.001]
    else:
      gobj.data.splines[pobj.fp_deps[1] * 2 - pobj.fp_deps[2] + 1].points[0].co = new_loc_second + [0.001]
    target_loc = [new_loc_second[i] + obj.location[i] for i in range(3)]
    items[0].location = target_loc
    for separation_complex_curve in self.DRAW_SEPARATION_CC.get_all():
      self.DRAW_SEPARATION_CC.update(separation_complex_curve)


