# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .specification_sheet import SpecificationSheet


class SPECIFICATION_SHEET_OT_object_specification_text(Operator):
    bl_idname = 'specification_sheet.object_specification_text'
    bl_label = 'Object specification text'
    bl_description = 'Open specification text'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # add specification text to active object
        SpecificationSheet.objct_specification_text(
            context=context,
            object_to_specificate=context.active_object
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object) \
               and hasattr(context.active_object.data, 'specification_text_link')


class SPECIFICATION_SHEET_OT_collection_specification_text(Operator):
    bl_idname = 'specification_sheet.collection_specification_text'
    bl_label = 'Collection specification text'
    bl_description = 'Open specification text'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # add specification text to active collection
        # ToDo
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.view_layer.active_layer_collection)


class SPECIFICATION_SHEET_OT_object_specification_to_selection(Operator):
    bl_idname = 'specification_sheet.object_specification_to_selection'
    bl_label = 'Active to selection'
    bl_description = 'Copy specification text from active object to all selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # copy specification text from active object to all the selection
        SpecificationSheet.object_specification_active_to_other(
            context=context,
            active_object=context.active_object,
            other=context.selected_objects
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.active_object) \
               and hasattr(context.active_object.data, 'specification_text_link') \
               and len(context.selected_objects) > 1


class SPECIFICATION_SHEET_OT_collection_specification_to_selection(Operator):
    bl_idname = 'specification_sheet.collection_specification_to_selection'
    bl_label = 'Active to selection'
    bl_description = 'Copy specification text from active collection to all selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # copy specification text from active collection to all the selection
        # ToDo
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return bool(context.view_layer.active_layer_collection)


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
        field_name = SpecificationSheet.add_new_specification_field(
            context=context
        )
        SpecificationSheet.add_field_to_specification_templates(
            field_name=field_name
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


def register():
    register_class(SPECIFICATION_SHEET_OT_object_specification_text)
    register_class(SPECIFICATION_SHEET_OT_collection_specification_text)
    register_class(SPECIFICATION_SHEET_OT_object_specification_to_selection)
    register_class(SPECIFICATION_SHEET_OT_collection_specification_to_selection)
    register_class(SPECIFICATION_SHEET_OT_specification_to_csv)
    register_class(SPECIFICATION_SHEET_OT_add_new_field)
    register_class(SPECIFICATION_SHEET_OT_remove_active_field)


def unregister():
    unregister_class(SPECIFICATION_SHEET_OT_remove_active_field)
    unregister_class(SPECIFICATION_SHEET_OT_add_new_field)
    unregister_class(SPECIFICATION_SHEET_OT_specification_to_csv)
    unregister_class(SPECIFICATION_SHEET_OT_collection_specification_to_selection)
    unregister_class(SPECIFICATION_SHEET_OT_object_specification_to_selection)
    unregister_class(SPECIFICATION_SHEET_OT_collection_specification_text)
    unregister_class(SPECIFICATION_SHEET_OT_object_specification_text)
