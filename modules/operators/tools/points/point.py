import bpy

from fashion_project.modules.draw.points.point import Point

class FP_Point(bpy.types.Operator):
  '''
  Инструмент точка:
  создает новую точку.
  '''
  bl_idname = "fp.point"
  bl_label = "FP_Point"
  
  _point = Point()
  
  @classmethod
  def poll(cls, context):
    return cls._point.poll(context)
  
  def execute(self, context):
    self._point.create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_Point)
  
def unregister():
  bpy.utils.unregister_class(FP_Point)