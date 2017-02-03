import bpy

from fashion_project.modules.draw.lines.dividing_line import DividingLine

class FP_DividingLine(bpy.types.Operator):
  '''
  Позволяет построить поределённое
  количество точек на линии
  на равном расстоянии.

  Требует выделенной линии.
  '''
  bl_idname = "fp.dividing_line"
  bl_label = "FP_DividingLine"

  _dividing_line = DividingLine()

  @classmethod
  def poll(cls, context):
    return cls._dividing_line.poll(context)

  def execute(self, context):
    parent = context.active_object
    self._dividing_line.create(parent.fp_count, context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_DividingLine)

def unregister():
  bpy.utils.unregister_class(FP_DividingLine)