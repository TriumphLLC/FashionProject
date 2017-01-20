import bpy

from math import cos, sin, pi

from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.base import Base
from fashion_project.modules.utils.fp_angle import deg_to_radians

from fashion_project.modules.utils.intersections import elements_intersection

from fashion_project.modules.draw.counter import Counter

from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.curves.bezier_curve import BezierCurve
from fashion_project.modules.draw.arcs.arc import Arc

from fashion_project.modules.draw.arcs import is_one_of_arc
from fashion_project.modules.draw.curves import is_one_of_bezier_curve
from fashion_project.modules.draw.lines import is_one_of_lines


class PointFiguresIntersection(Base):
  FP_TYPE = 'fp.draw.points.point_figures_intersection'
  BASE_NAME = 'ТочкаПересеченияФигур'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)


  def poll(self, context):
    '''
        Нужны две выделенных фигуры.
    '''
    return (
      len(context.selected_objects) == 2
      and
      (
        (all(is_one_of_lines(item) for item in context.selected_objects))
        or
        (all(is_one_of_arc(item) for item in context.selected_objects))
        or
        (all(is_one_of_bezier_curve(item) for item in context.selected_objects))
        or
        ((is_one_of_lines(context.selected_objects[0]) and is_one_of_bezier_curve(context.selected_objects[1])) or (is_one_of_lines(context.selected_objects[1]) and is_one_of_bezier_curve(context.selected_objects[0])))
        or
        ((is_one_of_lines(context.selected_objects[0]) and is_one_of_arc(context.selected_objects[1])) or (is_one_of_lines(context.selected_objects[1]) and is_one_of_arc(context.selected_objects[0])))
        or
        ((is_one_of_arc(context.selected_objects[0]) and is_one_of_bezier_curve(context.selected_objects[1])) or (is_one_of_arc(context.selected_objects[1]) and is_one_of_bezier_curve(context.selected_objects[0])))
      )
    )

  def create(self, context):
    if all(is_one_of_arc(item) for item in context.selected_objects):
      count_create_point = 2
    elif all(is_one_of_bezier_curve(item) for item in context.selected_objects):
      count_create_point = 9
    elif all(is_one_of_lines(item) for item in context.selected_objects):
      count_create_point = 1
    elif ((is_one_of_lines(context.selected_objects[0]) and is_one_of_bezier_curve(context.selected_objects[1])) or (is_one_of_lines(context.selected_objects[1]) and is_one_of_bezier_curve(context.selected_objects[0]))):
      count_create_point = 3
    elif ((is_one_of_lines(context.selected_objects[0]) and is_one_of_arc(context.selected_objects[1])) or (is_one_of_lines(context.selected_objects[1]) and is_one_of_arc(context.selected_objects[0]))):
      count_create_point = 2
    elif ((is_one_of_arc(context.selected_objects[0]) and is_one_of_bezier_curve(context.selected_objects[1])) or (is_one_of_arc(context.selected_objects[1]) and is_one_of_bezier_curve(context.selected_objects[0]))):
      count_create_point = 6

    parents = [obj for obj in bpy.data.objects if obj.fp_id > 0 and (obj.fp_id == context.selected_objects[0].fp_id or obj.fp_id == context.selected_objects[1].fp_id)]
    dep_id = tuple([
                     parents[0].fp_id
                     ] + [
                     parents[1].fp_id
                     ] + [0])

    count = 0 
    while count < count_create_point:
      bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
      obj = context.object

      Counter.register(obj, self.FP_TYPE)
      obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

      obj.fp_deps = dep_id
      obj.fp_number = count

      obj.lock_location = (True, True, True)
      obj.show_name = True
      obj.select = False

      mat = bpy.data.materials.new('ЗаливкаТочкиПересеченияФигур')
      mat.diffuse_color = self.FILL_COLOR
      obj.data.materials.append(mat)

      count += 1

  def update(self, point_obj, context):
    for obj in bpy.data.objects:
     if obj.fp_id == point_obj.fp_deps[0]:
      element1 = obj
    for obj in bpy.data.objects:
     if obj.fp_id == point_obj.fp_deps[1]:
      element2 = obj
    intersection_point = elements_intersection(element1, element2)
    # print("intersection_point = ", intersection_point)
    point_obj.location = (intersection_point["points"][point_obj.fp_number]["x"], intersection_point["points"][point_obj.fp_number]["y"], 0)
