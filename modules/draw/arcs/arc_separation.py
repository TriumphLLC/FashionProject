import bpy

from math import pi, tan

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.arcs import is_one_of_arc
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.utils import get_point_abs_location


class ArcSeparation(Base):
  FP_TYPE = 'fp.draw.points.arc_separation'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  FILL_COLOR = (0.8, 0.2, 0.2)
  DEFAULT_EXPRESSION = '1'
  BASE_NAME = 'РазделениеДуги'
  POINT_RADIUS = 0.075

  def poll(self, context):
    return (
      len(context.selected_objects) == 1
      and
      all(is_one_of_arc(item) for item in context.selected_objects)
    )

  def create(self, context):
    parent = context.active_object
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = bpy.context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.parent = parent
    obj.fp_expression = self.DEFAULT_EXPRESSION

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    mat = bpy.data.materials.new('ЗаливкаТочкиРазделениеДуги')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    expression = expression_to_value(obj.fp_expression)
    alfa = (180 * expression)/(pi * expression_to_value(obj.parent.fp_expression)) + obj.parent.fp_angles[0]
    b = (180 - alfa)/2
    rad = 57.2958
    k1 = tan(alfa/rad)
    k2 = tan((180 - b)/rad)
    location_o = get_point_abs_location(obj.parent.parent)
    b1 = -k1 * location_o[0] + location_o[1]
    b2 = -k2 * (location_o[0] + expression_to_value(obj.parent.fp_expression)) + location_o[1]
    op_x = (b2 - b1)/(k1 - k2)
    op_y = k1 * op_x + b1
    op_x -= location_o[0]
    op_y -= location_o[1]
    obj.location = (op_x, op_y, 0.0)
