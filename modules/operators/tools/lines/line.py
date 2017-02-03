import bpy

from mathutils import Vector


from fashion_project.modules.draw.lines.line import Line
# from fashion_project.modules.draw.points.point import Point


class FP_Line(bpy.types.Operator):
  '''
  Позволяет построить линию по двум точкам.

  Требует двух выделенных точек.
  '''
  bl_idname = 'fp.line'
  bl_label = 'FP_Line'
  
  _line = Line()

  @classmethod
  def poll(cls, context):
    return cls._line.poll(context)

  def execute(self, context):
    self._line.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_Line)

def unregister():
  bpy.utils.unregister_class(FP_Line)