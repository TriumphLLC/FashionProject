import bpy

from math import sqrt

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.utils.fp_expression import expression_to_value


class ReflectionVerticalLine(Base):
  FP_TYPE = 'fp.draw.points.reflection_vertical_line'
  BASE_NAME = 'ВертикальноеОтражениеЛинии'
  DEFAULT_EXPRESSION = '1'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0.5, 0, 0.9)

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

    mat = bpy.data.materials.new('ЗаливкаТочкиОтражениеЛинии')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    draw_line = Line()
    parent.select = True
    obj.select = True
    draw_line.create(context)

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
                                    ])
    d_a_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    d2d1_dif = (
      d_a_location[1][0] - d_a_location[0][0],
      d_a_location[1][1] - d_a_location[0][1],
      0.0
    )
    op_x = -d2d1_dif[0]
    op_y = d2d1_dif[1]
    obj.location = (op_x, op_y, 0.0)
