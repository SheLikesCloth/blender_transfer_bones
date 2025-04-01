bl_info = {
    "name": "Transfer Missing Bones",
    "author": "NotAZebra or SheLikesCloth",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "3D View > Armature",
    "description": "Adds bones to the active (recipient) armature if they are found in the non-active donor armature but not in the active recipient armature",
    "category": "Armature",
}

import bpy

class ARMATURE_OT_transfer_missing_bones(bpy.types.Operator):
    """Add bones from donor armature to recipient armature if not already present"""
    bl_idname = "armature.transfer_missing_bones"
    bl_label = "Transfer Missing Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']

        if len(sel_objs) != 2:
            self.report({'ERROR'}, "Select exactly two armature objects.")
            return {'CANCELLED'}

        active_obj = context.view_layer.objects.active
        if active_obj not in sel_objs:
            self.report({'ERROR'}, "Active object must be one of the selected armatures.")
            return {'CANCELLED'}

        # Active object is the recipient
        recipient = active_obj
        # Other selected objwect is the donor
        donor = (sel_objs[0] if sel_objs[0] != recipient else sel_objs[1])

        # # Must both be armature objects
        # if donor.type != 'ARMATURE' or recipient.type != 'ARMATURE':
        #     self.report({'ERROR'}, "Both donor and recipient must be armature objects.")
        #     return {'CANCELLED'}

        # Gather donor bone info (Edit Mode)
        bpy.ops.object.mode_set(mode='OBJECT')
        donor.select_set(True)
        context.view_layer.objects.active = donor
        bpy.ops.object.mode_set(mode='EDIT')

        donor_bones = {}
        for dbone in donor.data.edit_bones:
            parent_name = dbone.parent.name if dbone.parent else None
            donor_bones[dbone.name] = {
                'head': dbone.head.copy(),
                'tail': dbone.tail.copy(),
                'roll': dbone.roll,
                'parent_name': parent_name
            }

        bpy.ops.object.mode_set(mode='OBJECT')
        donor.select_set(False)

        # Add missing bones to recipient
        recipient.select_set(True)
        context.view_layer.objects.active = recipient
        bpy.ops.object.mode_set(mode='EDIT')

        recip_bones = recipient.data.edit_bones
        existing_names = {bone.name for bone in recip_bones}

        for bone_name, info in donor_bones.items():
            if bone_name not in existing_names:
                new_bone = recip_bones.new(bone_name)
                new_bone.head = info['head']
                new_bone.tail = info['tail']
                new_bone.roll = info['roll']
                if info['parent_name'] in recip_bones:
                    new_bone.parent = recip_bones[info['parent_name']]

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Added missing bones from donor to recipient.")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_transfer_missing_bones.bl_idname, text="Transfer Missing Bones")

def register():
    bpy.utils.register_class(ARMATURE_OT_transfer_missing_bones)
    # Append to Armature menu
    # Could change this
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
    bpy.utils.unregister_class(ARMATURE_OT_transfer_missing_bones)

if __name__ == "__main__":
    register()
