import bpy


class FP_PointOnBisector(bpy.types.Operator):
  '''
  Инструмент точка на биссектрисе:
  создает новую точку на биссектрисе
  острого угла по трем другим точкам.
  '''
  bl_idname = "fp.point_on_bisector"
  bl_label = "FP_PointOnBisector"

  def execute(self, context):
    return {'FINISHED'}

