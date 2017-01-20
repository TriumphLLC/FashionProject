import bpy

from math import sqrt
from mathutils import Vector

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.utils.fp_expression import expression_to_value


class LineContinuation(Base):
  FP_TYPE = 'fp.draw.points.line_continuation'
  BASE_NAME = 'ПродолжениеЛинии'
  DEFAULT_EXPRESSION = '1'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0, 0.6, 0.4)

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

    mat = bpy.data.materials.new('ЗаливкаТочкиПродолжениеЛинии')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    draw_line = Line()
    parent.select = True
    obj.select = True
    draw_line.create(context)


  def update(self, line_obj, context):
    p_a_location = get_point_abs_location(line_obj.parent)
    d_a_location = get_point_abs_location([
                                            d for d in bpy.data.objects
                                            if d.fp_id == line_obj.fp_deps[0] and d.fp_id > 0
                                            ][0])
    pd_dif = (
      p_a_location[0] - d_a_location[0],
      p_a_location[1] - d_a_location[1],
      0.0
    )
    pd_hyp = sqrt(pd_dif[0] ** 2 + pd_dif[1] ** 2)
    op_hyp = expression_to_value(line_obj.fp_expression)
    op_hyp += pd_hyp
    proportion = op_hyp / pd_hyp if pd_hyp else 0
    op_x = d_a_location[0] + pd_dif[0] * proportion - p_a_location[0]
    op_y = d_a_location[1] + pd_dif[1] * proportion - p_a_location[1]
    line_obj.location = (op_x, op_y, 0.0)
