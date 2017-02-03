import bpy

from math import sqrt

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.utils.fp_expression import expression_to_value


class PointOnBisector(Base):
  FP_TYPE = 'fp.draw.points.point_on_bisector'
  DEFAULT_EXPRESSION = '1'
  BASE_NAME = 'ТочкаНаБиссектрисе'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0.5, 0, 0.9)

  def poll(self, context):
    '''
    Нужны три выделенных точки,
    одна из которых является активной.
    '''
    return (
      context.active_object
      and context.active_object.fp_type == Point.FP_TYPE
      and len(context.selected_objects) == 3
      and all(is_one_of_points(item) for item in context.selected_objects)
    )

  def create(self, context):
    parent = context.active_object
    dep_id = tuple([
                     d.fp_id for d in context.selected_objects
                     if not d.fp_id == parent.fp_id
                     ] + [0])
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

    mat = bpy.data.materials.new('ЗаливкаТочкиНаБиссектрисе')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    collection_of_d_a_location = ([
      d for d in bpy.data.objects
      if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
    ])
    d_a_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    d1d2_dif = (
      d_a_location[0][0] - d_a_location[1][0],
      d_a_location[0][1] - d_a_location[1][1],
      0.0
    )
    d1d2_hyp = sqrt(d1d2_dif[0] ** 2 + d1d2_dif[1] ** 2)
    d1d3_hyp = d1d2_hyp / 2
    dirX = d1d2_dif[0] / d1d2_hyp
    dirY = d1d2_dif[1] / d1d2_hyp
    dirX *= d1d3_hyp
    dirY *= d1d3_hyp
    op_x = dirX + d_a_location[1][0]
    op_y = dirY + d_a_location[1][1]
    pd3_dif = (
      op_x - p_a_location[0],
      op_y - p_a_location[1],
      0.0
    )
    pd3_hyp = sqrt(pd3_dif[0] ** 2 + pd3_dif[1] ** 2)
    dirX = pd3_dif[0] / pd3_hyp
    dirY = pd3_dif[1] / pd3_hyp
    op_hyp = expression_to_value(obj.fp_expression)
    dirX *= op_hyp
    dirY *= op_hyp
    op_x = dirX
    op_y = dirY
    obj.location = (op_x, op_y, 0.0)

