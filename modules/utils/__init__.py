
def get_point_abs_location(point):
  parent_location = get_point_abs_location(point.parent) if point.parent else (0.0,0.0,0.0)
  return tuple([c + parent_location[i] for i,c in enumerate(point.location)])