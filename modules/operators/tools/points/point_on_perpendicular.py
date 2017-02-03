import bpy

from fashion_project.modules.draw.points.point_on_perpendicular import PointOnPerpendicular

class FP_PointOnPerpendicular(bpy.types.Operator):
  '''
  Инструмент точка на перпендикуляре:
  справочная информация.

  Требует двух выделенных точек
  '''
  bl_idname = "fp.point_on_perpendicular"
  bl_label = "FP_PointOnPerpendicular"

  
  @classmethod
  def poll(cls, context):
    return PointOnPerpendicular().poll(context)


  def execute(self, context):
    PointOnPerpendicular().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PointOnPerpendicular)

def unregister():
  bpy.utils.unregister_class(FP_PointOnPerpendicular)
