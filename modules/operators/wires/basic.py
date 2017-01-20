import bpy

# from math import pi, sin, cos
# from bpy_extras.view3d_utils import location_3d_to_region_2d
# from bgl import glEnable, glDisable, glBegin, glEnd, glVertex2f, glVertex3f, glColor4f, glLineWidth, GL_LINE_STRIP, GL_LINE_STIPPLE, GL_BLEND, GL_LINE_LOOP, GL_POLYGON

# from fashion_project.modules.utils import mouse, get_point_abs_location
# from fashion_project.modules.utils.mathlib import deg2rad

from .proto import FP_WireProto


class FP_BasicWire(bpy.types.Operator, FP_WireProto):
  '''
  Оператор построения направляющей 
  между выделенной точкой или началом координат
  и курсором мыши
  '''
  bl_idname = 'fp.draw_basic_wire'
  bl_label = 'FP wire between selected point and mouse cursor'


def register():
  bpy.utils.register_class(FP_BasicWire)

def unregister():
  bpy.utils.unregister_class(FP_BasicWire)