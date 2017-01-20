import bpy

from mathutils import Quaternion

from fashion_project.modules.utils import draw_area

VIEW_QUAT = Quaternion((1,0,0,0))

@bpy.app.handlers.persistent
def guard_view_2d(_0):
  area_2d = draw_area.find_2d_area()
  if area_2d:
    region = area_2d.spaces.active.region_3d
    if region.view_rotation != VIEW_QUAT:
      region.view_rotation = VIEW_QUAT

# def _area_find_2d():
#   if hasattr(bpy.context, 'screen') and hasattr(bpy.context.screen, 'areas'):
#     view_areas = [
#       a for a in bpy.context.screen.areas 
#       if a.type == 'VIEW_3D'
#     ]
#     return max(view_areas, key = lambda v: v.x) if len(view_areas) > 0 else None
#   else:
#     return None


def register():
  bpy.app.handlers.scene_update_post.append(guard_view_2d)
  
def unregister():
  bpy.app.handlers.scene_update_post.remove(guard_view_2d)
