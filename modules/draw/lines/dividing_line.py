import bpy

from math import sqrt

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.utils.fp_expression import expression_to_value


class DividingLine(Base):
  FP_TYPE = 'fp.draw.points.dividing_line'
  BASE_NAME = 'РазделениеЛинии'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def create(self, count, context):
    number = 1
    parent = context.active_object
    parent = [obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_id in parent.fp_deps]
    dep_id = tuple([
                     parent[1].fp_id
                     ] + [0, 0])
    nameParent = parent[0].name
    nameSelect = parent[1].name

    while number <= expression_to_value(count):
      bpy.data.objects[nameSelect].select = True
      bpy.data.objects[nameParent].select = True

      bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
      obj = context.object

      Counter.register(obj, self.FP_TYPE)
      obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

      obj.parent = parent[0]

      obj.fp_deps = dep_id

      obj.fp_expression = count

      obj.fp_number = number
      number += 1

      obj.lock_location = (True, True, True)
      obj.show_name = True
      obj.select = False

      mat = bpy.data.materials.new('ЗаливкаТочкиРазделениеЛинии')
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
    pd_hyp = sqrt(pd_dif[0] ** 2 + pd_dif[1] ** 2)
    op_hyp = pd_hyp / (1 + expression_to_value(obj.fp_expression))
    op_hyp *= obj.fp_number
    proportion = op_hyp / pd_hyp if pd_hyp else 0
    op_x = pd_dif[0] * proportion
    op_y = pd_dif[1] * proportion
    obj.location = (-op_x, -op_y, 0.0)



  def poll(self, context):
    '''
    Нужна выделенная линия.
    '''
    return (
      context.active_object
      and context.active_object.fp_type == Line.FP_TYPE
      and len(context.selected_objects) == 1
    )
