import bpy

from fashion_project.modules.draw.curves.bezier_curve import BezierCurve


class FP_BeziersCurve(bpy.types.Operator):
  '''
  Позволяет построить стандартную
  кривую кубическую Безье, изменяемую с помощью манипуляторов
  Требует двух выделенных точек
  '''
  bl_idname = "fp.beziers_curve"
  bl_label = "FP_BeziersCurve"
  
  _bc = BezierCurve()
    
  @classmethod
  def poll(cls, context):
    return cls._bc.poll(context)

  def execute(self, context):
    self._bc.create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_BeziersCurve)

def unregister():
  bpy.utils.unregister_class(FP_BeziersCurve)