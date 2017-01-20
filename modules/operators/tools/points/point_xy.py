import bpy

from fashion_project.modules.draw.points.point_xy import PointXY

class FP_PointXY(bpy.types.Operator):
  '''
  Позволяет построить точку, 
  которая привязана к координатам
  родительских точек.

  Требует двух выделенных точек
  '''
  bl_idname = "fp.point_xy"
  bl_label = "FP_PointXY"

  
  @classmethod
  def poll(cls, context):
    return PointXY().poll(context)

  def execute(self, context):
    PointXY().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PointXY)

def unregister():
  bpy.utils.unregister_class(FP_PointXY)