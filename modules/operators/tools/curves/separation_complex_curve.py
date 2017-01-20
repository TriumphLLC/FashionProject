import bpy

from fashion_project.modules.draw.curves.separation_complex_curve import SeparationComplexCurve

class FP_SeparationComplexCurve(bpy.types.Operator):
  '''
  Позволяет построит на сложной кривой
  точку на определённом расстоянии

  Требует выделенной сложной кривой
  '''
  bl_idname = "fp.separation_complex_curve"
  bl_label = "FP_SeparationComplexCurve"

  separation_cc = SeparationComplexCurve()

  @classmethod
  def poll(cls, context):
    return cls.separation_cc.poll(context)

  def execute(self, context):
    self.separation_cc.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_SeparationComplexCurve)

def unregister():
  bpy.utils.unregister_class(FP_SeparationComplexCurve)