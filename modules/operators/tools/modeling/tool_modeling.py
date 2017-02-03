import bpy


class FP_ToolModeling(bpy.types.Operator):
  '''
  Позволяет делать копии замкнутой части конструкции 
  '''
  bl_idname = "fp.tool_modeling"
  bl_label = "FP_ToolModeling"

  def execute(self, context):
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ToolModeling)

def unregister():
  bpy.utils.unregister_class(FP_ToolModeling)