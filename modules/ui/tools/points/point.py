import bpy

from fashion_project.modules.fp_draw.connected_points import FPDrawPoint

# Инструмент точка: создает новую точку
class FP_Point(bpy.types.Operator):
  bl_idname = "fp.point"
  bl_label = "FP_Point"

  def execute(self, context):
    FPDrawPoint.create(context)
    return {'FINISHED'}
