import bpy

from math import cos, sin, pi

from fashion_project.modules.utils.fp_expression import expression_to_value
from fashion_project.modules.utils.fp_angle import deg_to_radians
from fashion_project.modules.draw.points import is_one_of_points

from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.base import Base


class FreePoint(Base):
  FP_TYPE = 'fp.draw.points.free_point'
  DEFAULT_EXPRESSION = '1.25'
  DEFAULT_ANGLE = 0.0
  BASE_NAME = 'Точка'
  POINT_RADIUS = 0.075
  COUNT = '1'
  FILL_COLOR = (0, 0.6, 0.4)
  
  def create(self, context):
    parent = None
    if context.active_object and is_one_of_points(context.active_object):
      parent = context.active_object
    if len(context.selected_objects) == 1 and context.selected_objects[0].fp_type == self.FP_TYPE:
      parent = context.selected_objects[0] 
      
    bpy.ops.mesh.primitive_plane_add(radius = self.POINT_RADIUS)
    obj = bpy.context.object
    
    Counter.register(obj, self.FP_TYPE)
    obj.name = self.BASE_NAME + '.' + Counter.get_counter_suffix(obj)
    
    if parent:
      obj.parent = parent
    obj.fp_expression = self.DEFAULT_EXPRESSION
    obj.fp_angle = self.DEFAULT_ANGLE
    obj.fp_count = self.COUNT

    obj.lock_location = (True, True, True)
    obj.show_name = True
    obj.select = False
    
    mat = bpy.data.materials.new('ЗаливкаТочки')
    mat.diffuse_color = self.FILL_COLOR
    obj.data.materials.append(mat)
    
    return obj
  
  def update(self, obj, context):
    # if obj.fp_angle == 360.0:
    #   obj.fp_angle = 0.0
    #   return obj
    
    points = self.get_all()
    obj.location = points[-1].location if len(points) > 1 else (0.0,0.0,0.0)
    
    line = expression_to_value(obj.fp_expression)

    radians = deg_to_radians(obj.fp_angle)
    
    prevLocation = (0.0,0.0,0.0)
    
    line_x = prevLocation[0] + (cos(radians) * line)
    line_y = prevLocation[1] + (sin(radians) * line)

    obj.location = (line_x, line_y, 0.0)
    
  # def get_all(self):
  #   return tuple(oth for oth in bpy.data.objects if oth.fp_type == self.FP_TYPE)
  
  def poll(self, context):
    '''
    Добавить точку можно всегда.
    '''
    return True
