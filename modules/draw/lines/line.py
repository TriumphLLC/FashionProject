import bpy

from mathutils import Vector

from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point


class Line(Base):
  FP_TYPE = 'fp.draw.lines.line'
  BASE_NAME = 'Линия'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0, 0.6, 0.4)
  COUNT = "2"
  
  def create(self, context, source_points = None):
    if not source_points:
      source_points = context.selected_objects
    locations = tuple(get_point_abs_location(point) for point in source_points)
    center = (
      (locations[1][0] - locations[0][0]) / 2 + locations[0][0],
      (locations[1][1] - locations[0][1]) / 2 + locations[0][1],
      0.0
    )
    vectors = [Vector(location) for location in locations]
    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    
    curvedata.dimensions = self.CURVE_DIMS
    curvedata.bevel_depth = self.CURVE_BEVEL_DEPTH
    curvedata.fill_mode = self.CURVE_FILL_MODE

    line_mat = bpy.data.materials.new('ОбводкаЛинии')
    line_mat.diffuse_color = self.STROKE_COLOR
    curvedata.materials.append(line_mat)

    objectdata = bpy.data.objects.new(self.BASE_NAME, curvedata)
    
    Counter.register(objectdata, self.FP_TYPE)
    
    objectdata.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(objectdata)
    
    objectdata.fp_deps = tuple([so.fp_id for so in source_points] + [0])

    objectdata.location = center
    objectdata.lock_location = (True, True, True)
    objectdata.show_name = True
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new("POLY")
    polyline.points.add(len(vectors)-1)
    for num in range(len(vectors)):
      x, y, z = vectors[num]
      polyline.points[num].co = (x - center[0], y - center[1], 0, 0.001)
    objectdata.fp_count = self.COUNT
    return objectdata
      
  def update(self, line_obj, context):
    points = [obj for obj in bpy.data.objects if obj.fp_id > 0 and obj.fp_id in line_obj.fp_deps]
    if len(points) < 2:
      return
    locations = [get_point_abs_location(point) for point in points]
    center = (
      (locations[1][0] - locations[0][0]) / 2 + locations[0][0],
      (locations[1][1] - locations[0][1]) / 2 + locations[0][1],
      0.0
    )
    line_obj.location = center
    for index,location in enumerate(locations):
      line_obj.data.splines[0].points[index].co = tuple([c - center[i] for i,c in enumerate(location)] + [0.001])
  
  def poll(self, context):
    '''
    Добавить линию можно, если есть две выделенных точки любого типа.
    '''
    return (
      context.active_object
      and is_one_of_points(context.active_object)
      and len(context.selected_objects) == 2
      and all(is_one_of_points(item) for item in context.selected_objects)
    )
