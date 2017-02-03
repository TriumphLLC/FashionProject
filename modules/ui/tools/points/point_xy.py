import bpy


class FP_PointXY(bpy.types.Operator):
  '''
  Позволяет построить точку, которая привязана к координатам
  родительских точек. Из первой точки берется Х, из второй - У.
  '''
  bl_idname = "fp.point_xy"
  bl_label = "FP_PointXY"

  def execute(self, context):
    return {'FINISHED'}


