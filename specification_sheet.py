# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

import bpy

# ToDo - и для коллекций и понять как работает collection instance (is_instancer)


class SpecificationSheet:

    prefix = '_sp'

    @classmethod
    def objct_specification_text(cls, context, object_to_specificate):
        # show object specification text
        if object_to_specificate:
            text_object = cls.get_specification_text_object(object_to_specificate=object_to_specificate)
            # open in text editor
            text_editor_area = next(iter(area for area in context.screen.areas if area.type == 'TEXT_EDITOR'), None)
            if text_editor_area:
                text_editor_area.spaces.active.text = object_to_specificate.data.specification_text_link
            else:
                # ToDo create text editor area
                pass

    @classmethod
    def object_specification_active_to_other(cls, active_object, other: list):
        # copy specification text from active object to all other objects
        for object_to_specificate in other:
            if object_to_specificate != active_object and hasattr(object_to_specificate.data, 'specification_text_link'):
                text_object = cls.get_specification_text_object(
                    object_to_specificate=object_to_specificate
                )
                text_object.from_string(active_object.data.specification_text_link.as_string())


    @classmethod
    def get_specification_text_object(cls, object_to_specificate):
        # get text object for object_to_specificate
        if object_to_specificate.data.specification_text_link \
                and object_to_specificate.data.specification_text_link in bpy.data.texts[:]:
            text_object = object_to_specificate.data.specification_text_link
        else:
            text_object = bpy.data.texts.new(name=cls.prefix)
            object_to_specificate.data.specification_text_link = text_object
        return text_object
