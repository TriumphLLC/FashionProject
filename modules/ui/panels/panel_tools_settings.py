import bpy

from math import pi

from fashion_project.modules.utils.fp_expression import expression_to_value

from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.lines import is_one_of_points_lines
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.points.point_on_line import PointOnLine
from fashion_project.modules.draw.points.point_for_dart import PointForDart
from fashion_project.modules.draw.points.point_on_bisector import PointOnBisector
from fashion_project.modules.draw.points.point_xy import PointXY
from fashion_project.modules.draw.points.point_on_perpendicular import PointOnPerpendicular
from fashion_project.modules.draw.points.special_point_on_shoulder import SpecialPointOnShoulder
from fashion_project.modules.draw.points.perpendicular_point_on_line import PerpendicularPointOnLine
from fashion_project.modules.draw.points.point_figures_intersection import PointFiguresIntersection
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.lines.line_for_dart import LineForDart
from fashion_project.modules.draw.lines.line_continuation import LineContinuation
from fashion_project.modules.draw.lines.reflection_horizontal_line import ReflectionHorizontalLine
from fashion_project.modules.draw.lines.reflection_vertical_line import ReflectionVerticalLine
from fashion_project.modules.draw.lines.dividing_line import DividingLine
from fashion_project.modules.draw.lines.parallel_lines import ParallelLines
from fashion_project.modules.draw.arcs.arc import Arc
from fashion_project.modules.draw.arcs.arc_separation import ArcSeparation
from fashion_project.modules.draw.curves.separation_beziers_curve import SeparationBeziersCurve
from fashion_project.modules.draw.curves.separation_complex_curve import SeparationComplexCurve
from fashion_project.modules.draw.curves.intersection_beziers_curve_and_axis import IntersectionBeziersCurveAndAxis

from fashion_project.modules.draw.circles.circle import Circle
from fashion_project.modules.draw.points.line_intersection_and_circle import LineIntersectionAndCircle

from fashion_project.modules.draw.detail_tool.detail_tool import ToolDetail

from fashion_project.modules.operators.tools.details.copying import is_modeling

from fashion_project.modules.draw.lines import get_line_length
from fashion_project.modules.utils.contours import get_contours

from fashion_project.modules.operators.contours.highlight import get_current_index as contour_highlight_index


class FP_PanelToolsSettings(bpy.types.Panel):
  '''
  Панель настройки инструментов
  '''
  bl_label = "Fashion Project Tools Settings"
  bl_space_type = "VIEW_3D"
  bl_region_type = "TOOLS"
  bl_category = "Fashion Project"

  @classmethod
  def poll(cls, context):
    '''
    Если есть выделенный объект - показываем панель.
    '''
    return (
      context.active_object is not None
      and
      context.active_object.fp_id > 0
    )

  def draw(self, context):
    layout = self.layout
    if is_modeling():
      self.bl_label = 'Моделирование'
      row = layout.row()
      row.operator('fp.copying_stop', text='Готово')
      return
    self.bl_label = context.active_object.name + ' (' + context.active_object.fp_type + ')'
    row = layout.row()
    if context.active_object.fp_type == Point.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
      row = layout.row()
      row.label(text = "Значение:")
      row.alignment = 'LEFT'
      row.label(text = str(expression_to_value(context.active_object.fp_expression)))
      row = layout.row()
      row.prop(context.active_object, "fp_angle")
      # row = layout.row()
      # row.alignment = 'EXPAND'
      # props = row.operator('fp.draw_wire_between_points', text='Тестовая направляющая')
      # props.color3f = (0.8, 0.8, 0.2)
      # props.alpha = 0.75
      # props.line_width = 3
      # props.point_radius = 5
      # props.poly = 4
      # props.angle_ammend = pi/4
    elif context.active_object.fp_type == PointOnLine.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == PointForDart.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
      row = layout.row()
      row.prop(context.active_object, "fp_angle")
    elif context.active_object.fp_type == PointOnPerpendicular.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == PointOnBisector.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == LineContinuation.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == PointXY.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == PointFiguresIntersection.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == PerpendicularPointOnLine.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == ParallelLines.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == ReflectionHorizontalLine.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == ReflectionVerticalLine.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == DividingLine.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == IntersectionBeziersCurveAndAxis.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_angle")
    elif context.active_object.fp_type == SpecialPointOnShoulder.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == Arc.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
      row = layout.row()
      row.prop(context.active_object, "fp_angles")
    elif context.active_object.fp_type == Circle.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == LineIntersectionAndCircle.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == ArcSeparation.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == SeparationBeziersCurve.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == SeparationComplexCurve.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_expression")
    elif context.active_object.fp_type == ToolDetail.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
    elif context.active_object.fp_type == LineForDart.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_count")
      row = layout.row()
      row.label(text = "Длина:")
      row.alignment = "LEFT"
      row.label(text = str(get_line_length(context.active_object)))
      row = layout.row()
      row.label(text = "Количество контуров:")
      row.alignment = "LEFT"
      contours = get_contours(context.active_object)
      row.label(text = str(len(contours)))
      row = layout.row()
      _props = row.operator("fp.contour_highlight", text="Выбрать контур ({0}/{1})".format(contour_highlight_index() + 1, len(contours)))
      row = layout.row()
      row.operator("fp.change_type_line", text="Сменить тип линии")
    elif context.active_object.fp_type == Line.FP_TYPE:
      row.prop(context.active_object, "name", text="Название")
      row = layout.row()
      row.prop(context.active_object, "fp_count")
      row = layout.row()
      row.label(text = "Длина:")
      row.alignment = "LEFT"
      row.label(text = str(get_line_length(context.active_object)))
      row = layout.row()
      row.label(text = "Количество контуров:")
      row.alignment = "LEFT"
      contours = get_contours(context.active_object)
      row.label(text = str(len(contours)))
      row = layout.row()
      _props = row.operator("fp.contour_highlight", text="Выбрать контур ({0}/{1})".format(contour_highlight_index() + 1, len(contours)))
      row = layout.row()
      row.operator("fp.change_type_line", text="Сменить тип линии")


def register():
  bpy.utils.register_class(FP_PanelToolsSettings)

def unregister():
  bpy.utils.unregister_class(FP_PanelToolsSettings)
