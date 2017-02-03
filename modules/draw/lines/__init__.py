'''
Утилиты для работы с линиями.
'''

import bpy

from math import sqrt
from functools import reduce

from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.curves import is_one_of_bezier_curve


def is_one_of_points_lines(obj):
  if obj.fp_type != Line.FP_TYPE:
    return obj.fp_type.startswith('fp.draw.lines.')
    
def is_one_of_lines(obj):
  if not obj:
    return False
  else:
    return obj.fp_type.startswith('fp.draw.lines.')
  
def get_all_lines():
  return [item for item in bpy.data.objects if is_one_of_lines(item)]

def get_line_length(obj, ndig=2):
  plocs = [p.co[:2] for p in obj.data.splines[0].points]
  return round(sqrt(sum([(plocs[1][i] - plocs[0][i])**2 for i in range(2)])), ndig)
  
def get_line_ends(obj):
  deps = obj.fp_deps
  points = [x for x in bpy.data.objects if x.fp_id in deps and x.fp_id > 0 ]
  ret_points = [get_point_abs_location(p) for p in points]
  return ret_points

def get_contours(obj):
  contours = []
  lines = [
    line
    for line in get_all_lines()
    if line.fp_id != obj.fp_id
  ]
  ldeps = [d for d in obj.fp_deps if d != 0]
  (bp, ep) = ldeps
  def _walker(pbegin, cbuffer):
    connected_lines = [
      line
      for line in lines 
      if pbegin in line.fp_deps
    ]
    for line in connected_lines:
      if line in cbuffer:
        continue
      tbuffer = cbuffer[:] + [line]
      if ep in line.fp_deps:
        contours.append(tbuffer)
      else:
        another_point = [p for p in line.fp_deps if p != pbegin][0]
        if all(all((another_point != p) for p in ln.fp_deps) for ln in cbuffer):
          _walker(another_point, tbuffer)
  _walker(bp, [obj])
  contours.sort(key=len)
  return contours

def get_contours_exclusive(obj):
  raise Exception('501 not implemented')
  
def flatmap_contour_points(contour):
  return set(reduce(lambda result, line: result + list(filter(lambda d: d != 0, line.fp_deps)), contour, []))

def selection_is_contour():
  selection = bpy.context.selected_objects
  if (
    not all(is_one_of_lines(obj) or is_one_of_bezier_curve(obj) for obj in selection)
    or
    len(selection) < 2
  ):
    return False
  else:
    return True
