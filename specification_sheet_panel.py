# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Panel, UIList
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
        box.label(text='Export')
        box.operator('specification_sheet.specification_to_csv', icon='EXPORT')
        box = layout.box()
        box.label(text='Specification fields')
        row = box.row()
        row.template_list('SPECIFICATION_SHEET_UL_presets_list', 'The_List', context.scene, 'specification_fields', context.scene, 'specification_active_field')
        col = row.column(align=True)
        col.operator('specification_sheet.add_new_field', icon='ADD', text='')
        col.operator('specification_sheet.remove_active_field', icon='REMOVE', text='')
        if context.active_object and hasattr(context.active_object.data, 'specification'):
            box = layout.box()
            box.label(text='Active Object')
            row = box.row()
            row.template_list('SPECIFICATION_SHEET_UL_object_fields', 'object_fields', context.active_object.data, 'specification', context.active_object.data, 'specification_active_field')
            col = row.column(align=True)
            col.operator('specification_sheet.object_active_to_selection', icon='CON_LOCLIKE', text='')


class SPECIFICATION_SHEET_UL_presets_list(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        layout.prop(data=item, property='field_name', text='', emboss=False)


class SPECIFICATION_SHEET_UL_object_fields(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        split = layout.split(factor=0.3)
        col = split.column()
        col.prop(data=item, property='name', text='', emboss=False)
        col = split.column()
        col.prop(data=item, property='value', text='')


def register():
    register_class(SPECIFICATION_SHEET_PT_panel)
    register_class(SPECIFICATION_SHEET_UL_presets_list)
    register_class(SPECIFICATION_SHEET_UL_object_fields)


def unregister():
    unregister_class(SPECIFICATION_SHEET_UL_object_fields)
    unregister_class(SPECIFICATION_SHEET_UL_presets_list)
    unregister_class(SPECIFICATION_SHEET_PT_panel)
