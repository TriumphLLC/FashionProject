import bpy


class FP_ExportSVG(bpy.types.Operator):
  '''
  Экспорт конструкции в формате SVG
  '''
  bl_idname = "fp.export_svg"
  bl_label = "FP_ExportSVG"

  def execute(self, context):
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_ExportSVG)

def unregister():
  bpy.utils.unregister_class(FP_ExportSVG)