# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class SPECIFICATION_SHEET_PT_panel(Panel):
    bl_idname = 'SPECIFICATION_SHEET_PT_panel'
    bl_label = 'Sp-Sheet'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Sp-Sheet'

    def draw(self, context):
        self.layout.operator('specification_sheet.main', icon='BLENDER', text='specification_sheet execute')


def register():
    register_class(SPECIFICATION_SHEET_PT_panel)


def unregister():
    unregister_class(SPECIFICATION_SHEET_PT_panel)
