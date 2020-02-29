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

# ToDo - кнопка select all specificated (заполненно хоть одно поле)


class SpecificationSheet:

    _prefix = '_sp'
    _export_file_name = 'specification'
    _field_id = 0
    _csv_delimiter = ';'

    @classmethod
    def add_new_specification_field(cls, context, field_name=None, to_objects=True):
        # add specification field
        new_field = context.scene.specification_fields.add()
        if field_name:
            new_field.field_name = field_name
        else:
            new_field.field_name = cls.generate_new_field_name(fields=context.scene.specification_fields)
        if to_objects:
            # add new field to all objects
            for obj in cls._specificated_objects(context=context):
                if new_field.field_name not in (field.name for field in obj.specification):
                    object_field = obj.specification.add()
                    object_field.name = new_field.field_name
            # add new field to all collections
            # ToDo

    @classmethod
    def remove_specification_field(cls, context, field_id, from_objects=True):
        # remove specification field
        field_name = context.scene.specification_fields[field_id].field_name
        context.scene.specification_fields.remove(field_id)
        if from_objects:
            # remove from objects
            for obj in cls._specificated_objects(context=context):
                field_id = cls._id_by_name(name=field_name, fields=obj.specification)
                if field_id is not None:
                    obj.specification.remove(field_id)
            # remove from collections
            # ToDo

    @classmethod
    def on_rename_specification_field(cls, context, old_name, new_name):
        # specification field was renamed - change field name in all specification objects
        # objects
        for obj in cls._specificated_objects(context=context):
            for field in obj.specification:
                if field.name == old_name:
                    field.name = new_name
        # collections
        # ToDo

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
    def object_active_to_other(cls, context, active_object, other: list):
        # copy specification text from active object to all other objects
        objects = cls._specificated_objects(context=context, objects=other)
        if active_object.data in objects:
            objects.remove(active_object.data)
        for obj in objects:
            for field in active_object.data.specification:
                other_field = cls._field_by_name(name=field.name, fields=obj.specification)
                if other_field:
                    other_field.value = field.value

    @classmethod
    def export_to_csv(cls, context):
        # export specification to csv file
        specification_list = Counter(cls._specificated_objects(context=context, remove_instances=False))
        # write to csv file
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls._export_file_name + '.csv')
        try:
            with open(file=output_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=cls._csv_delimiter)
                # header
                writer.writerow(cls._export_header(context=context))
                # content
                for i, item in enumerate(dict(specification_list).items()):
                    writer.writerow([i + 1] + cls._export_row(context=context, fields=item[0].specification) + [item[1]])
        except IOError as error:
            bpy.ops.specification_sheet.messagebox('INVOKE_DEFAULT', message='Can\'t write to file!')

    @classmethod
    def _export_header(cls, context):
        # header for export specification table
        line_break = context.preferences.addons[__package__].preferences.line_break_char
        text_header = ['',] + [field.field_name.replace(line_break, '\n') for field in context.scene.specification_fields] + ['Amount',]
        return text_header

    @classmethod
    def _export_row(cls, context, fields):
        # row for export specification table
        line_break = context.preferences.addons[__package__].preferences.line_break_char
        row = [field.value.replace(line_break, '\n') if field.name in cls._specification_filds(context=context) else '' for field in fields]
        return row

    @staticmethod
    def _specificated_objects(context, objects=None, remove_instances=True):
        # return all objects with specification without instances
        if not objects:
            objects = context.scene.objects     # all from scene
        if remove_instances:
            return {obj.data for obj in objects if hasattr(obj.data, 'specification')}
        else:
            return (obj.data for obj in objects if hasattr(obj.data, 'specification'))

    @staticmethod
    def _specification_filds(context):
        # return specification field names
        return  (field.field_name for field in context.scene.specification_fields)

    @staticmethod
    def _id_by_name(name, fields):
        # return field id by field name
        return next((f[0] for f in enumerate(fields) if f[1].name == name), None)

    @staticmethod
    def _field_by_name(name, fields):
        # return field by field name
        return next((field for field in fields if field.name == name), None)

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
