import bpy
import math
import string
import re
from fashion_project.modules.props.size_table import SIZE_TABLE_MAP

sizes = SIZE_TABLE_MAP

def expression_to_value(formula):
    if formula is None:
        return 0
    expression = str(formula).upper()
    value = split_math(expression)

    i = 0
    for i, item in enumerate(value):
        for size in sizes:
            if item == size.upper():
            	key = sizes[size]['propName']
            	value[i] = getattr(bpy.context.scene.fp_size_table, key)

    value = "".join(str(v) for v in value)

    try:
        eval(value)
        if not math.isnan(eval(value)):
            return eval(value)
        else:
            return 0        
    except ValueError:
        return 0
    except Exception:
        return 0


def split_math(str):
    return re.split("([\(\)+-/*])", str.replace(" ", ""))
    
def location_to_expression(location):
    '''
    location_to_expression(location: tuple3f) -> str
    
    Получаем формулу в виде строчного расстояния, исходя из координат в 3д.
    '''
    return str(round(math.sqrt(location[0]**2 + location[1]**2), 2))
    
def location_to_angle(location):
    pass
