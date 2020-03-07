# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


class SPECIFICATION_SHEET_preferences(AddonPreferences):

    bl_idname = __package__

    line_break_char: StringProperty(
        name='Line break character',
        default='#'
    )

    output_font_name: StringProperty(
        name='Output font name',
        default='PT Sans'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'line_break_char')
        layout.prop(self, 'output_font_name')


def register():
    register_class(SPECIFICATION_SHEET_preferences)


def unregister():
    unregister_class(SPECIFICATION_SHEET_preferences)
