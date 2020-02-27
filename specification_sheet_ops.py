# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Operator
from bpy.props import EnumProperty
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


def register():
    register_class(SPECIFICATION_SHEET_OT_object_specification_text)
    register_class(SPECIFICATION_SHEET_OT_collection_specification_text)
    register_class(SPECIFICATION_SHEET_OT_object_specification_to_selection)
    register_class(SPECIFICATION_SHEET_OT_collection_specification_to_selection)
    register_class(SPECIFICATION_SHEET_OT_specification_to_csv)


def unregister():
    unregister_class(SPECIFICATION_SHEET_OT_specification_to_csv)
    unregister_class(SPECIFICATION_SHEET_OT_collection_specification_to_selection)
    unregister_class(SPECIFICATION_SHEET_OT_object_specification_to_selection)
    unregister_class(SPECIFICATION_SHEET_OT_collection_specification_text)
    unregister_class(SPECIFICATION_SHEET_OT_object_specification_text)
