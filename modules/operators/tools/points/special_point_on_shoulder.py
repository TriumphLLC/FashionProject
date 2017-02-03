import bpy
from fashion_project.modules.draw.points.special_point_on_shoulder import SpecialPointOnShoulder


class FP_SpecialPointOnShoulder(bpy.types.Operator):
    '''
       Позволяет построить специальную точку на плече
    '''
    bl_idname = "fp.special_point_on_shoulder"
    bl_label = "FP_SpecialPointOnShoulder"

    @classmethod
    def poll(cls, context):
        return SpecialPointOnShoulder().poll(context)

    def execute(self, context):
        SpecialPointOnShoulder().create(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FP_SpecialPointOnShoulder)


def unregister():
    bpy.utils.unregister_class(FP_SpecialPointOnShoulder)
