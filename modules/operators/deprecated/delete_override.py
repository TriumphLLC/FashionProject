'''
@deprecated
'''

import bpy


class FPDeleteOverride(bpy.types.Operator):
  bl_idname = 'object.delete'
  bl_label = 'Object Delete Operator'

  @classmethod
  def poll(cls, context):
    return context.active_object is not None

  def execute(self, context):
    global orig
    for obj in context.selected_objects:
      if not obj.fp_type == 'fp.tools.points.point':
        bpy.context.scene.objects.unlink(obj)
        bpy.data.objects.remove(obj)
    return {'FINISHED'}