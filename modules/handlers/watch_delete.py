import bpy

from functools import reduce


class _FP_Cache():
  ids = set()
  parents = {}
  deps = {}
  
  def obj_by_fp_id(self, fp_id):
    return reduce(lambda res, item: item if item.fp_id == fp_id else res, bpy.data.objects, None)
  
  def set_ids(self, ids):
    self.ids = set(ids)
    
  def set_parents(self, objs):
    self.parents = {}
    for obj in objs:
      if obj.parent and obj.fp_id and obj.parent.fp_id:
        self.parents[obj.fp_id] = obj.parent.fp_id
  
  def get_children(self, obj):
    return self.parents[obj.fp_id]
    
  def set_deps(self, objs):
    self.deps = {}
    for obj in objs:
      deps = [d for d in obj.fp_deps if d != 0]
      if obj and obj.fp_id and len(deps):
        self.deps[obj.fp_id] = deps
        
  def get_deps(self, obj):
    return self.deps[obj.fp_id]
    
  def get_diffset(self, ids):
    if len(self.ids) == 0:
      return set()
    return set(ids) - self.ids
    
  def remove_obj(self, obj):
    bpy.context.scene.objects.unlink(obj)
    bpy.data.objects.remove(obj)
    
  def remove_obj_recur(self, obj):
    for item in [i for i in bpy.data.objects if i.fp_id > 0]:
      if self.parents.get(item.fp_id) == obj.fp_id:
        self.remove_obj_recur(item)
      deps = self.deps.get(item.fp_id)
      if deps and obj.fp_id in deps:
        self.remove_obj_recur(item)
    self.remove_obj(obj)
    
  
cache = _FP_Cache()

@bpy.app.handlers.persistent
def watch_del(_0):
  global cache
  current_fp_objects = tuple([item for item in bpy.data.objects if item.fp_id > 0 and item.fp_type])
  current_ids = set(map(lambda item: item.fp_id, current_fp_objects))
  diff_ids = cache.get_diffset(current_ids)
  # if len(diff_ids) > 0:
  #   print(diff_ids)
  #   for fp_id in diff_ids:
  #     cache.remove_obj_recur(cache.obj_by_fp_id(fp_id))
  cache.set_ids(current_ids)
  cache.set_parents(current_fp_objects)
  cache.set_deps(current_fp_objects)


def register():
  bpy.app.handlers.scene_update_post.append(watch_del)

def unregister():
  bpy.app.handlers.scene_update_post.remove(watch_del)
  