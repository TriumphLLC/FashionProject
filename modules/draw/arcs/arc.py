import bpy

from math import pi, ceil, sqrt, tan, acos, asin, sin, cos
from operator import add, sub

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points.free_point import FreePoint
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.utils.mathlib import deg2rad, rad2deg


class Arc(Base):
  FP_TYPE = 'fp.draw.arcs.arc'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0, 0.6, 0.4)

  '''Количество сплайнов, используемых для построения окружности - больше сплайнов - плавнее окружность.'''
  _splines = 4

  '''Радиус окружности, вычисляется из fp_expression.'''
  _radius = 0.0

  DRAW_FREE_POINT = FreePoint()

  def poll(self, context):
    return context.active_object and is_one_of_points(context.active_object) and len(context.selected_objects) == 1

  def create(self, context):
    curve = bpy.data.curves.new(name="Дуга", type="CURVE")
    curve.dimensions = self.CURVE_DIMS
    curve.bevel_depth = self.CURVE_BEVEL_DEPTH
    curve.bevel_resolution = 12
    curve.fill_mode = self.CURVE_FILL_MODE
    curve_mat = bpy.data.materials.new('ОбводкаДуги')
    curve_mat.diffuse_color = self.STROKE_COLOR
    curve.materials.append(curve_mat)
    obj = bpy.data.objects.new("Дуга", curve)
    context.scene.objects.link(obj)
    obj.parent = context.active_object
    obj.location = (0, 0, 0)
    obj.lock_location = (True, True, True)
    obj.show_name = True
    Counter.register(obj, self.FP_TYPE)
    for i in range(self._splines):
      spline = curve.splines.new('BEZIER')
      spline.bezier_points.add(1)
      for j in range(2):
        spline.bezier_points[j].co = (0, 0, 0)
        spline.bezier_points[j].handle_left = (0, 0, 0)
        spline.bezier_points[j].handle_right = (0, 0, 0)
    obj.fp_angles = (0.0, 90.0)
    obj.fp_expression = '1.0'
    curve.resolution_u = 64
    # for i in range(2):
    #   obj.select = True
    #   self.DRAW_FREE_POINT.create(context)
    #   context.active_object.fp_expression = obj.fp_expression
    #   context.active_object.fp_angle = obj.fp_angles[i]


  def update(self, obj, context):
    self._radius = expression_to_value(obj.fp_expression)
    if self._radius == 0:
      return
    angle_diff_deg = -sub(*obj.fp_angles)
    if angle_diff_deg < 0:
      obj.fp_angles = (obj.fp_angles[1], obj.fp_angles[1])
      return
    if angle_diff_deg > 360:
      obj.fp_angles = (obj.fp_angles[0], obj.fp_angles[0] + 360.0)
      return
    counter = 0
    part = 360.0/self._splines
    rng = int(angle_diff_deg//part)
    for i in range(rng):
      if i < self._splines:
        counter += 1
        self._draw_spline(obj.data.splines[i], (obj.fp_angles[0] + i*part, obj.fp_angles[0] + counter*part))
    if counter < self._splines:
      self._draw_spline(obj.data.splines[counter], (obj.fp_angles[0] + counter*part, obj.fp_angles[1]))
      counter += 1
      for i in range(self._splines - counter):
        self._draw_collapsed_spline(obj.data.splines[counter + i])


  def _draw_spline(self, spline, angles_deg):
    handle = (4/3) * tan(deg2rad(-sub(*angles_deg))/4) * self._radius
    for index, angle_cur in enumerate([deg2rad(angle) for angle in angles_deg]):
      hyp = sqrt(handle**2 + self._radius**2)
      angle_inter = acos(self._radius/hyp)
      angle_bot = (sub, add)[index](angle_cur, angle_inter)
      angle_top = (add, sub)[index](angle_cur, angle_inter)
      angle_left = (angle_bot, angle_top)[index]
      angle_right = (angle_top, angle_bot)[index]
      spline.bezier_points[index].co = (self._radius * cos(angle_cur), self._radius * sin(angle_cur), 0)
      spline.bezier_points[index].handle_left = (hyp * cos(angle_left), hyp * sin(angle_left), 0)
      spline.bezier_points[index].handle_right = (hyp * cos(angle_right), hyp * sin(angle_right), 0)

  def _draw_collapsed_spline(self, spline):
    for index in range(2):
      spline.bezier_points[index].co = (0, 0, 0)
      spline.bezier_points[index].handle_left = (0, 0, 0)
      spline.bezier_points[index].handle_right = (0, 0, 0)
