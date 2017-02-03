import bpy

from collections import OrderedDict


SIZE_TABLE_MAP = OrderedDict([
  ('Р', {'propName': 'grows', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Рост (Р)", min=0, max=300, default=168)}),
  ('ОГ', {'propName': 'chest_girth', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Обхват груди (ОГ)", min=0, max=500, default=92)}),
  ('ОТ', {'propName': 'waist_girth', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Обхват талии (ОТ)", min=0, max=500, default=76)}),
  ('ОБ', {'propName': 'hips_girth', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Обхват бедер (ОБ)", min=0, max=500, default=100)}),
  ('ОШ', {'propName': 'neck_girth', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Обхват шеи (ОШ)", min=0, max=500, default=36.6)}),
  ('ШШЗ', {'propName': 'width_neck_back', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Ширина шеи сзади (ШШЗ)", min=0, max=500, default=6.8)}),
  ('ВПРЗ', {'propName': 'armhole_height_back', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Высота проймы сзади (ВПРЗ)", min=0, max=500, default=20.5)}),
  ('ДТС', {'propName': 'length_back_to_waist', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Длина спины до талии (ДТС)", min=0, max=500, default=41.8)}),
  ('ВБ', {'propName': 'hips_height', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Высота бедер (ВБ)", min=0, max=500, default=62.6)}),
  ('ДЮ', {'propName': 'length_skirt', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Длина юбки (ДЮ)", min=0, max=500, default=61.5)}),
  ('ВГII', {'propName': 'height_chest_2', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Высота груди II (ВГII)", min=0, max=500, default=28.9)}),
  ('ДТПII', {'propName': 'length_waist_front_2', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Длина талии спереди II (ДТПII)", min=0, max=500, default=45.9)}),
  ('ШС', {'propName': 'back_width', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Ширина спины (ШС)", min=0, max=500, default=17)}),
  ('ШПР', {'propName': 'armhole_width', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Ширина проймы (ШПР)", min=0, max=500, default=10)}),
  ('ШГ', {'propName': 'chest_width', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Ширина груди (ШГ)", min=0, max=500, default=19)}),
  ('ШП', {'propName': 'width_shoulder_slope', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Ширина плечевого ската (ШП)", min=0, max=500, default=12.4)}),
  ('ДР', {'propName': 'length_sleeve', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Длина рукава (ДР)", min=0, max=500, default=60.2)}),
  ('ОП', {'propName': 'shoulder_girth', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Обхват плеча (ОП)", min=0, max=500, default=29.2)}),
  ('ОЗАП', {'propName': 'circumference_wrist', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Обхват запястья (ОЗАП)", min=0, max=500, default=16.2)}),
  ('ДСБ', {'propName': 'length_waist_floor_side', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Длина от талии до пола сбоку (ДСБ)", min=0, max=500, default=106)}),
  ('ВС', {'propName': 'seat_height', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Высота сиденья (ВС)", min=0, max=500, default=26.5)}),
  ('ДН', {'propName': 'leg_length', 'propValue': lambda update: bpy.props.IntProperty(update=update, name="Длина ноги (ДН)", min=0, max=500, default=79)}),
  ('ОЩ', {'propName': 'ankle_girth', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Обхват щиколотки (ОЩ)", min=0, max=500, default=25)}),
  ('ВК', {'propName': 'knee_height', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Высота колена (ВК)", min=0, max=500, default=31.8)}),
  ('ШЗ', {'propName': 'bottom_width', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Ширина низа (ШЗ)", min=0, max=500, default=42)}),
  ('ДИ', {'propName': 'product_length', 'propValue': lambda update: bpy.props.FloatProperty(update=update, name="Длина изделия (ДИ)", min=0, max=500, default=0)}),
])
