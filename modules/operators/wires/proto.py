import bpy

from math import pi, sin, cos
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bgl import glEnable, glDisable, glBegin, glEnd, glVertex2f, glVertex3f, glColor4f, glLineWidth, GL_LINE_STRIP, GL_LINE_STIPPLE, GL_BLEND, GL_LINE_LOOP, GL_POLYGON

from fashion_project.modules.utils import mouse, get_point_abs_location
from fashion_project.modules.utils.mathlib import deg2rad


class FP_WireProto:
  '''
  Базовый класс для наследования 
  операторами рисования направляющих,
  сам по себе оператором не является.
  '''
  
  color3f = bpy.props.FloatVectorProperty(size=3, default=(0.8,0.2,1.0))
  alpha = bpy.props.FloatProperty(default=0.5)
  line_width = bpy.props.IntProperty(default=1)
  point_radius = bpy.props.IntProperty(default=5)
  point_poly = bpy.props.IntProperty(default=64)
  point_angle_ammend = bpy.props.FloatProperty(default=0.0)
  
  _handle = None
  
  @classmethod
  def poll(cls, context):
    return context.area.type == 'VIEW_3D'
    
  def execute(self, context):
    self.target = bpy.context.area.spaces.active
    self._handle = self.target.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
    context.area.tag_redraw()
    context.window_manager.modal_handler_add(self)
    self.on_before_modal()
    return {'RUNNING_MODAL'}

  def modal(self, context, event):
    mouse.set_event(event)
    if event.type in {'LEFTMOUSE'}:
      self.target.draw_handler_remove(self._handle, 'WINDOW')
      context.area.tag_redraw()
      self.on_before_finish()
      return {'FINISHED'}
    else:
      if event.type in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'}:
        context.area.tag_redraw()
      return {'PASS_THROUGH'}
  
  def draw_callback(self, context):
    mouse_coords_2 = mouse.get_rel_coords_region_2d()
    mouse_coords_3 = mouse.get_coords_location_3d()
    if (
          (not mouse_coords_3) 
          or 
          (not mouse_coords_3[2] == 0.0)
      ): 
      return
    if (mouse.is_window_event()):
      first = get_point_abs_location(context.active_object) if context.active_object else (0,0,0)
      second = (mouse_coords_3)
      self.draw_line(context, (first, second))
      self.draw_point(context, (second,))
    
  def draw_line(self, context, coords3f):
    region = context.region
    region_data = context.region_data
    glEnable(GL_BLEND)
    glLineWidth(self.line_width)
    glColor4f(*self.get_color4f())
    glBegin(GL_LINE_STRIP)
    for c3f in coords3f:
      glVertex2f(*location_3d_to_region_2d(region, region_data, tuple(c3f)).to_tuple())
    glEnd()
    glDisable(GL_BLEND)
    glColor4f(0.0, 0.0, 0.0, 1.0)
    glLineWidth(1)
    glDisable(GL_LINE_STIPPLE)
    
  def draw_point(self, context, coords3f):
    region = context.region
    region_data = context.region_data
    glEnable(GL_BLEND)
    glBegin(GL_POLYGON)
    glColor4f(*self.get_color4f())
    for center in coords3f:
      (cx, cy) = location_3d_to_region_2d(region, region_data, tuple(center)).to_tuple()
      for i in range(self.point_poly):
        angle = (2 * pi * i / self.point_poly) + self.point_angle_ammend
        x = cos(angle) * self.point_radius
        y = sin(angle) * self.point_radius
        glVertex2f(cx + x, cy + y)
    glEnd()
    glColor4f(0.0, 0.0, 0.0, 1.0)
    glDisable(GL_BLEND)
    
  def get_color4f(self):
    return (tuple(self.color3f) + (self.alpha,))
    
  def on_before_modal(self):
    pass
    
  def on_before_finish(self):
    pass
