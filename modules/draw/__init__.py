import bpy

from .points.point import Point
from .points.free_point import FreePoint
from .points.point_on_line import PointOnLine
from .points.point_for_dart import PointForDart
from .points.point_on_bisector import PointOnBisector
from .points.point_xy import PointXY
from .points.point_on_perpendicular import PointOnPerpendicular
from .points.line_intersection_and_circle import LineIntersectionAndCircle
from .points.point_figures_intersection import PointFiguresIntersection
from .points.point_intersection_line_axis import IntersectionLineAndAxis

from .points.point_on_the_top import PointOnTheTop
from .points.special_point_on_shoulder import SpecialPointOnShoulder
from .points.perpendicular_point_on_line import PerpendicularPointOnLine

from .lines.line import Line
from .lines.line_for_dart import LineForDart
from .lines.line_continuation import LineContinuation
from .lines.parallel_lines import ParallelLines
from .lines.reflection_horizontal_line import ReflectionHorizontalLine
from .lines.reflection_vertical_line import ReflectionVerticalLine
from .lines.dividing_line import DividingLine
from .lines.line_line_intersection import LineLineIntersection

from .arcs.arc import Arc
from .arcs.arc_separation import ArcSeparation
from .arcs.intersection_arc_and_axis import IntersectionArcAndAxis

from .circles.circle import Circle

from .detail_tool.detail_tool import ToolDetail

from .curves.bezier_curve import BezierCurve
from .curves.intersection_beziers_curve_and_axis import IntersectionBeziersCurveAndAxis
from .curves.complex_curve import ComplexCurve
from .curves.separation_beziers_curve import SeparationBeziersCurve
from .curves.separation_complex_curve import SeparationComplexCurve


def update(obj, context):
  draw_point = Point()
  draw_free_point = FreePoint()
  draw_point_on_line = PointOnLine()
  draw_point_for_dart = PointForDart()
  draw_point_on_bisector = PointOnBisector()
  draw_point_xy = PointXY()
  draw_point_on_perpendicular = PointOnPerpendicular()
  draw_point_intersection_line_axis = IntersectionLineAndAxis()
  draw_line_intersection_and_circle = LineIntersectionAndCircle()
  draw_point_on_the_top = PointOnTheTop()
  draw_special_point_on_shoulder = SpecialPointOnShoulder()
  draw_perpendicular_point_on_line = PerpendicularPointOnLine()
  draw_point_figures_intersection = PointFiguresIntersection()
  draw_line = Line()
  draw_line_for_dart = LineForDart()
  draw_line_continuation = LineContinuation()
  draw_line_line_intersection = LineLineIntersection()
  draw_parallel_lines = ParallelLines()
  draw_reflection_horizontal_Line = ReflectionHorizontalLine()
  draw_reflection_vertical_Line = ReflectionVerticalLine()
  draw_dividing_line = DividingLine()
  draw_arc = Arc()
  draw_detail = ToolDetail()
  draw_arc_separation = ArcSeparation()
  draw_circle = Circle()
  draw_bc = BezierCurve()
  draw_intersection_beziers_curve_and_axis = IntersectionBeziersCurveAndAxis()
  draw_complex_curve = ComplexCurve()
  draw_separation_bc = SeparationBeziersCurve()
  draw_separation_cc = SeparationComplexCurve()
  draw_intersection_arc_and_axis = IntersectionArcAndAxis()

  if hasattr(obj, 'fp_type'):
    if obj.fp_type == Point.FP_TYPE:
      draw_point.update(obj, context)
    elif obj.fp_type == Line.FP_TYPE:
      pass

  points = tuple(
    oth for oth in bpy.data.objects
    if oth.fp_type == Point.FP_TYPE
  )
  for point in points:
    draw_point.update(point, context)

  free_points = tuple(
    oth for oth in bpy.data.objects
    if oth.fp_type == FreePoint.FP_TYPE
  )
  for point in free_points:
    draw_free_point.update(point, context)

  for pfd in draw_point_for_dart.get_all():
    draw_point_for_dart.update(pfd, context)

  lines = tuple(
    ln for ln in bpy.data.objects
    if ln.fp_type == Line.FP_TYPE
  )
  for line in lines:
    draw_line.update(line, context)

  lines_for_dart = tuple(
    ln for ln in bpy.data.objects
    if ln.fp_type == LineForDart.FP_TYPE
  )
  for line in lines_for_dart:
    draw_line_for_dart.update(line, context)

  for arc in [
    oth for oth in bpy.data.objects
    if oth.fp_type == Arc.FP_TYPE
  ]:
    draw_arc.update(arc, context)

  for circle in [
    oth for oth in bpy.data.objects
    if oth.fp_type == Circle.FP_TYPE
    ]:
    draw_circle.update(circle, context)

  for bc in draw_bc.get_all():
    draw_bc.update(bc, context)

  for intersection_line_and_axis in draw_point_intersection_line_axis.get_all():
    draw_point_intersection_line_axis.update(intersection_line_and_axis)

  for intersection_beziers_curve_and_axis in draw_intersection_beziers_curve_and_axis.get_all():
    draw_intersection_beziers_curve_and_axis.update(intersection_beziers_curve_and_axis)

  for complex_curve in draw_complex_curve.get_all():
    draw_complex_curve.update(complex_curve, context)

  for pol in draw_point_on_line.get_all():
    draw_point_on_line.update(pol, context)

  for arc_separation in draw_arc_separation.get_all():
    draw_arc_separation.update(arc_separation, context)

  for pop in draw_point_on_perpendicular.get_all():
    draw_point_on_perpendicular.update(pop, context)

  for point_on_line_circle in draw_line_intersection_and_circle.get_all():
    draw_line_intersection_and_circle.update(point_on_line_circle, context)

  for point_on_arc_axis in draw_intersection_arc_and_axis.get_all():
    draw_intersection_arc_and_axis.update(point_on_arc_axis, context)

  for pob in draw_point_on_bisector.get_all():
    draw_point_on_bisector.update(pob, context)

  for pxy in draw_point_xy.get_all():
    draw_point_xy.update(pxy, context)

  for pot in draw_point_on_the_top.get_all():
    draw_point_on_the_top.update(pot, context)

  for pfi in draw_point_figures_intersection.get_all():
    draw_point_figures_intersection.update(pfi, context)

  for posh in draw_special_point_on_shoulder.get_all():
    draw_special_point_on_shoulder.update(posh, context)

  for dt in draw_detail.get_all():
    draw_detail.update(dt, context)

  for perpendicular_point_on_line in draw_perpendicular_point_on_line.get_all():
    draw_perpendicular_point_on_line.update(perpendicular_point_on_line, context)

  for line_continuation in draw_line_continuation.get_all():
    draw_line_continuation.update(line_continuation, context)

  for parallel_lines in draw_parallel_lines.get_all():
    draw_parallel_lines.update(parallel_lines, context)

  for reflection_horizontal_line in draw_reflection_horizontal_Line.get_all():
    draw_reflection_horizontal_Line.update(reflection_horizontal_line, context)

  for reflection_vertical_line in draw_reflection_vertical_Line.get_all():
    draw_reflection_vertical_Line.update(reflection_vertical_line, context)

  for line_line_intersection in draw_line_line_intersection.get_all():
    draw_line_line_intersection.update(line_line_intersection, context)

  for dividing_line in draw_dividing_line.get_all():
    draw_dividing_line.update(dividing_line, context)

  for separation_bc in draw_separation_bc.get_all():
    draw_separation_bc.update(separation_bc)

  for separation_cc in draw_separation_cc.get_all():
    draw_separation_cc.update(separation_cc)
