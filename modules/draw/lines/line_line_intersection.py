import bpy

from mathutils import Vector

from fashion_project.modules.utils import get_point_abs_location

from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.lines.line import Line

from fashion_project.modules.utils.intersections import elements_intersection
from fashion_project.modules.utils.intersections import line_to_line


class LineLineIntersection(Base):
  FP_TYPE = 'fp.draw.points.line_line_intersection'
  BASE_NAME = 'ТочкаПересеченияЛиний'
  POINT_RADIUS = 0.075
  FILL_COLOR = (0, 0.6, 0.4)
  

  def create(self, context):
    dep_id = tuple([
      d.fp_id for d in context.selected_objects
    ] + [0])

    line1_points = [obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_id in context.selected_objects[0].fp_deps]
    line2_points = [obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_id in context.selected_objects[1].fp_deps]

    locations1 = [get_point_abs_location(point) for point in line1_points]
    locations2 = [get_point_abs_location(point) for point in line2_points]

    center = line_to_line({ "x": locations1[0][0], "y": locations1[0][1] },
                          { "x": locations1[1][0], "y": locations1[1][1] },
                          { "x": locations2[0][0], "y": locations2[0][1] },
                          { "x": locations2[1][0], "y": locations2[1][1] })

    bpy.ops.mesh.primitive_plane_add(radius = self.POINT_RADIUS)

    obj = context.object
    obj.fp_deps = dep_id

    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)

    obj.location = (center["points"][0]["x"], center["points"][0]["y"], 0)

    obj.lock_location = (True, True, True)
    obj.show_name = True

    mat = bpy.data.materials.new('ЗаливкаТочки')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)
    return obj


  def update(self, point_obj, context):
    for obj in bpy.data.objects:
      if obj.fp_id == point_obj.fp_deps[0]:
        line1 = obj
    for obj in bpy.data.objects:
     if obj.fp_id == point_obj.fp_deps[1]:
      line2 = obj
    intersection_point = elements_intersection(line1, line2)
    point_obj.location = (intersection_point["points"][0]["x"], intersection_point["points"][0]["y"], 0)



  def poll(self, context):
    '''
    Нужны четыре выделенных точки,
    одна из которых является активной.
    '''
    return (
      context.active_object 
      and context.active_object.fp_type == Line.FP_TYPE
      and len(context.selected_objects) == 2
      and all(obj.fp_type == Line.FP_TYPE for obj in context.selected_objects)
    )


