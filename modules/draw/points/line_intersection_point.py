import bpy

from math import cos, sin, pi

from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.base import Base
from fashion_project.modules.utils.fp_angle import deg_to_radians

from fashion_project.modules.draw.counter import Counter


class LineIntersectionPoint(Base):
  FP_TYPE = 'fp.draw.points.line_intersection_point'
  DEFAULT_EXPRESSION = '1.25'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'Точка пересечения линии и окружности'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def create(self, context):
    '''Under Construction'''
    pass

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    if (
                                    d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1] or d.fp_id == obj.fp_deps[
                                      2]) and d.fp_id > 0
                                    ])
    d_a_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    selected_p_A_x = d_a_location[0][0]
    selected_p_A_y = d_a_location[0][1]
    selected_p_B_x = d_a_location[1][0]
    selected_p_B_y = d_a_location[1][1]
    active_p_C_x = p_a_location[0]
    active_p_C_y = p_a_location[1]
    radius = float(obj.fp_expression)
    if abs(selected_p_B_x - active_p_C_x) > 0.001:
      coef_k1_BC = (active_p_C_y - selected_p_B_y) / (active_p_C_x - selected_p_B_x)
      coef_b1_BC = -coef_k1_BC * selected_p_B_x + selected_p_B_y
      coef_sqr_A = coef_k1_BC * coef_k1_BC + 1
      coef_sqr_B = 2 * coef_k1_BC * coef_b1_BC - 2 * selected_p_A_y * coef_k1_BC - 2 * selected_p_A_x
      coef_sqr_C = coef_b1_BC * coef_b1_BC - 2 * selected_p_A_y * coef_b1_BC + selected_p_A_y * selected_p_A_y + selected_p_A_x * selected_p_A_x - radius * radius
      deter = coef_sqr_B * coef_sqr_B - 4 * coef_sqr_A * coef_sqr_C
      if deter == 0:
        final_p_D_x = (-coef_sqr_B + sqrt(deter)) / (2 * coef_sqr_A)
        final_p_D_y = coef_k1_BC * final_p_D_x + coef_b1_BC
        obj.location = (final_p_D_x - active_p_C_x, final_p_D_y - active_p_C_y, 0.0)
      elif deter > 0:
        final_p_D_x = (-coef_sqr_B + sqrt(deter)) / (2 * coef_sqr_A)
        final_p_D_y = coef_k1_BC * final_p_D_x + coef_b1_BC
        length_CD = sqrt((active_p_C_x - final_p_D_x) * (active_p_C_x - final_p_D_x) + (active_p_C_y - final_p_D_y) * (
        active_p_C_y - final_p_D_y))
        final_p_F_x = (-coef_sqr_B - sqrt(deter)) / (2 * coef_sqr_A)
        final_p_F_y = final_p_F_x * coef_k1_BC + coef_b1_BC
        length_FD = sqrt((active_p_C_x - final_p_F_x) * (active_p_C_x - final_p_F_x) + (active_p_C_y - final_p_F_y) * (
        active_p_C_y - final_p_F_y))
        nearest_p_x = final_p_D_x if length_CD < length_FD else final_p_F_x
        nearest_p_y = final_p_D_y if length_CD < length_FD else final_p_F_y
        obj.location = (nearest_p_x - active_p_C_x, nearest_p_y - active_p_C_y, 0.0)
      else:
        obj.location = (-10000.0, -10000.0, 0.0)
    else:
      coef_sqr_A = 1
      coef_sqr_B = -2 * selected_p_A_y
      coef_sqr_C = selected_p_A_y * selected_p_A_y + active_p_C_x * active_p_C_x + 2 * active_p_C_x * selected_p_A_x + selected_p_A_x * selected_p_A_x - radius * radius
      deter = coef_sqr_B * coef_sqr_B - 4 * coef_sqr_A * coef_sqr_C
      if deter > 0:
        final_p_D_y = (-coef_sqr_B + sqrt(deter)) / (2 * coef_sqr_A)
        length_CD = sqrt(
          (active_p_C_x - active_p_C_x) * (active_p_C_x - active_p_C_x) + (active_p_C_y - final_p_D_y) * (
          active_p_C_y - final_p_D_y))
        final_p_E_y = (-coef_sqr_B - sqrt(deter)) / (2 * coef_sqr_A)
        length_FD = sqrt(
          (active_p_C_x - active_p_C_x) * (active_p_C_x - active_p_C_x) + (active_p_C_y - final_p_E_y) * (
          active_p_C_y - final_p_E_y))
        nearest_p_y = final_p_E_y if length_CD < length_FD else final_p_D_y
        obj.location = (selected_p_B_x - active_p_C_x, nearest_p_y - active_p_C_y, 0.0)

  def poll(self):
    # TEST
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    if
                                    (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1]) and d.fp_id > 0
                                    ])

    points_parent = [get_point_abs_location(x) for x in collection_of_d_a_location]
    handle_right = (
      obj.parent.data.splines[0].bezier_points[0].handle_right[0] - obj.parent.data.splines[0].bezier_points[0].co[0] +
      points_parent[0][0],
      obj.parent.data.splines[0].bezier_points[0].handle_right[1] - obj.parent.data.splines[0].bezier_points[0].co[1] +
      points_parent[0][1], 0.0)
    handle_left = (
      obj.parent.data.splines[0].bezier_points[1].handle_left[0] - obj.parent.data.splines[0].bezier_points[1].co[0] +
      points_parent[1][0],
      obj.parent.data.splines[0].bezier_points[1].handle_left[1] - obj.parent.data.splines[0].bezier_points[1].co[1] +
      points_parent[1][1], 0.0)
    bezier_t = 0.0
    bezier_l = 0.0
    step_t = 0.001
    x = 0.0
    y = 0.0
    previous_x = points_parent[0][0]
    previous_y = points_parent[0][1]
    while bezier_t <= 1.0:
      x = ((1 - bezier_t) ** 3) * points_parent[0][0] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[
        0] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[0] + (bezier_t ** 3) * points_parent[1][0]
      y = ((1 - bezier_t) ** 3) * points_parent[0][1] + 3 * bezier_t * ((1 - bezier_t) ** 2) * handle_right[
        1] + 3 * (bezier_t ** 2) * (1 - bezier_t) * handle_left[1] + (bezier_t ** 3) * points_parent[1][1]
      bezier_l += sqrt((x - previous_x) ** 2 + (y - previous_y) ** 2)
      previous_x = x
      previous_y = y
      if bezier_l >= expression_to_value(obj.fp_expression):
        bezier_t = 2.0
      bezier_t += step_t
    x += obj.parent.data.splines[0].bezier_points[0].co[0] - points_parent[0][0]
    y += obj.parent.data.splines[0].bezier_points[0].co[1] - points_parent[0][1]
    obj.location = (x, y, 0.0)
