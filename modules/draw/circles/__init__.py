'''
Утилиты для работы с кругом.
'''

import bpy

from fashion_project.modules.draw.arcs.arc import Arc


def is_one_of_circle(obj):
    return obj.fp_type.startswith('fp.draw.circles.')

