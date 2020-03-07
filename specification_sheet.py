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
                    field = obj.specification.add()
                    field.name = new_field.field_name
            # add new field to all collections
            for collection in cls._scene_collections(context=context):
                if new_field.field_name not in (field.name for field in collection.specification):
                    field = collection.specification.add()
                    field.name = new_field.field_name

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
            for collection in cls._scene_collections(context=context):
                field_id = cls._id_by_name(name=field_name, fields=collection.specification)
                if field_id is not None:
                    collection.specification.remove(field_id)

    @classmethod
    def fields_to_objects(cls, context):
        # translate specification fields to objects
        # objects
        for sp_object in cls._specificated_objects(context=context):
            for field in context.scene.specification_fields:
                cls._add_field_to_object(sp_object=sp_object, field_name=field.field_name)
        # collections
        for collection in cls._scene_collections(context=context):
            for field in context.scene.specification_fields:
                cls._add_field_to_object(sp_object=collection, field_name=field.field_name)

    @classmethod
    def on_rename_specification_field(cls, context, old_name, new_name):
        # specification field was renamed - change field name in all specification objects
        # objects
        for obj in cls._specificated_objects(context=context):
            for field in obj.specification:
                if field.name == old_name:
                    field.name = new_name
        # collections
        for collection in cls._scene_collections(context=context):
            for field in collection.specification:
                if field.name == old_name:
                    field.name = new_name

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

    @staticmethod
    def _add_field_to_object(sp_object, field_name):
        # add new specification field to object/collection
        if field_name not in (field.name for field in sp_object.specification):
            field = sp_object.specification.add()
            field.name = field_name

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
    def object_select_empty(cls, context):
        # select all objects with empty specification fields
        for obj in bpy.data.objects:
            if hasattr(obj.data, 'specification') and cls._empty(obj.data.specification):
                obj.select_set(True)
            else:
                obj.select_set(False)

    @classmethod
    def export_to_csv(cls, context):
        # export specification to csv file
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls._export_file_name + '.csv')
        try:
            with open(file=output_path, mode='w', newline='', encoding='utf8') as csv_file:
                writer = csv.writer(csv_file, delimiter=cls._csv_delimiter)
                for row in cls._export_body(context=context):
                    writer.writerow(row)
        except IOError as error:
            bpy.ops.specification_sheet.messagebox('INVOKE_DEFAULT', message='Can\'t write to file!')

    @classmethod
    def export_to_html(cls, context):
        # export specification to html file
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls._export_file_name + '.html')
        # html file
        try:
            with open(file=output_path, mode='w', newline='', encoding='utf8') as html_file:
                html_body = '<html>'
                html_body += '<head>'
                html_body += '<title>' + 'Project specification' + '</title>'
                html_body += '<meta http-equiv="content-type" content="text/html; charset = utf-8">'
                html_body += '<link href="specification.css" type="text/css" rel="stylesheet">'
                html_body += '<link href="https://fonts.googleapis.com/css?family=' \
                             + context.preferences.addons[__package__].preferences.output_font_name.replace(' ', '+') \
                             + '" type="text/css" rel="stylesheet">'
                html_body += '</head>'
                html_body += '<body>'
                html_body += '<div class="sp_title">Table of specification</div>'
                if context.window_manager.specification_add_project_info:
                    html_body += '<div class="sp_project_name">Blender project: ' + os.path.splitext(os.path.basename(bpy.data.filepath))[0] + '</div>'
                    html_body += '<div class="sp_project_filepath">File: ' + os.path.abspath(bpy.data.filepath) + '</div>'
                html_body += '<table class="sp_table">'
                for row in cls._export_body(context=context):
                    html_body += '<tr>'
                    for cell in row:
                        html_body += '<td>' if row[0] else ('<th class="' + (cell.lower() if cell else 'number') + '">')
                        html_body += str(cell).replace('\n', '<br>')
                        html_body += '</td>' if row[0] else '</th>'
                    html_body += '</tr>'
                html_body += '</table>'
                html_body += '</body>'
                html_body += '</html>'
                # write to file
                html_file.write(html_body)
        except IOError as error:
            bpy.ops.specification_sheet.messagebox('INVOKE_DEFAULT', message='Can\'t write to file!')
        # css file
        output_path = os.path.join(cls.output_path(path=context.scene.render.filepath), cls._export_file_name + '.css')
        try:
            with open(file=output_path, mode='w', newline='', encoding='utf8') as css_file:
                css_body = 'body{font-family: "' + context.preferences.addons[__package__].preferences.output_font_name + '"; margin: 5px;}'
                css_body += '.sp_title{text-align: center; font-weight: bold; margin: 25px}'
                css_body += '.sp_project_name, .sp_project_filepath {width: 90%; display: block; margin-left: auto; margin-right: auto; margin-bottom: 10px}'
                css_body += '.sp_table{width: 90%; border: 1px solid black; margin: 0 auto;}'
                css_body += '.sp_table th {border: 1px solid black;}'
                css_body += '.sp_table td {border: 1px solid black;}'
                css_body += '.sp_table .number {width: 30px;}'
                css_body += '.sp_table .amount {width: 60px;}'
                for cell in cls._export_header(context=context):
                    css_body += '.sp_table .' + cell.lower() + ' {width: ' + str(cls._specification_field_by_name(cell, context.scene.specification_fields).width) + '%}'
                # write to file
                css_file.write(css_body)
        except IOError as error:
            bpy.ops.specification_sheet.messagebox('INVOKE_DEFAULT', message='Can\'t write to file!')

    @classmethod
    def _export_header(cls, context):
        # header for export specification table
        line_break = context.preferences.addons[__package__].preferences.line_break_char
        text_header = [field.field_name.replace(line_break, '\n') for field in context.scene.specification_fields]
        return text_header

    @classmethod
    def _export_row(cls, context, fields):
        # row for export specification table
        line_break = context.preferences.addons[__package__].preferences.line_break_char
        row = [field.value.replace(line_break, '\n') if field.name in cls._specification_fields(context=context) else '' for field in fields]
        return row

    @classmethod
    def _export_body(cls, context):
        # table body fro export specification
        object_names = context.window_manager.specification_add_obj_names
        # header
        header = ['',] + cls._export_header(context=context) + ['Amount',]
        if object_names:
            header.insert(1, 'Objects')
        # body
        body = []
        # objects with counted instances
        number = 1
        if 'OBJECTS' in context.window_manager.specification_object_types:
            sp_objects = Counter(cls._specificated_objects(context=context, remove_instances=False))
            for item in dict(sp_objects).items():
                if not item[0].specification_skip and not (context.window_manager.specification_skip_empty and cls._empty(item[0].specification)):
                    row = [number,] + cls._export_row(context=context, fields=item[0].specification) + [item[1],]
                    if object_names:
                        row.insert(1, item[0].name)
                    body.append(row)
                    number += 1
        # collections with counted instances
        if 'COLLECTIONS' in context.window_manager.specification_object_types:
            sp_collection_instances = cls._collection_instances(context=context)
            sp_collection_instances_all = []
            for col in sp_collection_instances:
                sp_collection_instances_all += cls._collections_inner(collection=col)
            # collections + collection instances + inner collections in instances
            sp_collections = Counter(cls._scene_collections(context=context)) + \
                Counter(cls._collection_instances(context=context)) + \
                Counter(sp_collection_instances_all)
            for item in dict(sp_collections).items():
                if not item[0].specification_skip and not (context.window_manager.specification_skip_empty and cls._empty(item[0].specification)):
                    row = [number,] + cls._export_row(context=context, fields=item[0].specification) + [item[1],]
                    if object_names:
                        row.insert(1, item[0].name)
                    body.append(row)
                    number += 1
        return [header,] + body

    @staticmethod
    def _specificated_objects(context, objects=None, remove_instances=True):
        # return all objects with specification without instances
        if not objects:
            objects = bpy.data.objects     # all
        if remove_instances:
            return {obj.data for obj in objects if hasattr(obj.data, 'specification')}
        else:
            return (obj.data for obj in objects if hasattr(obj.data, 'specification'))

    @classmethod
    def _scene_collections(cls, context):
        # return all scene collections
        return (collection for collection in bpy.data.collections)

    @classmethod
    def _collection_instances(cls, context):
        # return all collections for collection instances
        return (c_instance.instance_collection for c_instance in bpy.data.objects if c_instance.instance_collection)

    @classmethod
    def _collections_all(cls, collection, col_list):
        # get all collections on all levels of collection
        col_list.append(collection)
        for sub_collection in collection.children:
            cls._collections_all(collection=sub_collection, col_list=col_list)

    @classmethod
    def _collections_inner(cls, collection):
        # get all inner collections on all levels of collection
        col_list = []
        cls._collections_all(collection=collection, col_list=col_list)
        return col_list[1:]

    @staticmethod
    def _specification_fields(context):
        # return specification field names
        return (field.field_name for field in context.scene.specification_fields)

    @staticmethod
    def _empty(fields):
        # check if all fields are empty
        return not bool(next((field.value for field in fields if field.value), None))

    @staticmethod
    def _id_by_name(name, fields):
        # return field id by field name
        return next((f[0] for f in enumerate(fields) if f[1].name == name), None)

    @staticmethod
    def _field_by_name(name, fields):
        # return field by field name
        return next((field for field in fields if field.name == name), None)

    @staticmethod
    def _specification_field_by_name(name, fields):
        # return specification field by field name
        return next((field for field in fields if field.field_name == name), None)

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
