import bpy

from math import pi, sqrt, atan

from fashion_project.modules.utils.mathlib import rad2deg
from fashion_project.modules.draw.points.point import Point
from fashion_project.modules.operators.wires.proto import FP_WireProto
from fashion_project.modules.utils import mouse


TARGET_LOCATION = (0,0,0)
OAAT_LOCK = False


class FP_PointFreeWired(bpy.types.Operator, FP_WireProto):
  bl_idname = "fp.point_free_wired"
  bl_label = "Free Wired Point"
  
  precision_expression = bpy.props.IntProperty(default=2)
  precision_coords = bpy.props.IntProperty(default=2)
  
  @classmethod
  def poll(cls, context):
    return True
    
  def __init__(self):
    self.color3f = (0.9, 0.9, 0.1)
    self.point_poly = 4
    self.point_radius = 12
    self.point_angle_ammend = pi/4
    
  def on_before_modal(self):
    global OAAT_LOCK
    OAAT_LOCK = True
    
  def on_before_finish(self):
    global OAAT_LOCK
    (x,y) = [round(c, bpy.context.scene.fp_dev.coords_precision) for c in TARGET_LOCATION[:2]]
    point = Point()
    point_obj = point.create(bpy.context)
    point_obj.parent = None
    point_obj.fp_expression = str(round(sqrt(x**2 + y**2), bpy.context.scene.fp_dev.expression_precision))
    point_obj.fp_angle = rad2deg(atan(y/x)) if x != 0 else 0
    OAAT_LOCK = False
    
  def draw_callback(self, context):
    global TARGET_LOCATION
    mouse_coords_3 = mouse.get_coords_location_3d()
    if (
          (not mouse_coords_3) 
          or 
          (not mouse_coords_3[2] == 0.0)
      ): 
      return
    first = (0,0,0)
    second = mouse_coords_3
    self.draw_point(context, (second,))
    TARGET_LOCATION = mouse_coords_3


def register():
  bpy.utils.register_class(FP_PointFreeWired)

def unregister():
  bpy.utils.unregister_class(FP_PointFreeWired)
