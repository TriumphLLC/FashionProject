import bpy

from fashion_project.modules.draw.curves.complex_curve import ComplexCurve

BUFFER_CURVE = 0
BUFFER_HANDLE = None
BUFFER_HANDLE_COORDS = (0,0,0)


@bpy.app.handlers.persistent
def watch_active_habdlers(_0):
  global BUFFER, BUFFER_HANDLE, BUFFER_HANDLE_COORDS
  cc = ComplexCurve()
  obj = bpy.context.active_object
  if obj and obj.fp_type == ComplexCurve.FP_TYPE:
    if BUFFER != obj.fp_id:
      cc.remove_guides()
      cc.add_guides(obj)
      BUFFER = obj.fp_id
  elif obj and obj.fp_type == ComplexCurve.FP_TYPE_CONTROL_POINT:
    if obj.fp_id != BUFFER_HANDLE:
      BUFFER_HANDLE = obj.fp_id
      BUFFER_HANDLE_COORDS = obj.location[::]
    else:
      if any((BUFFER_HANDLE_COORDS[i] != obj.location[i]) for i in range(2)):
        cc.update_active(obj)
        BUFFER_HANDLE_COORDS = obj.location[::]
  else:
    cc.remove_guides()
    BUFFER = 0


def register():
  bpy.app.handlers.scene_update_pre.append(watch_active_habdlers)

def unregister():
  bpy.app.handlers.scene_update_pre.remove(watch_active_habdlers)
