import bpy

from math import sqrt, cos, sin

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.draw.points import is_one_of_points, get_angle
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.utils.mathlib import get_distance
from fashion_project.modules.utils.fp_angle import deg_to_radians

from fashion_project.modules.utils.fp_expression import expression_to_value


class PointForDart(Base):
  FP_TYPE = 'fp.draw.points.point_for_dart'
  DEFAULT_EXPRESSION = '1.1'
  BASE_NAME = 'ТочкаДляВытачки'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.3, 0.7)

  def poll(self, context):
    '''
    Нужны две выделенных точки,
    одна из которых является активной.
    '''
    return (
      context.active_object
      and is_one_of_points(context.active_object)
      and len(context.selected_objects) == 2
      and all(is_one_of_points(obj) for obj in context.selected_objects)
    )

  def create(self, context):
    parent = context.active_object
    dep_id = tuple([
      d.fp_id for d in context.selected_objects
      if not d.fp_id == parent.fp_id
    ] + [0, 0])
    dep = [d for d in context.selected_objects if not d.fp_id == parent.fp_id]
    distance = get_distance(get_point_abs_location(context.selected_objects[0]), get_point_abs_location(context.selected_objects[1]))
    
    bpy.ops.mesh.primitive_plane_add(radius = self.POINT_RADIUS)
    obj = context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.parent = parent

    obj.fp_deps = dep_id

    obj.fp_expression = self.DEFAULT_EXPRESSION

    obj.lock_location = (True, True, True)
    obj.show_name = True
    # obj.select = False
    id_dart = obj.fp_id

    p_a_location = get_point_abs_location(obj.parent)
    d_a_location = get_point_abs_location([
      d for d in bpy.data.objects
      if d.fp_id == obj.fp_deps[0] and d.fp_id > 0
    ][0])
    pd_dif = (
      p_a_location[0] - d_a_location[0],
      p_a_location[1] - d_a_location[1],
      0.0
    )
    pd_hyp = sqrt(pd_dif[0]**2 + pd_dif[1]**2)
    op_hyp = expression_to_value(obj.fp_expression)
    proportion = op_hyp/pd_hyp if pd_hyp else 0
    op_x = pd_dif[0] * proportion
    op_y = pd_dif[1] * proportion
    obj.location = (-op_x, -op_y, 0.0)

    print("parent 1 = ", obj.parent)
    obj.fp_angle = get_angle(get_point_abs_location(obj), get_point_abs_location(dep[0]))
    
    draw_line = Line()
    parent.select = True
    draw_line.create(context)

    mat = bpy.data.materials.new('ЗаливкаТочкиДляВытачки')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)




    bpy.ops.mesh.primitive_plane_add(radius = self.POINT_RADIUS)
    obj = context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.parent = dep[0]

    obj.fp_deps = tuple([parent.fp_id] + [0, 0])

    obj.fp_expression = str(distance - expression_to_value(self.DEFAULT_EXPRESSION))

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.fp_dart = id_dart
    # obj.select = False

    p_a_location = get_point_abs_location(obj.parent)
    d_a_location = get_point_abs_location([
      d for d in bpy.data.objects
      if d.fp_id == obj.fp_deps[0] and d.fp_id > 0
    ][0])
    pd_dif = (
      p_a_location[0] - d_a_location[0],
      p_a_location[1] - d_a_location[1],
      0.0
    )
    pd_hyp = sqrt(pd_dif[0]**2 + pd_dif[1]**2)
    op_hyp = expression_to_value(obj.fp_expression)
    proportion = op_hyp/pd_hyp if pd_hyp else 0
    op_x = pd_dif[0] * proportion
    op_y = pd_dif[1] * proportion
    obj.location = (-op_x, -op_y, 0.0)
    
    print("parent 2 = ", obj.parent)
    obj.fp_angle = get_angle(get_point_abs_location(obj), get_point_abs_location(parent))

    draw_line = Line()
    dep[0].select = True
    draw_line.create(context)

    mat = bpy.data.materials.new('ЗаливкаТочкиДляВытачки')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

    for obj in bpy.data.objects:
      obj.select = False

    for line in bpy.data.objects:
      if line.fp_type == Line.FP_TYPE and ((line.fp_deps[0] == parent.fp_id and line.fp_deps[1] == dep[0].fp_id) or (line.fp_deps[0] == dep[0].fp_id and line.fp_deps[1] == parent.fp_id)):
        line.select = True
        bpy.ops.object.delete()
        break


  def update(self, obj, context):
    points = self.get_all()
    obj.location = points[-1].location if len(points) > 1 else (0.0,0.0,0.0)
    
    line = expression_to_value(obj.fp_expression)

    radians = deg_to_radians(obj.fp_angle)
    
    prevLocation = (0.0,0.0,0.0)
    
    line_x = prevLocation[0] + (cos(radians) * line)
    line_y = prevLocation[1] + (sin(radians) * line)

    obj.location = (line_x, line_y, 0.0)

    # p_a_location = get_point_abs_location(obj.parent)
    # d_a_location = get_point_abs_location([
    #   d for d in bpy.data.objects
    #   if d.fp_id == obj.fp_deps[0] and d.fp_id > 0
    # ][0])
    # pd_dif = (
    #   p_a_location[0] - d_a_location[0],
    #   p_a_location[1] - d_a_location[1],
    #   0.0
    # )
    # pd_hyp = sqrt(pd_dif[0]**2 + pd_dif[1]**2)
    # op_hyp = expression_to_value(obj.fp_expression)
    # proportion = op_hyp/pd_hyp if pd_hyp else 0
    # op_x = pd_dif[0] * proportion
    # op_y = pd_dif[1] * proportion
    # obj.location = (-op_x, -op_y, 0.0)
