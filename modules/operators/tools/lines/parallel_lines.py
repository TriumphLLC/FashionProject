import bpy

from fashion_project.modules.draw.lines.parallel_lines import ParallelLines

class FP_ParallelLines(bpy.types.Operator):
  '''
  Позволяет построить параллельную
  линию, указав родительскую

  Требует трех выделынных точек
  '''
  bl_idname = "fp.parallel_lines"
  bl_label = "FP_ParallelLines"

  _parallel_lines = ParallelLines()
  
  @classmethod
  def poll(cls, context):
    return cls._parallel_lines.poll(context)

  def execute(self, context):
    self._parallel_lines.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ParallelLines)

def unregister():
  bpy.utils.unregister_class(FP_ParallelLines)
