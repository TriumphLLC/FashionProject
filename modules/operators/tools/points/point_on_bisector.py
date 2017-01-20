import bpy

from fashion_project.modules.draw.points.point_on_bisector import PointOnBisector


class FP_PointOnBisector(bpy.types.Operator):
  '''
  Инструмент точка на биссектрисе:
  создает новую точку на биссектрисе
  острого угла по трем другим точкам.

  Требует трех выделенных точек
  '''
  bl_idname = "fp.point_on_bisector"
  bl_label = "FP_PointOnBisector"

  @classmethod
  def poll(cls, context):
    return PointOnBisector().poll(context)


  def execute(self, context):
    PointOnBisector().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PointOnBisector)

def unregister():
  bpy.utils.unregister_class(FP_PointOnBisector)