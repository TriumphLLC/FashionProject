import bpy

from fashion_project.modules.draw.lines import is_one_of_lines
from fashion_project.modules.draw.lines.line_for_dart import LineForDart
from fashion_project.modules.draw.lines.line import Line

class FP_ChangeTypeLine(bpy.types.Operator):
  bl_idname = "fp.change_type_line"
  bl_label = "Change Type Line"

  TYPE_LINE_COLOR = (0, 0.6, 0.4)
  TYPE_LINE_FOR_DART_COLOR = (0, 0.3, 0.7)
  
  @classmethod
  def poll(cls, context):
    return (
      context.active_object.fp_type == Line.FP_TYPE
      or context.active_object.fp_type == LineForDart.FP_TYPE
    )
    
  def execute(self, context):
    line_mat = bpy.data.materials.new('ОбводкаЛинии')
    if context.active_object.fp_type == LineForDart.FP_TYPE:
      line_mat.diffuse_color = self.TYPE_LINE_COLOR
      context.active_object.data.materials[0] = line_mat 
      context.active_object.fp_type = Line.FP_TYPE
    else:
      line_mat.diffuse_color = self.TYPE_LINE_FOR_DART_COLOR
      context.active_object.data.materials[0] = line_mat
      context.active_object.fp_type = LineForDart.FP_TYPE

    return {'FINISHED'}


def register():
  bpy.utils.register_class(FP_ChangeTypeLine)

def unregister():
  bpy.utils.unregister_class(FP_ChangeTypeLine)
