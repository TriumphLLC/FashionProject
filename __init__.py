bl_info = {
  "name": "Fashion Project",
  "version": (0, 1, 3, ' (2016-05-19)'),
  "support": 'TESTING',
  "category": "BPY"
}

from . import main

def register():
  main.register()

def unregister():
  ui.unregister()
  # bpy.utils.unregister_class(FPDeleteOverride)
