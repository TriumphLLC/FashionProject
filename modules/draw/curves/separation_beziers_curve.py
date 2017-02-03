import bpy

from functools import reduce
from math import sqrt

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.curves import is_one_of_bezier_curve
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.utils.fp_expression import expression_to_value

class SeparationBeziersCurve(Base):
  FP_TYPE = 'fp.draw.points.bezier2p'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  FILL_COLOR = (0.8, 0.2, 0.2)
  DEFAULT_EXPRESSION = '1'
  BASE_NAME = 'РазделениеКривойБезье'
  POINT_RADIUS = 0.075

  def poll(self, context):
    return (
      context.active_object
      and is_one_of_bezier_curve(context.active_object)
    )
    
  def create(self, context):
    parent = context.active_object
    points_parent = [obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_id in parent.fp_deps]
    dep_id = tuple([
                     d.fp_id for d in points_parent
                   ] + [0])
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = bpy.context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.fp_deps = dep_id

    obj.parent = parent
    obj.fp_expression = self.DEFAULT_EXPRESSION

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    mat = bpy.data.materials.new('ЗаливкаТочкиРазделениеКривойБезье')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    
  def update(self, obj):
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
                                    ])
    points_parent = [get_point_abs_location(x) for x in collection_of_d_a_location]
    handle_right = (
      obj.parent.data.splines[0].bezier_points[0].handle_right[0] - obj.parent.data.splines[0].bezier_points[0].co[0] + points_parent[0][0],
      obj.parent.data.splines[0].bezier_points[0].handle_right[1] - obj.parent.data.splines[0].bezier_points[0].co[1] + points_parent[0][1],
      0.0
    )
    handle_left = (
      obj.parent.data.splines[0].bezier_points[1].handle_left[0] - obj.parent.data.splines[0].bezier_points[1].co[0] + points_parent[1][0],
      obj.parent.data.splines[0].bezier_points[1].handle_left[1] - obj.parent.data.splines[0].bezier_points[1].co[1] + points_parent[1][1],
      0.0
    )
    bezier_t = 0.0
    bezier_l = 0.0
    step_t = 0.001
    x = 0.0
    y = 0.0
    previous_x = points_parent[0][0]
    previous_y = points_parent[0][1]
    while bezier_t <= 1.0:
      x = ((1 - bezier_t) ** 3) * points_parent[0][0] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[0] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[0] + (bezier_t ** 3) * points_parent[1][0]
      y = ((1 - bezier_t) ** 3) * points_parent[0][1] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[1] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[1] + (bezier_t ** 3) * points_parent[1][1]
      bezier_l += sqrt((x - previous_x) ** 2 + (y - previous_y) ** 2)
      previous_x = x
      previous_y = y
      if bezier_l >= expression_to_value(obj.fp_expression):
        bezier_t = 2.0
      bezier_t += step_t
    x += obj.parent.data.splines[0].bezier_points[0].co[0] - points_parent[0][0]
    y += obj.parent.data.splines[0].bezier_points[0].co[1] - points_parent[0][1]
    obj.location = (x, y, 0.0)