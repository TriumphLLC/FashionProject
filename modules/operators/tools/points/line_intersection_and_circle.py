import bpy

from fashion_project.modules.draw.points.line_intersection_and_circle import LineIntersectionAndCircle

class FP_LineIntersectionAndCircle(bpy.types.Operator):
  '''
  Позволяет построить точки
  пересечения линии и окружности
  '''
  bl_idname = "fp.line_intersection_and_circle"
  bl_label = "FP_LineIntersectionAndCircle"

  @classmethod
  def poll(cls, context):
    return LineIntersectionAndCircle().poll(context)

  def execute(self, context):
    LineIntersectionAndCircle().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_LineIntersectionAndCircle)

def unregister():
  bpy.utils.unregister_class(FP_LineIntersectionAndCircle)
