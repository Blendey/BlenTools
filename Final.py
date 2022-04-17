bl_info = {
    "name": "BlenTools",
    "author": "Blendey",
    "version": (2, 1),
    "blender": (3, 2, 0),
    "location": "In the search menu",
    "description": "A collection of random macro's/presets",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy

# This script is basically a bunch of usefull macros/presets. The code is pretty messy, but it works (when you use it the right way), and that was my goal.

import bpy
def load(): # this is part of the vertexmixer, it can store vertex groups in your file, so you can use normalize and auto normalize on the remaining (bone) vertex groups.
    # Make sure we are in Object Mode
    if bpy.context.object.mode == "EDIT":
        bpy.ops.object.mode_set(mode="OBJECT")
    # Duplicate the object, give it the old name with the _vertexgroupunedited suffix.
    oldname = bpy.context.object.name
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    newname = oldname + "_vertexgroupunedited"
    bpy.context.object.name = newname
    
    # Remove all the unlocked vertex groups
    bpy.ops.object.vertex_group_remove(all_unlocked=True)
    
    # Hide the helper object
    bpy.context.object.hide_viewport = True
    
    # Select the original object and delete the transferred vertex group(s)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[oldname]
    bpy.context.scene.objects[oldname].select_set(True)
    bpy.ops.object.vertex_group_lock(action='INVERT', mask='ALL')
    bpy.ops.object.vertex_group_remove(all_unlocked=True)
    bpy.ops.object.vertex_group_lock(action='UNLOCK', mask='ALL')
    
    # Return the name of the original object
    return oldname
    
def smesh(): # this is part of the vertexmixer, it can store vertex groups in your file, so you can use normalize and auto normalize on the remaining (bone) vertex groups.
    oldname = bpy.context.object.name
    # Add the Data Transfer modifier to the old object, and transfer the unedited vertex
    # group(s) back to the original mesh
    newname = oldname + "_vertexgroupunedited"
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[oldname]
    bpy.context.scene.objects[oldname].select_set(True)
    
    # Add the modifier
    bpy.ops.object.modifier_add(type='DATA_TRANSFER')
    
    # Configure settings from modifier
    bpy.context.object.modifiers["DataTransfer"].object = bpy.data.objects[newname]
    bpy.context.object.modifiers["DataTransfer"].vert_mapping = 'TOPOLOGY'
    bpy.context.object.modifiers["DataTransfer"].data_types_verts = {'VGROUP_WEIGHTS'}
    bpy.ops.object.datalayout_transfer(modifier="DataTransfer")
    
    # Apply the modifier
    bpy.ops.object.modifier_apply(modifier="DataTransfer", report=False)
    
    # Select the helper object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[newname]
    bpy.context.scene.objects[newname].select_set(True)
    
    # Unhide the helper object and delete it
    bpy.context.object.hide_viewport = False
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[newname]
    bpy.context.scene.objects[newname].select_set(True)
    bpy.ops.object.delete()
    print(newname)
    
    # Select the original object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[oldname]
    bpy.context.scene.objects[oldname].select_set(True)
    
def retoposetup(): # This function will setup a retopo setup...
    # make sure we are in object mode
    if bpy.context.object.mode == "EDIT":
        bpy.ops.object.mode_set(mode="OBJECT")
    oldnameretopowithoutold = bpy.context.object.name
    bpy.context.object.name = bpy.context.object.name + "_old"
    oldretopo = bpy.context.active_object
    oldnameretopo = bpy.context.object.name
    
    # Add a plane for retopology
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.name = oldnameretopowithoutold + "_retopo"
    newname = bpy.context.object.name
    
    # Enable some snapping settings
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_elements = {'FACE'}
    
    # Configure the shrinkwrap modifier
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = oldretopo
    
    # Apply the scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Do some extra random stuff
    bpy.ops.object.editmode_toggle()
    bpy.context.space_data.shading.light = 'MATCAP'
    bpy.context.space_data.shading.studio_light = 'clay_brown.exr'
    bpy.ops.view3d.toggle_xray()

def easyIK():
    bpy.ops.pose.constraint_add(type='IK')
    Skelet = bpy.context.view_layer.objects.active
    IKbot = 'Bone'
    Skelet.pose.bones[IKbot].constraints['IK'].target = Skelet
    Skelet.pose.bones[IKbot].constraints['IK'].subtarget = 'HeelIK.L'
    Skelet.pose.bones[IKbot].constraints['IK'].pole_target = Skelet
    Skelet.pose.bones[IKbot].constraints['IK'].pole_subtarget = 'KneeTarget.L'
    bpy.ops.pose.constraint_add(type='COPY_ROTATION')
    bpy.context.object.pose.bones[IKbot].constraints["IK"].chain_count = 2
    
def RemoveUv():
    selected_objects = bpy.context.selected_objects

    uvmap = 'UVMap'
    for obj in selected_objects:
       if obj.type == "MESH":
         uvlayer = obj.data.uv_layers.get(uvmap)
         if uvlayer != None:
           obj.data.uv_layers.remove(uvlayer)
           
class VertexSeperate(bpy.types.Operator):
    """VertexSeperate"""     
    bl_idname = "object.seperate"        
    bl_label = "VertexSeperate"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        load()
        return {'FINISHED'}
    
class VertexMix(bpy.types.Operator):
    """VertexMix"""     
    bl_idname = "object.mix"        
    bl_label = "VertexMix"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        smesh()
        return {'FINISHED'}
    
class RetopoSetup(bpy.types.Operator):
    """RetopoSetup"""     
    bl_idname = "object.retopo"        
    bl_label = "RetopoSetup"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        retoposetup()
        return {'FINISHED'}

class RemoveUV(bpy.types.Operator):
    """RemoveUV"""     
    bl_idname = "object.uvremove"        
    bl_label = "Remove UV"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        RemoveUv()
        return {'FINISHED'}
    
class SetEasyIK(bpy.types.Operator):
    """EasyIK"""     
    bl_idname = "pose.easyik"        
    bl_label = "EasyIK"         
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        easyIK()
        return {'FINISHED'}
    

def menu_func(self, context):
    self.layout.operator(VertexSeperate.bl_idname)
    self.layout.operator(VertexMix.bl_idname)
    self.layout.operator(RetopoSetup.bl_idname)
    self.layout.operator(SetEasyIK.bl_idname)
    self.layout.operator(RemoveUV.bl_idname)

def register():
    bpy.utils.register_class(VertexSeperate)
    bpy.utils.register_class(VertexMix)
    bpy.utils.register_class(RetopoSetup)
    bpy.utils.register_class(SetEasyIK)
    bpy.utils.register_class(RemoveUV)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(VertexSeperate)
    bpy.utils.unregister_class(VertexMix)
    bpy.utils.unregister_class(RetopoSetup)
    bpy.utils.unregister_class(SetEasyIK)
    bpy.utils.unregister_class(RemoveUV)



if __name__ == "__main__":
    register()
