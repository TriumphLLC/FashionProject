import bpy

from fashion_project.modules.draw.points.point_figures_intersection import PointFiguresIntersection

class FP_PointFiguresIntersection(bpy.types.Operator):
  '''
  Позволяет построить точки пересечения линий, кривых, дуг

  Требует двух выделенных фигур
  '''
  bl_idname = "fp.point_figures_intersection"
  bl_label = "FP_PointFiguresIntersection"
  
  @classmethod
  def poll(cls, context):
    return PointFiguresIntersection().poll(context)

  def execute(self, context):
    PointFiguresIntersection().create(context)
    return {'FINISHED'}

def register():
  bpy.utils.register_class(FP_PointFiguresIntersection)

def unregister():
  bpy.utils.unregister_class(FP_PointFiguresIntersection)