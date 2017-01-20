import bpy

from mathutils import Vector


from fashion_project.modules.draw.lines.line_line_intersection import LineLineIntersection

class FP_LineLineIntersection(bpy.types.Operator):
  '''
  Позволяет построить точки на
  пересечении двух линий

  Требует двух выделенных линий
  '''
  bl_idname = "fp.line_line_intersection"
  bl_label = "FP_LineLineIntersection"

  _line_line_intersection = LineLineIntersection()

  @classmethod
  def poll(cls, context):
    return cls._line_line_intersection.poll(context)


  def execute(self, context):
    self._line_line_intersection.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_LineLineIntersection)

def unregiter():
  bpy.utils.unregister_class(FP_LineLineIntersection)

