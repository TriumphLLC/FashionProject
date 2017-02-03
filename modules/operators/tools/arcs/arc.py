import bpy

from fashion_project.modules.draw.arcs.arc import Arc


class FP_Arc(bpy.types.Operator):
  '''
  Позволяет построить дугу.
  
  Требует выделенной точки.
  '''
  bl_idname = "fp.arc"
  bl_label = "FP_Arc"
  
  _arc = Arc()

  @classmethod
  def poll(cls, context):
    return cls._arc.poll(context)

  def execute(self, context):
    self._arc.create(context)
    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_Arc)

def unregister():
  bpy.utils.unregister_class(FP_Arc)
