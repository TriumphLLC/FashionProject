import bpy

COUNTER = 0


class Counter:
  
  @staticmethod
  def register(obj, fp_type):
    global COUNTER
    _ids = tuple(oth.fp_id for oth in bpy.data.objects if oth.fp_id > 0)
    COUNTER = max(_ids) if len(_ids) > 0 else 0
    COUNTER += 1
    obj.fp_id = COUNTER
    obj.fp_type = fp_type
    return COUNTER
  
  @staticmethod
  def get_counter():
    global COUNTER
    return COUNTER

  @staticmethod
  def get_counter_suffix(obj):
    return '{0:03d}'.format(obj.fp_id)
