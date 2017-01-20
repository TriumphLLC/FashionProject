import bpy

from fashion_project.modules.draw.points.free_point import FreePoint

class FP_FreePoint(bpy.types.Operator):
  '''
  Инструмент точка:
  создает новую точку.
  '''
  bl_idname = "fp.free_point"
  bl_label = "FP_FreePoint"
  
  _free_point = FreePoint()
  
  @classmethod
  def poll(cls, context):
    return cls._free_point.poll(context)
  
  def execute(self, context):
    self._free_point.create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_FreePoint)
  
def unregister():
  bpy.utils.unregister_class(FP_FreePoint)