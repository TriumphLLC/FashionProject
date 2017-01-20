import bpy

from fashion_project.modules.draw.lines.reflection_horizontal_line import ReflectionHorizontalLine

class FP_ReflectionHorizontalLine(bpy.types.Operator):
  '''
  Позволяет построить отражённую по
  горизонтали линию, указав родительскую

  Требует трех выделенных точек
  '''
  bl_idname = "fp.reflection_horizontal_line"
  bl_label = "FP_ReflectionHorizontalLine"

  _reflection_horizontal_line = ReflectionHorizontalLine()

  @classmethod
  def poll(cls, context):
    return cls._reflection_horizontal_line.poll(context)

  def execute(self, context):
    self._reflection_horizontal_line.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ReflectionHorizontalLine)

def unregister():
  bpy.utils.unregister_class(FP_ReflectionHorizontalLine)