import bpy

from mathutils import Vector


from fashion_project.modules.draw.lines.line_for_dart import LineForDart
# from fashion_project.modules.draw.points.point import Point


class FP_LineForDart(bpy.types.Operator):
  '''
  Позволяет построить линию по двум точкам.

  Требует двух выделенных точек.
  '''
  bl_idname = 'fp.line_for_dart'
  bl_label = 'FP_Line_For_Dart'
  
  _line_for_dart = LineForDart()

  @classmethod
  def poll(cls, context):
    return cls._line_for_dart.poll(context)

  def execute(self, context):
    self._line_for_dart.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_LineForDart)

def unregister():
  bpy.utils.unregister_class(FP_LineForDart)