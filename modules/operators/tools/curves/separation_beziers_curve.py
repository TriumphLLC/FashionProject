import bpy

from fashion_project.modules.draw.curves.separation_beziers_curve import SeparationBeziersCurve

class FP_SeparationBeziersCurve(bpy.types.Operator):
  '''
  Позволяет построит на кривой Безье
  точку на определённом расстоянии

  Требует выделенной кривой Безье
  '''
  bl_idname = "fp.separation_beziers_curve"
  bl_label = "FP_SeparationBeziersCurve"

  separation_bc = SeparationBeziersCurve()

  @classmethod
  def poll(cls, context):
    return cls.separation_bc.poll(context)

  def execute(self, context):
    self.separation_bc.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_SeparationBeziersCurve)

def unregister():
  bpy.utils.unregister_class(FP_SeparationBeziersCurve)