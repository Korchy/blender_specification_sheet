# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class SPECIFICATION_SHEET_OT_main(Operator):
    bl_idname = 'specification_sheet.main'
    bl_label = 'specification_sheet: main'
    bl_description = 'specification_sheet - main operator'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print('specification_sheet.main')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def register():
    register_class(SPECIFICATION_SHEET_OT_main)


def unregister():
    unregister_class(SPECIFICATION_SHEET_OT_main)
