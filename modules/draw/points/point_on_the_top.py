import bpy
from math import cos, sin, pi, sqrt
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.base import Base
from fashion_project.modules.utils.fp_angle import deg_to_radians
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.counter import Counter


class PointOnTheTop(Base):
  FP_TYPE = 'fp.draw.points.point_on_the_top'
  DEFAULT_EXPRESSION = '1.25'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'Точка на вершине прямоугольного треугольника'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)

  def poll(self, context):
    '''
        Нужны четыре выделенных точки,
        одна из которых является активной.
    '''
    return len(context.selected_objects) == 4 and all(is_one_of_points(item) for item in context.selected_objects)

  def create(self, context):
    parent = context.active_object
    dep_id = tuple([
                     d.fp_id for d in context.selected_objects
                     if not d.fp_id == parent.fp_id
                     ])
    bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
    obj = context.object

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)
    obj.parent = parent
    obj.fp_deps = dep_id
    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False

    mat = bpy.data.materials.new('ЗаливкаТочкиИзДвухXиY')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)

  def update(self, obj, context):
    p_a_location = get_point_abs_location(obj.parent)
    collection_of_d_a_location = ([
                                    d for d in bpy.data.objects
                                    if (d.fp_id == obj.fp_deps[0] or d.fp_id == obj.fp_deps[1] or d.fp_id == obj.fp_deps[2]) and d.fp_id > 0
                                    ])
    d_a_location = [get_point_abs_location(x) for x in collection_of_d_a_location]
    selected_p_A_x = d_a_location[0][0]
    selected_p_A_y = d_a_location[0][1]
    selected_p_B_x = d_a_location[1][0]
    selected_p_B_y = d_a_location[1][1]
    selected_p_C_x = d_a_location[2][0]
    selected_p_C_y = d_a_location[2][1]
    active_p_D_x = p_a_location[0]
    active_p_D_y = p_a_location[1]
    length_CD = sqrt((active_p_D_x - selected_p_C_x) * (active_p_D_x - selected_p_C_x) + (active_p_D_y - selected_p_C_y) * (active_p_D_y - selected_p_C_y))
    radius = length_CD / 2.0
    radius_p_A_x = (active_p_D_x + selected_p_C_x) / 2.0
    radius_p_A_y = (active_p_D_y + selected_p_C_y) / 2.0
    if abs(selected_p_A_x - selected_p_B_x) > 0.001:
        coef_k1_AB = (selected_p_B_y - selected_p_A_y)/(selected_p_B_x - selected_p_A_x)
        coef_b1_AB = -selected_p_A_x * coef_k1_AB + selected_p_A_y
        coef_sqr_A = coef_k1_AB * coef_k1_AB + 1
        coef_sqr_B = 2 * coef_k1_AB * coef_b1_AB - 2 * radius_p_A_y * coef_k1_AB - 2 * radius_p_A_x
        coef_sqr_C = coef_b1_AB * coef_b1_AB - 2 * radius_p_A_y * coef_b1_AB + radius_p_A_y * radius_p_A_y + radius_p_A_x * radius_p_A_x - radius * radius
        deter = coef_sqr_B * coef_sqr_B - 4 * coef_sqr_A * coef_sqr_C
        if deter > 0:
            final_p_E_x = (-coef_sqr_B + sqrt(deter)) / (2 * coef_sqr_A)
            final_p_E_y = final_p_E_x * coef_k1_AB + coef_b1_AB
            length_AE = sqrt((selected_p_A_x - final_p_E_x) * (selected_p_A_x - final_p_E_x) + (selected_p_A_y - final_p_E_y) * (selected_p_A_y - final_p_E_y))
            final_p_F_x = (-coef_sqr_B - sqrt(deter)) / (2 * coef_sqr_A)
            final_p_F_y = final_p_F_x * coef_k1_AB + coef_b1_AB
            length_AF = sqrt((selected_p_A_x - final_p_F_x) * (selected_p_A_x - final_p_F_x) + (selected_p_A_y - final_p_F_y) * (selected_p_A_y - final_p_F_y))
            nearest_p_x = final_p_E_x if length_AE < length_AF else final_p_F_x
            nearest_p_y = final_p_E_y if length_AE < length_AF else final_p_F_y
            obj.location = (nearest_p_x - active_p_D_x, nearest_p_y - active_p_D_y, 0.0)
        else:
            obj.location = (-10000.0, -10000.0, 0.0)
    else:
        coef_sqr_A = 1
        coef_sqr_B = -2 * radius_p_A_y
        coef_sqr_C = radius_p_A_y * radius_p_A_y + selected_p_A_x * selected_p_A_x - 2 * selected_p_A_x * radius_p_A_x + radius_p_A_x * radius_p_A_x - radius * radius
        deter = coef_sqr_B * coef_sqr_B - 4 * coef_sqr_A * coef_sqr_C
        if deter > 0:
            final_p_E_y = (-coef_sqr_B + sqrt(deter)) / (2 * coef_sqr_A)
            length_AE = sqrt((selected_p_A_x - selected_p_A_x) * (selected_p_A_x - selected_p_A_x) + (selected_p_A_y - final_p_E_y) * (selected_p_A_y - final_p_E_y))

            final_p_F_y = (-coef_sqr_B - sqrt(deter)) / (2 * coef_sqr_A)
            length_AF = sqrt((selected_p_A_x - selected_p_A_x) * (selected_p_A_x - selected_p_A_x) + (selected_p_A_y - final_p_F_y) * (selected_p_A_y - final_p_F_y))

            nearest_p_y = final_p_E_y if length_AE < length_AF else final_p_F_y
            obj.location = (selected_p_A_x - active_p_D_x, nearest_p_y - active_p_D_y, 0.0)

