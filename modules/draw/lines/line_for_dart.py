import bpy

from mathutils import Vector

from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.draw.points import is_one_of_points
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.draw.points.point_for_dart import PointForDart


class LineForDart(Base):
  FP_TYPE = 'fp.draw.lines.line_for_dart'
  BASE_NAME = 'ЛинияДляВытачки'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0, 0.3, 0.7)
  COUNT = "2"
  
  def create(self, context, source_points = None):
    if not source_points:
      source_points = context.selected_objects

    points = []
    for point in source_points:
      if point.fp_type == PointForDart.FP_TYPE:
        if point.fp_dart == 0:
          points += [point]
        else:
          for obj in bpy.data.objects:
            if obj.fp_id == point.fp_dart:
              points += [obj]

    if len(points) != 2:
      for point in source_points:
        if point.fp_type != PointForDart.FP_TYPE:
          points += [point]
          break

    locations = tuple(get_point_abs_location(point) for point in points)
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

    line_mat = bpy.data.materials.new('ОбводкаЛинииДляВытачки')
    line_mat.diffuse_color = self.STROKE_COLOR
    curvedata.materials.append(line_mat)

    objectdata = bpy.data.objects.new(self.BASE_NAME, curvedata)
    
    Counter.register(objectdata, self.FP_TYPE)
    
    objectdata.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(objectdata)
    
    objectdata.fp_deps = tuple([so.fp_id for so in points] + [0])

    objectdata.location = center
    objectdata.lock_location = (True, True, True)
    objectdata.show_name = True
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(vectors)-1)
    for num in range(len(vectors)):
      x, y, z = vectors[num]
      polyline.points[num].co = (x - center[0], y - center[1], 0, 0.001)
    objectdata.fp_count = self.COUNT

    points_second = []
    for point in points:
      if point.fp_type == PointForDart.FP_TYPE:
        for obj in bpy.data.objects:
          if obj.fp_dart == point.fp_id:
            points_second += [obj]
            break

    if len(points_second) != 2:
      for point in source_points:
        if point.fp_type != PointForDart.FP_TYPE:
          points_second += [point]
          break

    locations = tuple(get_point_abs_location(point) for point in points_second)
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

    line_mat = bpy.data.materials.new('ОбводкаЛинииДляВытачки')
    line_mat.diffuse_color = self.STROKE_COLOR
    curvedata.materials.append(line_mat)

    objectdata = bpy.data.objects.new(self.BASE_NAME, curvedata)
    
    Counter.register(objectdata, self.FP_TYPE)
    
    objectdata.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(objectdata)
    
    objectdata.fp_deps = tuple([so.fp_id for so in points_second] + [0])

    objectdata.location = center
    objectdata.lock_location = (True, True, True)
    objectdata.show_name = True
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(vectors)-1)
    for num in range(len(vectors)):
      x, y, z = vectors[num]
      polyline.points[num].co = (x - center[0], y - center[1], 0, 0.001)
    objectdata.fp_count = self.COUNT
    
      
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
      and len(context.selected_objects) == 2
      and all(is_one_of_points(item) for item in context.selected_objects)
      and (context.selected_objects[0].fp_type == PointForDart.FP_TYPE or context.selected_objects[1].fp_type == PointForDart.FP_TYPE)
    )
