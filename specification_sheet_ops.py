# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .specification_sheet import SpecificationSheet


class SPECIFICATION_SHEET_OT_object_active_to_selection(Operator):
    bl_idname = 'specification_sheet.object_active_to_selection'
    bl_label = 'Object: active to selection'
    bl_description = 'Copy specification text from active object to all selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # copy specification text from active object to all the selection
        SpecificationSheet.object_active_to_other(
            context=context,
            active_object=context.active_object,
            other=context.selected_objects
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object) \
               and hasattr(context.active_object.data, 'specification') \
               and len(context.selected_objects) > 1


class SPECIFICATION_SHEET_OT_specification_to_csv(Operator):
    bl_idname = 'specification_sheet.specification_to_csv'
    bl_label = 'CSV'
    bl_description = 'Save specificaton to CSV file'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # export specification to csv
        SpecificationSheet.export_to_csv(context=context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.view_layer.active_layer_collection)


class  SPECIFICATION_SHEET_OT_add_new_field(Operator):
    bl_idname = 'specification_sheet.add_new_field'
    bl_label = 'Add new field'
    bl_description = 'Add new specification field'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # add new specification field
        SpecificationSheet.add_new_specification_field(
            context=context,
            to_objects=True
        )
        return {'FINISHED'}


class  SPECIFICATION_SHEET_OT_remove_active_field(Operator):
    bl_idname = 'specification_sheet.remove_active_field'
    bl_label = 'Remove active field'
    bl_description = 'Remove active specification field'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove active specification field
        SpecificationSheet.remove_specification_field(
            context=context,
            field_id=context.scene.specification_active_field
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if 0 <= context.scene.specification_active_field < len(context.scene.specification_fields):
            return True
        else:
            return False


class  SPECIFICATION_SHEET_OT_fields_to_objects(Operator):
    bl_idname = 'specification_sheet.fields_to_objects'
    bl_label = 'Translate specification fields to objects'
    bl_description = 'Translate specification fields to objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # translate specification fields to objects
        SpecificationSheet.fields_to_objects(
            context=context
        )
        return {'FINISHED'}


def register():
    register_class(SPECIFICATION_SHEET_OT_object_active_to_selection)
    register_class(SPECIFICATION_SHEET_OT_specification_to_csv)
    register_class(SPECIFICATION_SHEET_OT_add_new_field)
    register_class(SPECIFICATION_SHEET_OT_remove_active_field)
    register_class(SPECIFICATION_SHEET_OT_fields_to_objects)


def unregister():
    unregister_class(SPECIFICATION_SHEET_OT_fields_to_objects)
    unregister_class(SPECIFICATION_SHEET_OT_remove_active_field)
    unregister_class(SPECIFICATION_SHEET_OT_add_new_field)
    unregister_class(SPECIFICATION_SHEET_OT_specification_to_csv)
    unregister_class(SPECIFICATION_SHEET_OT_object_active_to_selection)
