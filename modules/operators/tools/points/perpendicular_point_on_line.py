import bpy

from fashion_project.modules.draw.points.perpendicular_point_on_line import PerpendicularPointOnLine


class FP_PerpendicularPointOnLine(bpy.types.Operator):
  '''
  Позволяет построить точку на
  пересечении линии и перпендикуляра
  к этой линии из

  Требует трех выбранных точек
  '''
  bl_idname = "fp.perpendicular_point_on_line"
  bl_label = "FP_PerpendicularPointOnLine"
  
  @classmethod
  def poll(cls, context):
    return PerpendicularPointOnLine().poll(context)

  def execute(self, context):
    PerpendicularPointOnLine().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PerpendicularPointOnLine)

def unregister():
  bpy.utils.unregister_class(FP_PerpendicularPointOnline)