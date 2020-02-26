# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

from . import specification_sheet_ops
from . import specification_sheet_panel
from .addon import Addon
from . import specification_sheet_params


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


def register():
    if not Addon.dev_mode():
        specification_sheet_params.register()
        specification_sheet_ops.register()
        specification_sheet_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        specification_sheet_panel.unregister()
        specification_sheet_ops.unregister()
        specification_sheet_params.unregister()


if __name__ == '__main__':
    register()
