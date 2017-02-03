import bpy

from functools import reduce
from math import sqrt

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.curves import is_one_of_complex_curve
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.utils.fp_expression import expression_to_value

class SeparationComplexCurve(Base):
  FP_TYPE = 'fp.draw.points.complexcurve'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  FILL_COLOR = (0.8, 0.2, 0.2)
  DEFAULT_EXPRESSION = '1'
  BASE_NAME = 'РазделениеСложнойКривой'
  POINT_RADIUS = 0.075

  def poll(self, context):
    return (
      context.active_object
      and is_one_of_complex_curve(context.active_object)
    )
    
  def create(self, context):
    parent = context.active_object
    dep_id = tuple(parent.fp_deps30)
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)

    line_length = [0]*29
    obj = bpy.context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.fp_deps30 = dep_id

    obj.parent = parent
    obj.fp_expression = self.DEFAULT_EXPRESSION

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    obj.fp_line_length = line_length

    mat = bpy.data.materials.new('ЗаливкаТочкиРазделениеСложнойКривой')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    
  def update(self, obj):
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    for i in range(30)
                                    if (d.fp_id == obj.fp_deps30[i]) and d.fp_id > 0
                                    ])
    points_parent = [get_point_abs_location(x) for x in collection_of_d_a_location]
    for i in range(len(collection_of_d_a_location)-1):
      bezier_t = 0.0
      bezier_l = 0.0
      step_t = 0.001
      handle_right = (
        obj.parent.data.splines[0].bezier_points[i].handle_right[0] - obj.parent.data.splines[0].bezier_points[0].co[0] + points_parent[0][0],
        obj.parent.data.splines[0].bezier_points[i].handle_right[1] - obj.parent.data.splines[0].bezier_points[0].co[1] + points_parent[0][1],
        0.0
      )
      handle_left = (
        obj.parent.data.splines[0].bezier_points[i+1].handle_left[0] - obj.parent.data.splines[0].bezier_points[1].co[0] + points_parent[1][0],
        obj.parent.data.splines[0].bezier_points[i+1].handle_left[1] - obj.parent.data.splines[0].bezier_points[1].co[1] + points_parent[1][1],
        0.0
      )
      previous_x = points_parent[i][0]
      previous_y = points_parent[i][1]
      while bezier_t <= 1.0:
        x = ((1 - bezier_t) ** 3) * points_parent[i][0] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[0] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[0] + (bezier_t ** 3) * points_parent[i+1][0]
        y = ((1 - bezier_t) ** 3) * points_parent[i][1] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[1] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[1] + (bezier_t ** 3) * points_parent[i+1][1]
        bezier_l += sqrt((x - previous_x) ** 2 + (y - previous_y) ** 2)
        previous_x = x
        previous_y = y
        bezier_t += step_t
      obj.fp_line_length[i] = bezier_l

    sum_length = 0.0
    for i in range(len(collection_of_d_a_location)-1):
      bezier_l = obj.fp_line_length[i]
      sum_length += bezier_l
      if expression_to_value(obj.fp_expression) < sum_length:
        if i == 0:
          bezier_l = 0.0
        else:
          bezier_l = sum_length - obj.fp_line_length[i]
        bezier_t = 0.0
        handle_right = (
          obj.parent.data.splines[0].bezier_points[i].handle_right[0] - obj.parent.data.splines[0].bezier_points[0].co[0] + points_parent[0][0],
          obj.parent.data.splines[0].bezier_points[i].handle_right[1] - obj.parent.data.splines[0].bezier_points[0].co[1] + points_parent[0][1],
          0.0
        )
        handle_left = (
          obj.parent.data.splines[0].bezier_points[i+1].handle_left[0] - obj.parent.data.splines[0].bezier_points[1].co[0] + points_parent[1][0],
          obj.parent.data.splines[0].bezier_points[i+1].handle_left[1] - obj.parent.data.splines[0].bezier_points[1].co[1] + points_parent[1][1],
          0.0
        )
        previous_x = points_parent[i][0]
        previous_y = points_parent[i][1]
        while bezier_t <= 1.0:
          x = ((1 - bezier_t) ** 3) * points_parent[i][0] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[0] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[0] + (bezier_t ** 3) * points_parent[i+1][0]
          y = ((1 - bezier_t) ** 3) * points_parent[i][1] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[1] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[1] + (bezier_t ** 3) * points_parent[i+1][1]
          bezier_l += sqrt((x - previous_x) ** 2 + (y - previous_y) ** 2)
          previous_x = x
          previous_y = y
          if bezier_l >= expression_to_value(obj.fp_expression):
            bezier_t = 2.0
          bezier_t += step_t
        loc = get_point_abs_location(obj.parent)
        x -= loc[0]
        y -= loc[1]
        obj.location = (x, y, 0.0)
        break
      elif expression_to_value(obj.fp_expression) > sum_length and i == len(collection_of_d_a_location)-2:
        obj.fp_expression = str(sum_length)
        loc = get_point_abs_location(obj.parent)
        x = points_parent[len(collection_of_d_a_location)-1][0] - loc[0]
        y = points_parent[len(collection_of_d_a_location)-1][1] - loc[1]
        obj.location = (x, y, 0.0)