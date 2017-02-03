import bpy
from math import cos, sin, pi, sqrt
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.circles.circle import Circle
from fashion_project.modules.draw.base import Base
from fashion_project.modules.utils.fp_angle import deg_to_radians
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.counter import Counter


class LineIntersectionAndCircle(Base):
  FP_TYPE = 'fp.draw.points.line_intersection_and_circle'
  DEFAULT_EXPRESSION = '1.5'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'Пересечение линии и окружности'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def poll(self, context):
    '''
        Нужны три выделенных точки,
        одна из которых является активной
    '''
    return len(context.selected_objects) == 3 and all(is_one_of_points(item) for item in context.selected_objects)

  def create(self, context):
    parent = context.active_object
    dep_id = tuple([
                      d.fp_id for d in context.selected_objects
                      if not d.fp_id == parent.fp_id
                      ] + [0])

    draw_circle = Circle()
    draw_circle.create(context)

    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = context.object
    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.parent = parent
    obj.fp_deps = dep_id
    obj.fp_expression = self.DEFAULT_EXPRESSION
    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False
    mat = bpy.data.materials.new('ЗаливкаТочкиНаПересеченииОкружности')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    parent_location = get_point_abs_location(obj.parent)
    print("parent ", obj.parent)
    collection_of_d_a_location = ([
      d for d in bpy.data.objects
      if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
    ])
    active_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    radius = expression_to_value(obj.parent.fp_expression)
    a1_x = active_location[0][0]
    a1_y = active_location[0][1]
    a2_x = active_location[1][0]
    a2_y = active_location[1][1]
    c_x = parent_location[0]
    c_y = parent_location[1]

    a_point = (a2_x - a1_x) * (a2_x - a1_x) + (a2_y - a1_y) * (a2_y - a1_y)
    b_point = 2 * ((a2_x - a1_x) * (a1_x - c_x) + (a2_y - a1_y) * (a1_y - c_y))
    cc_point = c_x * c_x + c_y * c_y + a1_x * a1_x + a1_y * a1_y - 2 * (c_x * a1_x + c_y * a1_y) - radius * radius
    deter = b_point * b_point - 4 * a_point * cc_point

    if deter < 0:
      obj.location = (-10000.0, -10000.0, 0.0)
    elif deter == 0:
      u1 = (-b_point) / (2 * a_point)
      if (0 <= u1) and (u1 <= 1):
        obj.location = (((a1_x + u1 * (a2_x - a1_x)) - c_x), ((a1_y + u1 * (a2_y - a1_y)) - c_y), 0.0)
    else:
      e = sqrt(deter)
      u1 = (-b_point + e) / (2 * a_point)
      u2 = (-b_point - e) / (2 * a_point)
      if (u1 < 0 or u1 > 1) and (u2 < 0 or u2 > 1):
        if (u1 < 0 and u2 < 0) or (u1 > 1 and u2 > 1):
          obj.location = (-10000.0, -10000.0, 0.0)
        else:
          obj.location = (-10000.0, -10000.0, 0.0)
      else:
        if (0 <= u1) and (u1 <= 1):
          obj.location = (((a1_x + u1 * (a2_x - a1_x)) - c_x), ((a1_y + u1 * (a2_y - a1_y)) - c_y), 0.0)
        if (0 <= u2) and (u2 <= 1):
          obj.location = (((a1_x + u2 * (a2_x - a1_x)) - c_x), ((a1_y + u2 * (a2_y - a1_y)) - c_y), 0.0)




