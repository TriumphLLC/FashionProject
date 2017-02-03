import bpy


class FP_LineIntersectionPoint(bpy.types.Operator):
  '''
  Позволяет построить точку на 
  пересечении линии и оси, 
  проведенной через точку 
  '''
  bl_idname = "fp.line_intersection_point"
  bl_label = "FP_LineIntersectionPoint"
  
  @classmethod
  def poll(cls, context):
    '''
    Компонент в разработке.
    '''
    return (False)

  def execute(self, context):
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_LineIntersectionPoint)

def unregister():
  bpy.utils.unregister_class(FP_LineIntersectionPoint)
