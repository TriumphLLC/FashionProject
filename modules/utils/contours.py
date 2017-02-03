import bpy

from math import sqrt
from functools import reduce

from fashion_project.modules.draw.lines.line import Line
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.draw.lines import is_one_of_lines
from fashion_project.modules.draw.curves import is_one_of_bezier_curve
  
def get_all_obj():
	# возвращает все линии и кривые на сцене
  return [item for item in bpy.data.objects if is_one_of_lines(item) or is_one_of_bezier_curve(item)]

def get_contours(obj):
	contours = []
	lines = [	# массив всех линий и кривых на сцене, за исключением выделенной
		objects
		for objects in get_all_obj()
		if objects.fp_id != obj.fp_id
	]
	ldeps = [d for d in obj.fp_deps if d != 0]	# получить начальную и конечную точку в выделенном объете
	(bp, ep) = ldeps	# variable unpacking
	def _walker(pbegin, cbuffer):
		connected_obj = [	# получить связанные объекты если начальная точка выбранного принадлежит еще какому либо объекту
			line
			for line in lines 
			if pbegin in line.fp_deps
		]
		for line in connected_obj:	# пройти по всем связаненым объектам
			if line in cbuffer:		# если объект является выделенным, пропустить
				continue
			tbuffer = cbuffer[:] + [line]	# собрать массив из выделенного объекта и всех связанных объектов
			if ep in line.fp_deps:		# если конечная точка присутствует в связанных объектах
				contours.append(tbuffer)	# добавить собранный массив
			else:
				another_point = [p for p in line.fp_deps if p != pbegin][0]	# берем конечную точку из связанной линии
				if all(all((another_point != p) for p in ln.fp_deps) for ln in cbuffer): # если оставшаяся точка не содержится в выделенном объекте
					_walker(another_point, tbuffer)		# рекурсивный вызов с оставшимися точками и связанными объектами
	_walker(bp, [obj])	# вызов функции с передачей точки начала и выделенного объекта
	contours.sort(key=len)	# сортировка по длине
	return contours