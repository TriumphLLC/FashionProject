import bpy


def _get_all_fp_objects():
  return tuple(obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_type)


class FP_ToggleNames(bpy.types.Operator):
  bl_idname = "fp.toggle_names"
  bl_label = "FP Toggle Names"
  
  def execute(self, context):
    show = False
    fp_objects = _get_all_fp_objects()
    if any(not obj.show_name for obj in fp_objects):
      show = True
    for obj in fp_objects:
      obj.show_name = show
    return {'FINISHED'}


class FP_HideNames(bpy.types.Operator):
  bl_idname = "fp.hide_names"
  bl_label = "FP Hide Names"

  def execute(self, context):
    for obj in _get_all_fp_objects():
      obj.show_name = False
    return {"FINISHED"}


class FP_ShowNames(bpy.types.Operator):
  bl_idname = "fp.show_names"
  bl_label = "FP Show Names"

  def execute(self, context):
    for obj in _get_all_fp_objects():
      obj.show_name = True
    return {"FINISHED"}


class FP_ShowNamesSelected(bpy.types.Operator):
  bl_idname = "fp.show_names_selected"
  bl_label = "FP Show Names Selected"

  def execute(self, context):
    for obj in _get_all_fp_objects():
      if obj in context.selected_objects:
        obj.show_name = True
    return {"FINISHED"}


class FP_ShowNamesSelected(bpy.types.Operator):
  bl_idname = "fp.show_names_selected"
  bl_label = "FP Show Names Selected"

  def execute(self, context):
    for obj in _get_all_fp_objects():
      if obj in context.selected_objects:
        obj.show_name = True
    return {"FINISHED"}


class FP_ToggleNamesSelected(bpy.types.Operator):
  bl_idname = "fp.toggle_names_selected"
  bl_label = "FP Toggle Names Selected"

  def execute(self, context):
    for obj in _get_all_fp_objects():
      if obj in context.selected_objects:
        obj.show_name = not obj.show_name
    return {"FINISHED"}


clss = [
  FP_ToggleNames,
  FP_HideNames,
  FP_ShowNames,
  FP_ShowNamesSelected,
  FP_ToggleNamesSelected,
]


def register():
  for cls in clss:
    bpy.utils.register_class(cls)
  
def unregister():
  for cls in clss:
    bpy.utils.unregister_class(cls)
