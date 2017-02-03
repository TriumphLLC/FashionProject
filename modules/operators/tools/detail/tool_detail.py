import bpy

from fashion_project.modules.draw.detail_tool.detail_tool import ToolDetail

class FP_ToolDetail(bpy.types.Operator):
  '''
    Позволяет получить деталь из чертежа конструкции 
  '''
  bl_idname = "fp.tool_detail"
  bl_label = "FP_ToolDetail"

  _td = ToolDetail()
    
  @classmethod
  def poll(cls, context):
    return cls._td.poll(context)

  def execute(self, context):
    self._td.create(context)
    return {'FINISHED'}	

def register():
  bpy.utils.register_class(FP_ToolDetail)

def unregister():
  bpy.utils.unregister_class(FP_ToolDetail)