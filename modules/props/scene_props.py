import bpy

from fashion_project.modules.draw import update
from .size_table import SIZE_TABLE_MAP


class FP_SizeTable(bpy.types.PropertyGroup):
  pass
  
class FP_DevSettings(bpy.types.PropertyGroup):
  expression_precision = bpy.props.IntProperty(default=2, name="Округление формулы")
  coords_precision = bpy.props.IntProperty(default=2, name="Округление координат")

def _render_scene_props(scene, context):
  pass

def set_scene_props():
  global SIZE_TABLE_MAP
  for v in SIZE_TABLE_MAP.values():
    setattr(FP_SizeTable, v['propName'], v['propValue'](update))
  bpy.utils.register_class(FP_SizeTable)
  bpy.utils.register_class(FP_DevSettings)
  bpy.types.Scene.fp_size_table = bpy.props.PointerProperty(type=FP_SizeTable)
  bpy.types.Scene.fp_dev = bpy.props.PointerProperty(type=FP_DevSettings)


def register():
  set_scene_props()

def unregister():
  pass