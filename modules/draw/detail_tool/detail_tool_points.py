import bpy

from functools import reduce

from fashion_project.modules.draw.base import Base
from fashion_project.modules.draw.counter import Counter
from fashion_project.modules.draw.points import is_one_of_points 
from fashion_project.modules.utils import get_point_abs_location
from fashion_project.modules.utils import mouse,  fp_expression
from mathutils import Vector
import math


class ToolDetail(Base):
  FP_TYPE = 'fp.draw.detail_tool.tool_detail'
  CURVE_DIMS = '3D'
  CURVE_BEVEL_DEPTH = 0.01
  CURVE_FILL_MODE = 'FULL'
  STROKE_COLOR = (0.2, 0.7, 0.7)
  GUIDE_COLOR = (0.9, 0.1, 0.1)
  HANDLE_COLOR = (0.8, 0.0, 0.0)
  HANDLE_RADIUS = 0.05
  
  def poll(self, context):
    '''
    Требует двух выделенных точек.
    '''
    return (
      len(bpy.context.selected_objects) > 2
      and
      all([is_one_of_points(obj) for obj in bpy.context.selected_objects])
    )
    
  def create(self, context):
    locations = [];
    f_ids = [];
    # test call
     

    for d in context.selected_objects:
      locations.append(d.location)
      print(d.location) 
    locations.append(locations[0])  
    cList = locations

    for d in context.selected_objects:
        d.select = False

    bpy.ops.object.modal_operator('INVOKE_DEFAULT') 
    ##self.MakePolyLine(cList,context)

    # context.selected_objects  

    # obj.fp_deps = tuple([item.fp_id for item in context.selected_objects] + [0])  
    # locations = [
    #   get_point_abs_location(item) for item in bpy.data.objects
    #   if item.fp_id > 0 and item.fp_id in obj.fp_deps
    # ]
    # obj.location = [
    #   (locations[0][j] + locations[1][j])/2
    #   for j in range(3)
    # ]  

  def prepare_locations(self,clist):
    
    locations = [];
    for d in clist:
      locations.append(d.location)
      print(d.location) 
    locations.append(locations[0])
    print('locations',locations)
    self.MakePolyLine(self,locations,clist)

    #self.MakePolyLine(locations)  
    # curve = bpy.data.curves.new(name="КриваяБезье", type="CURVE")
    # curve.dimensions = self.CURVE_DIMS
    # curve.bevel_depth = self.CURVE_BEVEL_DEPTH
    # curve.bevel_resolution = 12
    # curve.fill_mode = self.CURVE_FILL_MODE
    # curve_mat = bpy.data.materials.new('ОбводкаКривойБезье')
    # curve_mat.diffuse_color = self.STROKE_COLOR
    # curve.materials.append(curve_mat)
    # obj = bpy.data.objects.new("КриваяБезье", curve)
    # obj.location = (0,0,0)
    # obj.lock_location = (True, True, True)
    # obj.show_name = True
    # context.scene.objects.link(obj)
    # Counter.register(obj, self.FP_TYPE)
    # obj.fp_deps = tuple([item.fp_id for item in context.selected_objects] + [0])
    # spline = curve.splines.new('BEZIER')
    # spline.bezier_points.add(1)
    # curve.resolution_u = 64
    # locations = [
    #   get_point_abs_location(item) for item in bpy.data.objects
    #   if item.fp_id > 0 and item.fp_id in obj.fp_deps
    # ]
    # obj.location = [
    #   (locations[0][j] + locations[1][j])/2
    #   for j in range(3)
    # ]
    # for index, loc in enumerate(locations):
    #   point_loc = [loc[i] - obj.location[i] for i in range(3)]
    #   obj.data.splines[0].bezier_points[index].co = point_loc 
    #   obj.data.splines[0].bezier_points[index].handle_left = [(point_loc[i] - 1.0 if i == 1 else point_loc[i]) for i in range(3)]
    #   obj.data.splines[0].bezier_points[index].handle_right = [(point_loc[i] + 1.0 if i == 1 else point_loc[i]) for i in range(3)]
    

  def MakePolyLine(self,cList,objects):
    curve = bpy.data.curves.new(name="Деталь", type='CURVE')  
    curve.dimensions = '3D'  
    curve.resolution_u = 2
    curve.dimensions = self.CURVE_DIMS
    curve.bevel_depth = self.CURVE_BEVEL_DEPTH
    curve.bevel_resolution = 12
    curve.fill_mode = self.CURVE_FILL_MODE
    curve_mat = bpy.data.materials.new('ОбводкаДетали')
    curve_mat.diffuse_color = self.STROKE_COLOR
    curve.materials.append(curve_mat)

    objectdata = bpy.data.objects.new("Деталь", curve)  
    
    for item in objects:
      prop = objectdata.fp_deps_c.add()
      prop.name = 'new'
      prop.value = str(item.fp_id)
    objectdata.location = (0,0,0) #object origin 
    objectdata.show_name = True
    bpy.context.scene.objects.link(objectdata)  
    Counter.register(objectdata, self.FP_TYPE)
  
    polyline = curve.splines.new('POLY')  
    polyline.points.add(len(cList)-1)  
    for num in range(len(cList)):  
        polyline.points[num].co = tuple(cList[num]) + (1,)
  
    polyline.order_u = len(polyline.points)-1
    polyline.use_endpoint_u = True    


  def update(self, obj, context):
      deps = []
      locations = []
      for x in obj.fp_deps_c:
          deps.append(int(x.value))

      print('deps',deps)


      for d in deps:
        for item in bpy.data.objects:
          if(item.fp_id == d):
              locations.append(Vector(get_point_abs_location(item)))

      locations.append(locations[0])  

      for index,location in enumerate(locations):
        obj.data.splines[0].points[index].co = tuple([c for i,c in enumerate(location)] + [0.001])
      
      print('update locations',locations)
      pass


class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"
    POINTS = []
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        pass
        #context.object.location.x = self.value / 100.0

    def modal(self, context, event):
        mouse.set_event(event) 
        
        if event.type == 'MOUSEMOVE':  # Apply
          pass
            #self.value = event.mouse_x
            #self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            print('self.POINTS')
            print(self.POINTS)
            ToolDetail.prepare_locations(ToolDetail,self.POINTS)
            return {'FINISHED'}
        elif event.type == 'RIGHTMOUSE':  # Cancel
            # print(dir(event))
            # print(event.value)
            if(event.value == 'RELEASE'):
              self.check_find_point(mouse.get_coords_location_3d())

            #print(event)
            # print('context.selected_objects')
            # print(context.selected_objects)
            # print('event.mouse_x '+str(event.mouse_x))
            # print(mouse.get_coords_location_3d())
            # print('event.mouse_y '+str(event.mouse_y))
            #bpy.data.objects["Точка.004"].select = True 
            
            #return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.value = event.mouse_x
        self.execute(context)

        print(context.window_manager.modal_handler_add(self))
        return {'RUNNING_MODAL'}


    def check_find_point(self,coords):
      print('find coors',coords)
      #print(coords)

      for ob in bpy.data.objects:
        print('ob.location',ob.location, ob.name)
        if(math.fabs(ob.location[0] - coords[0]) < 0.1) & (math.fabs(ob.location[1] - coords[1]) < 0.1):
          ob.select = True
          self.POINTS.append(ob)
          print('self.points')
          print(self.POINTS)
          return ob      

bpy.utils.register_class(ModalOperator)
