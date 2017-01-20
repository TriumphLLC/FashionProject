import bpy

from fashion_project.modules.draw.circles.circle import Circle


class FP_Circle(bpy.types.Operator):
  '''
  Позволяет построить окружность.

  Требует выделенной точки.
  '''
  bl_idname = "fp.circle"
  bl_label = "FP_Circle"

  _circle = Circle()

  @classmethod
  def poll(cls, context):
    return cls._circle.poll(context)

  def execute(self, context):
    self._circle.create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_Circle)

def unregister():
  bpy.utils.unregister_class(FP_Circle)
