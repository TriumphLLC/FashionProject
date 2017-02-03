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
						# self.value = event.mouse_x
						# self.execute(context)
				elif event.type == 'LEFTMOUSE':  # Confirm
						print('self.POINTS')
						print(self.POINTS)
						#ToolDetail.prepare_locations(ToolDetail,self.POINTS)
						ToolDetail.make_bezier(ToolDetail,self.POINTS)  
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