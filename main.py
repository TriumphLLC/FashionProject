import bpy

# Панели
from fashion_project.modules.ui.panels import panel_tools
from fashion_project.modules.ui.panels import panel_tools_settings
from fashion_project.modules.ui.panels import panel_size_table

# Операторы добавления точек
from fashion_project.modules.operators.tools.points import point
from fashion_project.modules.operators.tools.points import free_point
from fashion_project.modules.operators.tools.points import point_for_dart
from fashion_project.modules.operators.tools.points import point_on_line
from fashion_project.modules.operators.tools.points import point_on_perpendicular
from fashion_project.modules.operators.tools.points import point_on_bisector
from fashion_project.modules.operators.tools.points import point_xy
from fashion_project.modules.operators.tools.points import perpendicular_point_on_line
from fashion_project.modules.operators.tools.points import line_intersection_point
from fashion_project.modules.operators.tools.points import special_point_on_shoulder
from fashion_project.modules.operators.tools.points import point_on_the_top
from fashion_project.modules.operators.tools.points import line_intersection_and_circle
from fashion_project.modules.operators.tools.points import point_figures_intersection
from fashion_project.modules.operators.tools.points import point_free
from fashion_project.modules.operators.tools.points import point_intersection_line_axis

# Операторы добавления линий
from fashion_project.modules.operators.tools.lines import line
from fashion_project.modules.operators.tools.lines import line_for_dart
from fashion_project.modules.operators.tools.lines import line_line_intersection
from fashion_project.modules.operators.tools.lines import parallel_lines
from fashion_project.modules.operators.tools.lines import reflection_horizontal_line
from fashion_project.modules.operators.tools.lines import reflection_vertical_line
from fashion_project.modules.operators.tools.lines import dividing_line
from fashion_project.modules.operators.tools.lines import line_continuation

# Операторы добавления произвольных кривых
from fashion_project.modules.operators.tools.curves import beziers_curve
from fashion_project.modules.operators.tools.curves import complex_curve
from fashion_project.modules.operators.tools.curves import separation_beziers_curve
from fashion_project.modules.operators.tools.curves import separation_complex_curve
from fashion_project.modules.operators.tools.curves import intersection_beziers_curve_and_axis

# Операторы добавления круговых кривых
from fashion_project.modules.operators.tools.arcs import arc
from fashion_project.modules.operators.tools.arcs import arc_separation
from fashion_project.modules.operators.tools.arcs import intersection_arc_and_axis

# Операторы добавления окружности
from fashion_project.modules.operators.tools.circles import circle

# Специальные операторы
from fashion_project.modules.operators.tools.modeling import tool_modeling
from fashion_project.modules.operators.tools.detail import tool_detail
# from fashion_project.modules.operators.tools.details_mode import details_mode
from fashion_project.modules.operators.tools.export_svg import export_svg

from fashion_project.modules.operators.tools.detail_tool import detail_tool

from fashion_project.modules.operators.tools.details import copying
from fashion_project.modules.operators.tools.details import moving
from fashion_project.modules.operators.tools.details import modeling

# Инструмент таблица размеров ???
from fashion_project.modules.operators.tools.size_table import size_table

# Создаем переменные таблицы размеров, присваивая кастомные свойства сцене
from fashion_project.modules.props import scene_props

# Кастомные данные для объектов - устанавливаем тип инструмента, которым создан объект
# from fashion_project.modules.props import common_props

# Кастомные данные для точки - длина и угол
from fashion_project.modules.props import object_props

# Модуль фиксирования 2д-окна
from fashion_project.modules.ui.handlers import view_2d

# Модуль отслеживания удаления объектов
from fashion_project.modules.handlers import watch_delete

from fashion_project.modules.handlers import watch_active
from fashion_project.modules.handlers import watch_active_handlers

from fashion_project.modules.operators.wires import basic as basic_wire
# from fashion_project.modules.operators.wires.between_points import FP_BetweenPointsWire

from fashion_project.modules.operators.utils import mouse as mouse_op

from fashion_project.modules.operators.contours import highlight as contour_highlight
from fashion_project.modules.operators.tools.lines import change_type_line

from fashion_project.modules.operators.utils import toggle_names


'''
Модули, у которых должны быть методы register и unregister,
для реализации логики регистрации в самих модулях.
Необходимость логики регистрации нужна для единого интерфейса
регистрации классов, определения макро и добавления хендлеров
'''
mdls = [
  scene_props,
  object_props,

  panel_tools,
  panel_tools_settings,
  panel_size_table,

  # POINTS
  point,
  free_point,
  point_for_dart,
  point_on_line,
  point_on_perpendicular,
  point_on_bisector,
  point_xy,
  perpendicular_point_on_line,
  line_intersection_point,
  special_point_on_shoulder,
  point_on_the_top,
  line_intersection_and_circle,
  point_figures_intersection,
  point_free,
  point_intersection_line_axis,

  # LINES
  line,
  line_for_dart,
  line_line_intersection,
  parallel_lines,
  reflection_horizontal_line,
  reflection_vertical_line,
  dividing_line,
  line_continuation,

  # CURVES
  beziers_curve,
  complex_curve,
  separation_beziers_curve,
  separation_complex_curve,
  intersection_beziers_curve_and_axis,

  # ARC
  arc,
  arc_separation,
  intersection_arc_and_axis,

  # CIRCLE
  circle,

  # TOOL MODELING, DETAIL
  tool_modeling,
  tool_detail,
  # details_mode,
  export_svg,

  detail_tool,

  copying,
  moving,
  modeling,

  # SIZE TABLE
  size_table,

  # HANDLERS
  view_2d,
  watch_delete,
  watch_active,
  watch_active_handlers,

  basic_wire,

  mouse_op,

  contour_highlight,
  change_type_line,

  toggle_names,

]

#delete panel left and right
# for pt in bpy.types.Panel.__subclasses__():
#   if pt.bl_space_type == 'VIEW_3D':
#     if "bl_rna" in pt.__dict__:
#       bpy.utils.unregister_class(pt) 


def register():
  '''
  Регистрация модулей.
  '''
  for m in mdls:
    if hasattr(m, 'register') and callable(m.register):
      m.register()
    else:
      raise Exception('модуль не имеет метода регистрации')

def unregister():
  '''
  Отмена регистрации модулей.
  '''
  for m in mdls:
    if hasattr(m, 'unregister') and callable(m.unregister):
      m.unregister()
    else:
      raise Exception('модуль не имеет метода отмены регистрации')
