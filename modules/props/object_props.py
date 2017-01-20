import bpy

from fashion_project.modules.draw import update


class SceneSettingItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Test Prop", default="Unknown")
    value = bpy.props.StringProperty(name="Test Prop", default="0")

bpy.utils.register_class(SceneSettingItem)

def _set_props():
  bpy.types.Object.fp_type = bpy.props.StringProperty(
    name="Тип инструмента"
  )
  bpy.types.Object.fp_id = bpy.props.IntProperty(
    name="Идентификатор",
    default=0
  )
  bpy.types.Object.order = bpy.props.IntProperty(
    name="порядок",
    default=0
  )
  bpy.types.Object.hr = bpy.props.FloatVectorProperty(
    name="hr",
    default=(0.0,)*3,
    size=3
  )
  bpy.types.Object.hl = bpy.props.FloatVectorProperty(
    name="hl",
    default=(0.0,)*3,
    size=3
  )
  bpy.types.Object.end1 = bpy.props.FloatVectorProperty(
    name="end1",
    default=(0.0,)*3,
    size=3
  )
  bpy.types.Object.end2 = bpy.props.FloatVectorProperty(
    name="end2",
    default=(0.0,)*3,
    size=3
  )
  bpy.types.Object.co = bpy.props.FloatVectorProperty(
    name="co",
    default=(0.0,)*3,
    size=3
  )
  bpy.types.Object.fp_expression = bpy.props.StringProperty(
    name="Формула", 
    update=update
  )
  bpy.types.Object.fp_count = bpy.props.StringProperty(
    name="Количество точек разделения",
    update=update
  )
  bpy.types.Object.fp_number = bpy.props.IntProperty(
    name="Номер точки в списке точек разделения или в списке точек пересечения",
    update=update
  )
  bpy.types.Object.fp_angle = bpy.props.FloatProperty(
    name="Угол", 
    # min=0.0,
    # max=360.0,
    step=100,
    update=update
  )
  bpy.types.Object.fp_deps = bpy.props.IntVectorProperty(
    name="Зависимости",
    default=(0,)*3,
    size=3
  )
  bpy.types.Object.fp_deps30 = bpy.props.IntVectorProperty(
    name="Зависимости(30)",
    default=(0,)*30,
    size=30
  )
  bpy.types.Object.fp_dart = bpy.props.IntProperty(
    name="Идентификатор зависимой точки для выточки",
    default=0
  )
  bpy.types.Object.fp_coef_b = bpy.props.FloatProperty(
    name="Коэффициент B прямой", 
    default=0,
    update=update
  )
  bpy.types.Object.fp_line_length = bpy.props.FloatVectorProperty(
    name="Зависимости(29)",
    default=(0,)*29,
    size=29
  )

  

  bpy.types.Object.fp_deps_c = bpy.props.CollectionProperty(type=SceneSettingItem)
   


  bpy.types.Object.fp_angles = bpy.props.FloatVectorProperty(
    name="Углы",
    size=2,
    default=(0.0,0.0),
    update=update
  )


def register():
  _set_props()
  
def unregister():
  pass