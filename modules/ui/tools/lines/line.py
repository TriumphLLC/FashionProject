import bpy

from mathutils import Vector

from fashion_project.modules.utils import get_point_abs_location

class FP_Line(bpy.types.Operator):
  '''
  Позволяет построить линию по двум точкам.

  Требует двух выделенных точек.
  '''
  bl_idname = "fp.line"
  bl_label = "FP_Line"

  @classmethod
  def poll(cls, context):
    return len(context.selected_objects) == 2

  def execute(self, context):
    vectors = [Vector(get_point_abs_location(point)) for point in context.selected_objects]
    curvedata = bpy.data.curves.new(name='Curve', type='CURVE')
    curvedata.dimensions = '3D'
    curvedata.bevel_depth = 0.03
    curvedata.fill_mode = "FRONT"
    line_mat = bpy.data.materials.new("Red")
    line_mat.diffuse_color = (0, 0.5, 0)
    curvedata.materials.append(line_mat)
    objectdata = bpy.data.objects.new("ObjCurve", curvedata)
    objectdata.location = (0,0,0)
    bpy.context.scene.objects.link(objectdata)
    polyline = curvedata.splines.new('POLY')
    polyline.points.add(len(vectors)-1)
    for num in range(len(vectors)):
      x, y, z = vectors[num]
      polyline.points[num].co = (x, y, z, 0.001)
    return {'FINISHED'}
