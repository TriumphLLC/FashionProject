import bpy

from fashion_project.modules.draw.base import Base

from mathutils import Vector

class PointsForCreateDetail(Base):
	def __init__(self, pos, hl = None, hr = None, type = None, fp_angles = None, fp_id = None):
		self.pos = Vector(pos)
		self.hl = Vector(hl) if hl else self.pos
		self.hr = Vector(hr) if hr else self.pos
		self.type = type
		self.fp_angles = fp_angles
		self.fp_id = fp_id