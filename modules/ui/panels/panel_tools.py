import bpy
import os
import bpy.utils.previews

from fashion_project.modules.operators.tools.details.copying import is_modeling
from fashion_project.modules.operators.tools.details.moving import is_moving

from fashion_project.modules.operators.tools.points.point_free import FP_PointFreeWired

PREVIEW_COLLECTIONS = {}

class FP_PanelTools(bpy.types.Panel):
  '''
  Панель инструментов редактора лекал
  '''
  bl_label = "Fashion Project Tools"
  bl_space_type = "VIEW_3D"
  bl_region_type = "TOOLS" # UI | TOOLS
  bl_category = "Fashion Project"
  

  def draw(self, context):
    layout = self.layout

    ####################### BOX POINTS #######################
    boxPoints = layout.box()
    boxPoints.label(text="Инструменты построения точек")

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    this_icon = PREVIEW_COLLECTIONS["fp.point"]["fp.point"].icon_id
    row.operator("fp.point", text="Точка", icon_value=this_icon)
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    # row.operator("fp.point_on_line", text="Точка на линии")
    row.operator("fp_point_on_line_wire", text="Точка на линии", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp_point_for_dart_wire", text="Точка для вытачки", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.point_on_perpendicular", text="Точка на перпендикуляре", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.point_on_bisector", text="Точка на биссектрисе", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.point_xy", text="Точка из двух X и Y", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.perpendicular_point_on_line", text="Перпендикулярная точка на линии", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line_intersection_point", text="Точка пересечения линии и оси", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.special_point_on_shoulder", text="Специальная точка на плече", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.point_on_the_top", text="Точка на вершине прямоугольного треугольника", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line_intersection_and_circle", text="Пересечение линии и окружности", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.point_figures_intersection", text="Точка пересечения фигур", icon="MESH_DATA")
    row.separator()

    row = boxPoints.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp_intersection_line_and_axis_wire", text="Точка пересечения линии и оси", icon="MESH_DATA")
    row.separator()


    ######################## BOX LINES ########################
    boxLines = layout.box()
    boxLines.label(text="Инструменты построения линий")

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line", text="Линия", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line_for_dart", text="Линия для вытачки", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line_line_intersection", text="Пересечение линий", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.parallel_lines", text="Параллельные линии", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.reflection_horizontal_line", text="Горизонтальное отражение линии", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.reflection_vertical_line", text="Вертикальное отражение линии", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.dividing_line", text="Разделение линии", icon="MESH_DATA")
    row.separator()

    row = boxLines.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.line_continuation", text="Продолжение линии", icon="MESH_DATA")
    row.separator()

    ######################## BOX CURVES ########################
    boxCurves = layout.box()
    boxCurves.label(text="Инструменты построения кривых")

    row = boxCurves.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.beziers_curve", text="Кривая Безье", icon="MESH_DATA")
    row.separator()

    row = boxCurves.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.separation_beziers_curve", text="Разделение кривой Безье", icon="MESH_DATA")
    row.separator()

    row = boxCurves.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.complex_curve", text="Сложная кривая", icon="MESH_DATA")
    row.separator()

    row = boxCurves.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.separation_complex_curve", text="Разделение сложной кривой", icon="MESH_DATA")
    row.separator()

    row = boxCurves.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp_intersection_beziers_curve_and_axis_wire", text="Пересечение кривой Безье и оси", icon="MESH_DATA")
    row.separator()


    ######################## Detail Tool ########################
    boxDetail = layout.box()
    boxDetail.label(text="Инструмент деталь")

    row = boxDetail.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.tool_detail", text="Инструмент деталь", icon="MESH_DATA")
    row.separator()


    ######################## BOX ARCS ########################
    boxArcs = layout.box()
    boxArcs.label(text="Инструменты построения дуг")

    row = boxArcs.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.arc", text="Дуга", icon="MESH_DATA")
    row.separator()

    row = boxArcs.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp.arc_separation", text="Разделение дуги", icon="MESH_DATA")
    row.separator()

    row = boxArcs.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("fp_intersection_arc_and_axis_wire", text="Пересечение дуги и оси", icon="MESH_DATA")
    row.separator()

    ''' Моделирование '''
    box = layout.box()
    box.label(text="Моделирование")

    row = box.row(align=True)
    row.alignment = 'EXPAND'
    row.operator('fp.contour_highlight', text='Выбрать контур', icon="MESH_DATA")
    row.operator('fp.copying_contour_target', text='Копировать', icon="MESH_DATA")
    row.operator('fp.moving_contour_target', text='Переместить', icon="MESH_DATA")
    row.separator()

    row = box.row(align=True)
    row.alignment = 'EXPAND'
    row.operator('fp_modal_modeling', text='Моделирование', icon="MESH_DATA")
    # row.operator('fp.draw_update_contour', text='Моделирование', icon="MESH_DATA")
    row.separator()

    ''' Разработка '''
    box = layout.box()
    box.label(text="Разработка")
    row = box.row(align=True)
    row.alignment = "EXPAND"
    row.operator("fp.point_free_wired", text="Свободная точка", icon="MESH_DATA")
    row.prop(context.scene.fp_dev, "expression_precision", text="Окр. формулы")
    row.prop(context.scene.fp_dev, "coords_precision", text="Окр. координат")
    row.separator()
    row = box.row(align=True)
    row.alignment = "EXPAND"
    row.operator("fp.show_names", text="Показать названия", icon="MESH_DATA")
    row.operator("fp.toggle_names_selected", text="Показать выделенные", icon="MESH_DATA")
    row.operator("fp.hide_names", text="Скрыть названия", icon="MESH_DATA")


def register():
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    pcoll.load("fp.point", os.path.join(icons_dir, "fp.point.png"), 'IMAGE')
    PREVIEW_COLLECTIONS["fp.point"] = pcoll
    bpy.utils.register_class(FP_PanelTools)

def unregister():
    bpy.utils.unregister_class(FP_PanelTools)
