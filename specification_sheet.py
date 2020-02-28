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

    _prefix = '_sp'
    _export_file_name = 'specification'
    _field_id = 0
    _csv_delimiter = ';'

    @classmethod
    def objct_specification_text(cls, context, object_to_specificate):
        # show object specification text
        if object_to_specificate:
            text_object = cls.get_specification_text_object(
                context=context,
                object_to_specificate=object_to_specificate
            )
            # open in text editor
            text_editor_area = next(iter(area for area in context.screen.areas if area.type == 'TEXT_EDITOR'), None)
            if not text_editor_area:
                bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.25)
                text_editor_area = context.screen.areas[-1]
                text_editor_area.type = 'TEXT_EDITOR'
            text_editor_area.spaces.active.text = object_to_specificate.data.specification_text_link

    @classmethod
    def object_specification_active_to_other(cls, context, active_object, other: list):
        # copy specification text from active object to all other objects
        if active_object.data.specification_text_link:
            for object_to_specificate in other:
                if object_to_specificate != active_object and hasattr(object_to_specificate.data, 'specification_text_link'):
                    text_object = cls.get_specification_text_object(
                        context=context,
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
            new_field.field_name = cls.generate_new_field_name(fields=context.scene.specification_fields)
        return new_field.field_name

    @classmethod
    def generate_new_field_name(cls, fields):
        # generate new field name
        cls._field_id += 1
        field_name = 'field.' + str(cls._field_id).zfill(3)
        existed_field_names = (field.field_name for field in fields)
        while field_name in existed_field_names:
            cls._field_id += 1
            field_name = 'field.' + str(cls._field_id).zfill(3)
        return field_name

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
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls._export_file_name + '.csv')
        try:
            with open(file=output_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=cls._csv_delimiter)
                # header
                writer.writerow(cls._specification_header_template(context=context))
                # content
                for i, item in enumerate(dict(specification_list).items()):
                    writer.writerow([i + 1, item[0].as_string(), item[1]])
        except IOError as error:
            bpy.ops.specification_sheet.messagebox('INVOKE_DEFAULT', message='Can\'t write to file!')

    @classmethod
    def get_specification_text_object(cls, context, object_to_specificate):
        # get text object for object_to_specificate
        if object_to_specificate.data.specification_text_link \
                and object_to_specificate.data.specification_text_link in bpy.data.texts[:]:
            text_object = object_to_specificate.data.specification_text_link
        else:
            # create new
            text_object = bpy.data.texts.new(name=cls._prefix)
            text_object.from_string(cls._specification_text_template(context=context))
            object_to_specificate.data.specification_text_link = text_object
        return text_object

    @classmethod
    def _specification_header_template(cls, context):
        # fields for header for specification table
        text_header = ['',] + [field.field_name for field in context.scene.specification_fields] + ['',]
        return text_header

    @classmethod
    def _specification_text_template(cls, context):
        # generate text template for item specification
        text_template = ''
        for field in context.scene.specification_fields:
            text_template += ('\n' if text_template else '') + cls._format_field_name(field_name=field.field_name)
        return text_template

    @staticmethod
    def _format_field_name(field_name):
        # return formatted field name for specification template
        return '@' + field_name + ':'

    @classmethod
    def add_field_to_specification_templates(cls, field_name):
        # add new field name to specification text objects
        specification_text_objects = (text_object for text_object in bpy.data.texts if cls._prefix in text_object.name)
        for text_object in specification_text_objects:
            if cls._format_field_name(field_name=field_name) not in text_object.as_string():
                text_object.from_string(
                    string=text_object.as_string() + ('\n' if text_object.as_string() else '') + cls._format_field_name(field_name=field_name)
                )

    @classmethod
    def change_field_in_specification_templates(cls, old_name, new_name):
        # change field name in all specification text objects
        specification_text_objects = (text_object for text_object in bpy.data.texts if cls._prefix in text_object.name)
        for text_object in specification_text_objects:
            text_object.from_string(
                string=text_object.as_string().replace(
                    cls._format_field_name(field_name=old_name),
                    cls._format_field_name(field_name=new_name)
                )
            )

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
