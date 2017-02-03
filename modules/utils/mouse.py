import bpy

from collections import namedtuple

from . import draw_area

from bpy_extras.view3d_utils import region_2d_to_location_3d


Event = namedtuple('Event', 'x y x_rel y_rel type')
_EVENT_BUFFER = None


def set_event(event):
  global _EVENT_BUFFER
  _EVENT_BUFFER = Event(
    x = event.mouse_x,
    y = event.mouse_region_y,
    x_rel = event.mouse_region_x,
    y_rel = event.mouse_region_y,
    type = event.type
  )

def get_event():
  return _EVENT_BUFFER
  
def is_window_event():
  if not _EVENT_BUFFER:
    return None
  window = draw_area.find_2d_window_region()
  coords_2d = get_rel_coords_region_2d()
  return (coords_2d[0] < window.width and coords_2d[1] < window.height)
  
def is_lmb():
  if not _EVENT_BUFFER:
    return None
  return _EVENT_BUFFER.type == 'LEFTMOUSE'
  
def get_coords_location_3d():
  if not _EVENT_BUFFER:
    return None
  coords_2d = get_rel_coords_region_2d()
  return region_2d_to_location_3d(bpy.context.region, bpy.context.space_data.region_3d, coords_2d, (0, 0, 0))
  
def get_rel_coords_region_2d():
  if not _EVENT_BUFFER:
    return None
  return (_EVENT_BUFFER.x_rel, _EVENT_BUFFER.y_rel)
