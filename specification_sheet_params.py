# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.props import CollectionProperty, PointerProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup, Mesh, Text, Scene
from bpy.utils import register_class, unregister_class


class SPECIFICATION_SHEET_fields(PropertyGroup):

    field_name: StringProperty(
        default='field'
    )


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
