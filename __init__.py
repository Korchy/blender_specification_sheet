# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

import bpy
from bpy.app.handlers import persistent
import functools
from . import specification_sheet_ops
from . import specification_sheet_panel
from . import specification_sheet_params
from . import message_box
from .addon import Addon
from .specification_sheet import SpecificationSheet


bl_info = {
    'name': 'specification_sheet',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 82, 0),
    'location': 'N-Panel > Sp-Sheet',
    'wiki_url': '',
    'tracker_url': '',
    'description': 'Specification sheet generator'
}


@persistent
def specification_sheet_add_default_fields(context, scene):
    # add default specification fields
    if hasattr(bpy.context, 'scene'):
        if len(bpy.context.scene.specification_fields) == 0:
            SpecificationSheet.add_new_specification_field(
                context=bpy.context,
                field_name='description'
            )
            SpecificationSheet.add_new_specification_field(
                context=bpy.context,
                field_name='comments'
            )
    else:
        return 0.25


def register():
    if not Addon.dev_mode():
        specification_sheet_params.register()
        specification_sheet_ops.register()
        specification_sheet_panel.register()
        message_box.register()
        bpy.app.timers.register(functools.partial(specification_sheet_add_default_fields, bpy.context, None), first_interval=0.25)
        # reload presets list with scene load
        if specification_sheet_add_default_fields not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(specification_sheet_add_default_fields)
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        if specification_sheet_add_default_fields in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(specification_sheet_add_default_fields)
        message_box.unregister()
        specification_sheet_panel.unregister()
        specification_sheet_ops.unregister()
        specification_sheet_params.unregister()


if __name__ == '__main__':
    register()
