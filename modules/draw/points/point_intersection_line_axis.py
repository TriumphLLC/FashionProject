import bpy

from functools import reduce

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.utils import get_point_abs_location


class IntersectionLineAndAxis(Base):
        FP_TYPE = 'fp.draw.points.intersection_line_and_axis'
        DEFAULT_LOCATION = (0.0, 0.0, 0.0)
        BASE_NAME = 'ТочкаПересеченияЛинииОси'
        POINT_RADIUS = 0.075
        FILL_COLOR = (0.5, 0, 0.9)

        def poll(self, context):
                return len(context.selected_objects) == 2

        def create(self, context):
                dep_id = tuple([d.fp_id for d in context.selected_objects] + [0])
                bpy.ops.mesh.primitive_plane_add(radius=self.POINT_RADIUS)
                obj = context.object
                Counter.register(obj, self.FP_TYPE)
                obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)
                obj.fp_deps = dep_id
                obj.lock_location = (True, True, True)
                obj.show_name = True
                obj.select = False
                mat = bpy.data.materials.new('ЗаливкаТочкиПересеченияЛинииОси')
                mat.diffuse_color = self.FILL_COLOR
                obj.data.materials.append(mat)
                obj.location = self.DEFAULT_LOCATION

        def update(self, obj, context):
                pass
