import bpy

from fashion_project.modules.draw.curves.bezier_curve import BezierCurve

BUFFER_CURVE = 0
BUFFER_HANDLE = None
BUFFER_HANDLE_COORDS = (0,0,0)


@bpy.app.handlers.persistent
def watch_active(_0):
  global BUFFER, BUFFER_HANDLE, BUFFER_HANDLE_COORDS
  bc = BezierCurve()
  obj = bpy.context.active_object
  if obj and obj.fp_type == BezierCurve.FP_TYPE:
    if BUFFER != obj.fp_id:
      bc.remove_guides()
      bc.add_guides(obj)
      BUFFER = obj.fp_id
  elif obj and obj.fp_type == BezierCurve.FP_TYPE_CONTROL_POINT:
    if obj.fp_id != BUFFER_HANDLE:
      BUFFER_HANDLE = obj.fp_id
      BUFFER_HANDLE_COORDS = obj.location[::]
    else:
      if any((BUFFER_HANDLE_COORDS[i] != obj.location[i]) for i in range(2)):
        bc.update_active(obj)
        BUFFER_HANDLE_COORDS = obj.location[::]
  else:
    bc.remove_guides()
    BUFFER = 0


def register():
  bpy.app.handlers.scene_update_pre.append(watch_active)

def unregister():
  bpy.app.handlers.scene_update_pre.remove(watch_active)
