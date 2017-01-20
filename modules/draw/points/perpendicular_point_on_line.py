import bpy

from math import sqrt, fabs

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points


class PerpendicularPointOnLine(Base):
  FP_TYPE = 'fp.draw.points.perpendicular_point_on_line'
  DEFAULT_EXPRESSION = '1.25'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'ПерпендикулярнаяТочкаНаЛинии'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def poll(self, context):
    '''
        Нужны три выделенных точки,
        одна из которых является активной.
        '''
    return (
      len(context.selected_objects) == 3
      and
      all(is_one_of_points(item) for item in context.selected_objects)
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

    mat = bpy.data.materials.new('ЗаливкаПерпендикулярнаяТочкаНаЛинии')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    collection_of_d_a_location = ([
      d for d in bpy.data.objects
      if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
    ])
    d_a_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    if fabs(d_a_location[0][0] - d_a_location[1][0]) < 0.0000001:
      op_x = d_a_location[0][0] - p_a_location[0]
      op_y = 0
    elif fabs(d_a_location[0][1] - d_a_location[1][1]) < 0.0000001:
      op_x = 0
      op_y = d_a_location[0][1] - p_a_location[1]
    else:
      k_first_line = (d_a_location[0][1] - d_a_location[1][1]) / (d_a_location[0][0] - d_a_location[1][0])
      k_second_line = -1/k_first_line
      b_first_line = -k_first_line * d_a_location[0][0] + d_a_location[0][1]
      b_second_line = -k_second_line * p_a_location[0] + p_a_location[1]
      op_x = (b_second_line - b_first_line) / (k_first_line - k_second_line)
      op_y = k_first_line * op_x + b_first_line
      op_x -= p_a_location[0]
      op_y -= p_a_location[1]
    obj.location = (op_x, op_y, 0.0)
