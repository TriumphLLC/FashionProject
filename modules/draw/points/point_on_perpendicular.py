import bpy

from math import sqrt, fabs

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.utils.fp_expression import expression_to_value


class PointOnPerpendicular(Base):
  FP_TYPE = 'fp.draw.points.point_on_perpendicular'
  DEFAULT_EXPRESSION = '1.5'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'ТочкаНаПерпендикуляре'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def poll(self, context):
    '''
    Нужны две выделенных точки,
    одна из которых является активной.
    '''
    return (
      context.active_object
      and is_one_of_points(context.active_object)
      and len(context.selected_objects) == 2
      and all(is_one_of_points(item) for item in context.selected_objects)
    )
    

  def create(self, context):
    parent = context.active_object
    dep_id = tuple([
                     d.fp_id for d in context.selected_objects
                     if not d.fp_id == parent.fp_id
                     ] + [0, 0])
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.parent = parent

    obj.fp_deps = dep_id

    obj.fp_expression = self.DEFAULT_EXPRESSION

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    mat = bpy.data.materials.new('ЗаливкаТочкиНаПерпендикуляре')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)


  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    d_a_location = get_point_abs_location([
                                            d for d in bpy.data.objects
                                            if d.fp_id == obj.fp_deps[0] and d.fp_id > 0
                                            ][0])
    pd_dif = (
      p_a_location[0] - d_a_location[0],
      p_a_location[1] - d_a_location[1],
      0.0
    )
    a_hyp = expression_to_value(obj.fp_expression)
    if fabs(p_a_location[0] - d_a_location[0]) < 0.0000001:
      if pd_dif[1] > 0:
        op_x = -a_hyp
      else:
        op_x = a_hyp
      op_y = 0
    elif fabs(p_a_location[1] - d_a_location[1]) < 0.0000001:
      if pd_dif[0] > 0:
        op_y = a_hyp
      else:
        op_y = -a_hyp
      op_x = 0
    else:
      k = (p_a_location[1] - d_a_location[1]) / (p_a_location[0] - d_a_location[0]) if (p_a_location[0] - d_a_location[0]) else 0
      _k = -1/k
      b = -_k*p_a_location[0] + p_a_location[1]
      if k == 0:
        op_x = 0
        if pd_dif[0] > 0:
          op_y = a_hyp
        else:
          op_y = -a_hyp
      else:
        if k < 0:
          if pd_dif[0] < 0:
            op_x = -100
          else:
            op_x = 100
        else:
          if pd_dif[0] < 0:
            op_x = 100
          else:
            op_x = -100
        op_y = _k * op_x + b
        d1d2_dif = (
          op_x - p_a_location[0],
          op_y - p_a_location[1],
          0.0
        )
        d1d2_hyp = sqrt(d1d2_dif[0] ** 2 + d1d2_dif[1] ** 2)
        proportion = a_hyp / d1d2_hyp
        op_x = d1d2_dif[0] * proportion
        op_y = d1d2_dif[1] * proportion


    obj.location = (op_x, op_y, 0.0)