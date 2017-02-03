import bpy

from math import sqrt

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.points import is_one_of_points


class PointXY(Base):
  FP_TYPE = 'fp.draw.points.point_xy'
  DEFAULT_EXPRESSION = '1.1'
  BASE_NAME = 'ТочкаИзДвухXиY'
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

    mat = bpy.data.materials.new('ЗаливкаТочкиИзДвухXиY')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    d_a_location = get_point_abs_location([
                                            d for d in bpy.data.objects
                                            if d.fp_id == obj.fp_deps[0] and d.fp_id > 0
                                            ][0])
    op_x = 0
    op_y = d_a_location[1] - p_a_location[1]
    obj.location = (op_x, op_y, 0.0)


