import bpy

from fashion_project.modules.draw.lines.reflection_vertical_line import ReflectionVerticalLine

class FP_ReflectionVerticalLine(bpy.types.Operator):
  '''
  Позволяет построить отражённую по
  вертикальную линию, указав родительскую

  Требует трех выделенных точек
  '''
  bl_idname = "fp.reflection_vertical_line"
  bl_label = "FP_ReflectionVerticalLine"

  _reflection_vertical_line = ReflectionVerticalLine()

  @classmethod
  def poll(cls, context):
    return cls._reflection_vertical_line.poll(context)

  def execute(self, context):
    self._reflection_vertical_line.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ReflectionVerticalLine)

def unregister():
  bpy.utils.unregister_class(FP_ReflectionVerticalLine)