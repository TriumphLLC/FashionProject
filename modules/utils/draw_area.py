import bpy


def find_2d_area():
  if hasattr(bpy.context, 'screen') and hasattr(bpy.context.screen, 'areas'):
    view_areas = [
      a for a in bpy.context.screen.areas 
      if a.type == 'VIEW_3D'
    ]
    return max(view_areas, key = lambda a: a.x) if len(view_areas) > 0 else None
  else:
    return None

def find_2d_window_region():
  area = find_2d_area()
  if area is None: 
    return None
  else:
    return [
      r for r in area.regions
      if r.type == 'WINDOW'
    ][0]
  