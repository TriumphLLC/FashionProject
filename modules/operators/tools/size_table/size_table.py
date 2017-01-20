import bpy


class FP_SizeTable(bpy.types.Operator):
  '''
  Список всех размеров 
  '''
  bl_idname = "fp.sizetable"
  bl_label = "FP_SizeTable"

  def execute(self, context):
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_SizeTable)

def unregister():
  bpy.utils.unregister_class(FP_SizeTable)