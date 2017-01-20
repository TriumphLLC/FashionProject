import bpy

from fashion_project.modules.props.size_table import SIZE_TABLE_MAP


class FP_PanelSizeTable(bpy.types.Panel):
  '''
  Панель таблицы размеров
  '''
  bl_label = "Fashion Project Size Table"
  bl_space_type = "VIEW_3D"
  bl_region_type = "TOOLS" # UI | TOOLS
  bl_category = "Fashion Project"

  @classmethod
  def poll(cls, context):
    '''
    Если есть выделенный объект - показываем панель.
    '''
    return (context.active_object is not None and context.active_object.fp_id > 0)

  def draw(self, context):
    layout = self.layout

    row = layout.row()
    row.label(text="Таблица размеров")

    for size in SIZE_TABLE_MAP.values():
      row = layout.row()
      row.prop(context.scene.fp_size_table, size['propName'])


def register():
  bpy.utils.register_class(FP_PanelSizeTable)

def unregister():
  bpy.utils.unregister_class(FP_PanelSizeTable)
