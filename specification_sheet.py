# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_specification_sheet

import bpy
from collections import Counter
import csv
import os
import tempfile

# ToDo - и для коллекций и понять как работает collection instance (is_instancer)


class SpecificationSheet:

    prefix = '_sp'
    export_file_name = 'specification'
    _field_id = 0

    @classmethod
    def objct_specification_text(cls, context, object_to_specificate):
        # show object specification text
        if object_to_specificate:
            text_object = cls.get_specification_text_object(object_to_specificate=object_to_specificate)
            # open in text editor
            text_editor_area = next(iter(area for area in context.screen.areas if area.type == 'TEXT_EDITOR'), None)
            if not text_editor_area:
                bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.25)
                text_editor_area = context.screen.areas[-1]
                text_editor_area.type = 'TEXT_EDITOR'
            text_editor_area.spaces.active.text = object_to_specificate.data.specification_text_link

    @classmethod
    def object_specification_active_to_other(cls, active_object, other: list):
        # copy specification text from active object to all other objects
        if active_object.data.specification_text_link:
            for object_to_specificate in other:
                if object_to_specificate != active_object and hasattr(object_to_specificate.data, 'specification_text_link'):
                    text_object = cls.get_specification_text_object(
                        object_to_specificate=object_to_specificate
                    )
                    text_object.from_string(active_object.data.specification_text_link.as_string())

    @classmethod
    def add_new_specification_field(cls, context, field_name=None):
        # add specification field
        new_field = context.scene.specification_fields.add()
        if field_name:
            new_field.field_name = field_name
        else:
            cls._field_id += 1
            new_field.field_name = 'field.' + str(cls._field_id).zfill(3)

    @classmethod
    def remove_specification_field(cls, context, field_id):
        # remove specification field
        context.scene.specification_fields.remove(field_id)

    @classmethod
    def export_to_csv(cls, context):
        # export specification to csv file
        objects_with_specification = (obj.data.specification_text_link for obj in context.scene.objects if hasattr(obj.data, 'specification_text_link') and obj.data.specification_text_link)
        # join by instances
        specification_list = Counter(objects_with_specification)
        # write to csv file
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls.export_file_name + '.csv')
        with open(file=output_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for i, item in enumerate(dict(specification_list).items()):
                writer.writerow([i + 1, item[0].as_string(), item[1]])

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

    @staticmethod
    def output_path(path):
        # returns absolute file path for output
        if not path:
            output_path = tempfile.gettempdir()
        if path[:2] == '//':
            output_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), path[2:]))
        else:
            output_path = os.path.abspath(path)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        return output_path
