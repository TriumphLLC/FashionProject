import bpy

from fashion_project.modules.draw.curves.complex_curve import ComplexCurve


class FP_ComplexCurve(bpy.types.Operator):
  '''
  Позволяет построить сложную
  кривую, изменяемую 
  с помощью манипуляторов

  Требует более двух выделенных точек
  '''
  bl_idname = "fp.complex_curve"
  bl_label = "FP_ComplexCurve"
    
  @classmethod
  def poll(cls, context):
    return ComplexCurve().poll(context)

  def execute(self, context):
    ComplexCurve().create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_ComplexCurve)

def unregister():
  bpy.utils.unregister_class(FP_ComplexCurve)