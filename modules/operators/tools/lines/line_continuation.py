import bpy

from fashion_project.modules.draw.lines.line_continuation import LineContinuation
# from fashion_project.modules.draw.points.point import Point

class FP_LineContinuation(bpy.types.Operator):
  '''
  Позволяет построить продолжение линии

  Требует двух выделенных точек
  '''
  bl_idname = "fp.line_continuation"
  bl_label = "FP_LineContinuation"

  _line_continuation = LineContinuation()

  @classmethod
  def poll(cls, context):
    return cls._line_continuation.poll(context)

  def execute(self, context):
    self._line_continuation.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_LineContinuation)

def unregister():
  bpy.utils.unregister_class(FP_LineContinuation)
