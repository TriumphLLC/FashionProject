import bpy

from fashion_project.modules.draw.arcs.arc_separation import ArcSeparation

class FP_ArcSeparation(bpy.types.Operator):
  '''
  Позволяет построить точку на дуге

  Требует выделенной дуги.
  '''
  bl_idname = "fp.arc_separation"
  bl_label = "FP_ArcSeparation"

  _arc_separation = ArcSeparation()

  @classmethod
  def poll(cls, context):
    return cls._arc_separation.poll(context)

  def execute(self, context):
    self._arc_separation.create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ArcSeparation)

def unregister():
  bpy.utils.unregister_class(FP_ArcSeparation)