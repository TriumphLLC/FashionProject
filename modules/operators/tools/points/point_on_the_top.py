import bpy

from fashion_project.modules.draw.points.point_on_the_top import PointOnTheTop

class FP_PointOnTheTop(bpy.types.Operator):
  '''
  Позволяет строить точку на вершине
  прямого угла прямоугольного треугольника

  Требует четырех выделенных точек
  '''
  bl_idname = "fp.point_on_the_top"
  bl_label = "FP_PointOnTheTop"

  @classmethod
  def poll(cls, context):
    return PointOnTheTop().poll(context)

  def execute(self, context):
    PointOnTheTop().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PointOnTheTop)

def unregister():
  bpy.utils.unregister_class(FP_PointOnTheTop)
