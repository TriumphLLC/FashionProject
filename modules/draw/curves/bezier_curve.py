import bpy

from functools import reduce

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points 
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.curves import is_one_of_bezier_curve
from fashion_project.modules.draw.curves.separation_beziers_curve import SeparationBeziersCurve


class BezierCurve(Base):
  FP_TYPE = 'fp.draw.curves.bezier2p'
  FP_TYPE_CONTROL_POINT = 'fp.draw.curves.bezier2p.control_point'
  FP_TYPE_CONTROL_GUIDE = 'fp.draw.curves.bezier2p.control_guide'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0, 0.6, 0.4)
  GUIDE_COLOR = (0.9, 0.1, 0.1)
  HANDLE_COLOR = (0.8, 0.0, 0.0)
  HANDLE_RADIUS = 0.05
  DRAW_SEPARATION_BC = SeparationBeziersCurve()
  
  def poll(self, context):
    '''
    Требует двух выделенных точек
    '''
    return (
      context.active_object
      and is_one_of_points(context.active_object)
      and len(context.selected_objects) == 2
      and all(is_one_of_points(item) for item in context.selected_objects)
    )
    
  def create(self, context):
    curve = bpy.data.curves.new(name="КриваяБезье", type="CURVE")
    curve.dimensions = self.CURVE_DIMS
    curve.bevel_depth = self.CURVE_BEVEL_DEPTH
    curve.bevel_resolution = 12
    curve.fill_mode = self.CURVE_FILL_MODE
    curve_mat = bpy.data.materials.new('ОбводкаКривойБезье')
    curve_mat.diffuse_color = self.STROKE_COLOR
    curve.materials.append(curve_mat)
    obj = bpy.data.objects.new("КриваяБезье", curve)
    obj.location = (0,0,0)
    obj.lock_location = (True, True, True)
    obj.show_name = True
    context.scene.objects.link(obj)
    Counter.register(obj, self.FP_TYPE)
    obj.fp_deps = tuple([item.fp_id for item in context.selected_objects] + [0])
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(1)
    curve.resolution_u = 64
    locations = [
      get_point_abs_location(item) for item in bpy.data.objects
      if item.fp_id > 0 and item.fp_id in obj.fp_deps
    ]
    obj.location = [
      (locations[0][j] + locations[1][j])/2
      for j in range(3)
    ]
    for index, loc in enumerate(locations):
      point_loc = [loc[i] - obj.location[i] for i in range(3)]
      obj.data.splines[0].bezier_points[index].co = point_loc 
      obj.data.splines[0].bezier_points[index].handle_left = [(point_loc[i] - 1.0 if i == 1 else point_loc[i]) for i in range(3)]
      obj.data.splines[0].bezier_points[index].handle_right = [(point_loc[i] + 1.0 if i == 1 else point_loc[i]) for i in range(3)]
    
  def update(self, obj, context):
    locations = [
      get_point_abs_location(item) for item in bpy.data.objects
      if item.fp_id > 0 and item.fp_id in obj.fp_deps
    ]
    obj.location = [
      (locations[0][j] + locations[1][j])/2
      for j in range(3)
    ]
    for index, loc in enumerate(locations):
      point_loc = [loc[i] - obj.location[i] for i in range(3)]
      obj.data.splines[0].bezier_points[index].co = point_loc
        
  def add_guides(self, obj):
    chs = bpy.data.curves.new('Управляющие', type='CURVE')
    chs.dimensions = self.CURVE_DIMS
    chs.bevel_depth = self.CURVE_BEVEL_DEPTH/1.0
    chs.bevel_resolution = 12
    chs.fill_mode = self.CURVE_FILL_MODE
    chs_mat = bpy.data.materials.new('ОбводкаУправляющей')
    chs_mat.diffuse_color = self.GUIDE_COLOR
    chs.materials.append(chs_mat)
    hobj = bpy.data.objects.new("КриваяБезье", chs)
    hobj.location = obj.location
    hobj.lock_location = (True, True, True)
    hobj.show_name = False
    hobj.hide_select = True
    hobj.fp_type = self.FP_TYPE_CONTROL_GUIDE
    bpy.context.scene.objects.link(hobj)
    for spline_index in range(2):
      spline = chs.splines.new('POLY')
      spline.points.add(1)
      bpoint = obj.data.splines[0].bezier_points[spline_index]
      if spline_index == 0:
        spline.points[0].co = list(obj.data.splines[0].bezier_points[0].co) + [0.001]
        spline.points[1].co = list(bpoint.handle_right) + [0.001]
      elif spline_index == 1:
        spline.points[0].co = list(bpoint.handle_left) + [0.001]
        spline.points[1].co = list(obj.data.splines[0].bezier_points[1].co) + [0.001]
    for wing_index in range(2):
      wing = obj.data.splines[0].bezier_points[wing_index]
      for handle_index in range(2):
        if wing_index == 0 and handle_index == 0:
          continue
        if wing_index == 1 and handle_index == 1:
          continue
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
    new_loc = [pobj.location[i] - obj.location[i]  for i in range(3)]
    if pobj.fp_deps[2] == 0:
      bpoint.handle_left = new_loc
    elif pobj.fp_deps[2] == 1:
      bpoint.handle_right = new_loc
    gobj = [item for item in bpy.data.objects if item.fp_type == self.FP_TYPE_CONTROL_GUIDE][0]
    gobj.data.splines[pobj.fp_deps[1]].points[pobj.fp_deps[2]].co = new_loc + [0.001]
    for separation_beziers_curve in self.DRAW_SEPARATION_BC.get_all():
      self.DRAW_SEPARATION_BC.update(separation_beziers_curve)
