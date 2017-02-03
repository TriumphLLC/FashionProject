'''
Утилиты для работы с дугами.
'''

import bpy

from fashion_project.modules.utils import get_point_abs_location

def is_one_of_bezier_curve(obj):
    return obj.fp_type.startswith('fp.draw.curves.bezier2p')

def is_one_of_complex_curve(obj):
    return obj.fp_type.startswith('fp.draw.curves.complex_curve')

def get_curve_ends(obj):
  deps = obj.fp_deps
  points = [x for x in bpy.data.objects if x.fp_id in deps and x.fp_id > 0 ]
  ret_points = [get_point_abs_location(p) for p in points]
  return ret_points
