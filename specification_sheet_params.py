# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.props import CollectionProperty, PointerProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup, Mesh, Text, Scene
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
                SpecificationSheet.change_field_in_specification_templates(
                    old_name=self.field_name_old,
                    new_name=self.field_name
                )
        self.field_name_old = self.field_name


def register():
    register_class(SPECIFICATION_SHEET_fields)
    Mesh.specification_text_link = PointerProperty(type=Text)
    Scene.specification_fields = CollectionProperty(type=SPECIFICATION_SHEET_fields)
    Scene.specification_active_field = IntProperty(
        default=0
    )


def unregister():
    del Scene.specification_fields
    del Mesh.specification_text_link
    unregister_class(SPECIFICATION_SHEET_fields)
