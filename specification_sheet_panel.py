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
        layout = self.layout
        box = layout.box()
        box.label(text='Specification text to')
        row = box.row()
        row.operator('specification_sheet.object_specification_text', icon='FILE_TEXT', text='Active Object')
        row.operator('specification_sheet.object_specification_to_selection', icon='CON_LOCLIKE', text='')
        row = box.row()
        row.operator('specification_sheet.collection_specification_text', icon='FILE_TEXT', text='Active Collection')
        row.operator('specification_sheet.collection_specification_to_selection', icon='CON_LOCLIKE', text='')
        box = layout.box()
        box.label(text='Export')
        box.operator('specification_sheet.specification_to_csv', icon='EXPORT')


def register():
    register_class(SPECIFICATION_SHEET_PT_panel)


def unregister():
    unregister_class(SPECIFICATION_SHEET_PT_panel)
