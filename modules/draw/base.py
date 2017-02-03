import bpy


class Base():
  
  FP_TYPE = ''
  
  def __init__(self):
    if not bool(self.FP_TYPE):
      raise Exception('FP_TYPE should not be empty')
  
  def get_all(self):
    return tuple(
      obj for obj in bpy.data.objects
      if obj.fp_type == self.FP_TYPE
    )

  def poll(self):
    return False
