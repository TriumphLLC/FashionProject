'''
@deprecated - следует использовать стандартное удаление блендера
'''

import bpy

from math import sqrt, cos, radians, asin, acos, degrees

from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line

from fashion_project.modules.utils.fp_expression import expression_to_value


class FP_DrawPointDelete(bpy.types.Operator):
  '''
  Оператор удаления точки лекала.
  '''
  bl_idname='fp_drawpoint.delete'
  bl_label='FP_DrawPointDelete'

  def execute(self, context):
    obj = context.active_object
    d_point = Point()
    d_line = Line()
    points = d_point.get_all()

    children = [p for p in points if p.parent == obj]
    for nx in children:
      rm = obj
      rm_a = rm.fp_angle
      rm_l = expression_to_value(rm.fp_expression)
      nx_a = nx.fp_angle
      nx_l = expression_to_value(nx.fp_expression)

      _a = 360 - (180 - rm_a + nx_a)
      new_l = sqrt(rm_l**2 + nx_l**2 - 2*rm_l*nx_l*cos(radians(_a)))

      dx = nx.location[0] + rm.location[0]
      dy = nx.location[1] + rm.location[1]

      new_a = degrees(asin(dy/new_l))
      new_a = new_a if dx > 0 else 180 - new_a

      if obj.parent:
        nx.parent = obj.parent

      nx.fp_expression = str(new_l)
      nx.fp_angle = new_a
      
    lines = tuple(
      l for l in bpy.data.objects 
      if l.fp_type == Line.FP_TYPE and obj.fp_id in l.fp_deps
    )
    for ln in lines:
      bpy.context.scene.objects.unlink(ln)
      bpy.data.objects.remove(ln)

    bpy.ops.object.delete()

    return {'FINISHED'}
