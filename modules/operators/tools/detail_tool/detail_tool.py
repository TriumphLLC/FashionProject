import bpy

from fashion_project.modules.draw.detail_tool.detail_tool import ToolDetail

class FP_DetailTool(bpy.types.Operator):
  '''
  Инструмент деталь:
  создает замкнутый контур
  '''
  bl_idname = "fp.detail_tool"
  bl_label = "FP_DetailTool"

  @classmethod
  def poll(cls, context):
    return ToolDetail().poll(context)
  
  def execute(self, context):
    ToolDetail().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_DetailTool)

def unregister():
  bpy.utils.unregister_class(FP_DetailTool)