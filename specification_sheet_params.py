# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty
from bpy.types import PropertyGroup, Mesh, Collection, Scene, WindowManager
from bpy.utils import register_class, unregister_class
from .specification_sheet import SpecificationSheet


class SPECIFICATION_SHEET_fields(PropertyGroup):

    field_name: StringProperty(
        default='field',
        update=lambda self, context: self._field_name_update(
            self=self,
            context=context
        )
    )

    field_name_old: StringProperty(
        default=''
    )

    @staticmethod
    def _field_name_update(self, context):
        # field_name update
        if self.field_name_old != '' and self.field_name != self.field_name_old:
            if [field.field_name for field in context.scene.specification_fields].count(self.field_name) > 1:
                # field name already existed
                self.field_name = self.field_name_old
            else:
                SpecificationSheet.on_rename_specification_field(
                    context=context,
                    old_name=self.field_name_old,
                    new_name=self.field_name
                )
        self.field_name_old = self.field_name


class SPECIFICATION_SHEET_object_fields(PropertyGroup):

    name: StringProperty(
        default=''
    )

    value: StringProperty(
        default=''
    )


def register():
    register_class(SPECIFICATION_SHEET_fields)
    register_class(SPECIFICATION_SHEET_object_fields)
    Mesh.specification = CollectionProperty(type=SPECIFICATION_SHEET_object_fields)
    Mesh.specification_active_field = IntProperty(
        default=0
    )
    Mesh.specification_skip = BoolProperty(
        description='Skip this object in specification the list',
        default=False
    )
    Collection.specification = CollectionProperty(type=SPECIFICATION_SHEET_object_fields)
    Collection.specification_active_field = IntProperty(
        default=0
    )
    Collection.specification_skip = BoolProperty(
        description='Skip this object in specification the list',
        default=False
    )
    Scene.specification_fields = CollectionProperty(type=SPECIFICATION_SHEET_fields)
    Scene.specification_active_field = IntProperty(
        default=0
    )
    WindowManager.specification_add_obj_names = BoolProperty(
        description='Add object names to specification list',
        default=False
    )
    WindowManager.specification_skip_empty = BoolProperty(
        description='Skip objects with empty specification fields',
        default=False
    )


def unregister():
    del WindowManager.specification_add_obj_names
    del Scene.specification_active_field
    del Scene.specification_fields
    del Collection.specification_skip
    del Collection.specification_active_field
    del Collection.specification
    del Mesh.specification_skip
    del Mesh.specification_active_field
    del Mesh.specification
    unregister_class(SPECIFICATION_SHEET_object_fields)
    unregister_class(SPECIFICATION_SHEET_fields)
