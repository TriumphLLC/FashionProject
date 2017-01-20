import bpy

from fashion_project.modules.draw.lines import is_one_of_lines
from fashion_project.modules.utils.contours import get_contours

FP_ID = 0   # выделенный объект
CURRENT_INDEX = 0

def get_current_index():
  return CURRENT_INDEX

class FP_ContourHighlight(bpy.types.Operator):
  bl_idname = "fp.contour_highlight"
  bl_label = "Hightlight Contour"
  
  @classmethod
  def poll(cls, context):
    global FP_ID, CURRENT_INDEX
    cond = is_one_of_lines(context.active_object) and len(get_contours(context.active_object))  # True если выделена линия
    if cond:
      if FP_ID != context.active_object.fp_id:
        FP_ID = context.active_object.fp_id     # ID выделенного объекта
        CURRENT_INDEX = 0
      else:
        FP_ID = 0
        CURRENT_INDEX = 0
    return cond
    
  def execute(self, context):
    global CURRENT_INDEX
    contours = get_contours(context.active_object)  # получить замкнутый контур
    for obj in bpy.data.objects:  # пройти по всем объектам на сцене
      obj.select = obj in contours[CURRENT_INDEX]   # выделить все с заданным индексом
    CURRENT_INDEX += 1
    if CURRENT_INDEX == len(contours):  # если заданный индекс == длине массива всех объектов в контуре, обнулить
      CURRENT_INDEX = 0
    return {"FINISHED"}


def register():
  bpy.utils.register_class(FP_ContourHighlight)

def unregister():
  bpy.utils.unregister_class(FP_ContourHighlight)
