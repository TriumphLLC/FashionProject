import bpy

from fashion_project.modules.utils.mouse import set_event


class FP_StoreMouse(bpy.types.Operator):
  '''
  Оператор получения и хранения позиции мыши.
  '''
  bl_idname = 'fp.store_mouse'
  bl_label = 'FP_get_mouse'
  x = bpy.props.IntProperty()
  y = bpy.props.IntProperty()
  
  def invoke(self, context, event):
    set_event(event)
    return self.execute(context)
  
  def execute(self, context):
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_StoreMouse)

def unregister():
  bpy.utils.unregister_class(FP_StoreMouse)