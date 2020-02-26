# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_parametrizer

from mathutils import Matrix
from bpy.props import CollectionProperty, PointerProperty, FloatVectorProperty, StringProperty, IntProperty, FloatProperty, EnumProperty
from bpy.types import PropertyGroup, Mesh, Object, Text
from bpy.utils import register_class, unregister_class
# from .parametrizer import Parametrizer


# class PARAMETRIZER_transform_orientation_property(PropertyGroup):
#     c00: FloatProperty(default=1.0)
#     c01: FloatProperty(default=0.0)
#     c02: FloatProperty(default=0.0)
#     c03: FloatProperty(default=0.0)
#
#     c10: FloatProperty(default=0.0)
#     c11: FloatProperty(default=1.0)
#     c12: FloatProperty(default=0.0)
#     c13: FloatProperty(default=0.0)
#
#     c20: FloatProperty(default=0.0)
#     c21: FloatProperty(default=0.0)
#     c22: FloatProperty(default=1.0)
#     c23: FloatProperty(default=0.0)
#
#     c30: FloatProperty(default=0.0)
#     c31: FloatProperty(default=0.0)
#     c32: FloatProperty(default=0.0)
#     c33: FloatProperty(default=1.0)
#
#     def __repr__(self):
#         return '(({0},{1},{2},{3})\n({4},{5},{6},{7})\n({8},{9},{10},{11})\n({12},{13},{14},{15}))'.format(self.c00, self.c01, self.c01, self.c03, self.c10, self.c11, self.c12, self.c13, self.c20, self.c21, self.c22, self.c23, self.c30, self.c31, self.c32, self.c33)
#
#     @property
#     def matrix(self):
#         return (
#             (self.c00, self.c01, self.c02, self.c03),
#             (self.c10, self.c11, self.c12, self.c13),
#             (self.c20, self.c21, self.c22, self.c23),
#             (self.c30, self.c31, self.c32, self.c33),
#         )
#
#     @matrix.setter
#     def matrix(self, matrix4x4):
#         self.c00 = matrix4x4[0][0]
#         self.c01 = matrix4x4[0][1]
#         self.c02 = matrix4x4[0][2]
#         self.c03 = matrix4x4[0][3]
#         self.c10 = matrix4x4[1][0]
#         self.c11 = matrix4x4[1][1]
#         self.c12 = matrix4x4[1][2]
#         self.c13 = matrix4x4[1][3]
#         self.c20 = matrix4x4[2][0]
#         self.c21 = matrix4x4[2][1]
#         self.c22 = matrix4x4[2][2]
#         self.c23 = matrix4x4[2][3]
#         self.c30 = matrix4x4[3][0]
#         self.c31 = matrix4x4[3][1]
#         self.c32 = matrix4x4[3][2]
#         self.c33 = matrix4x4[3][3]
#
#
# class PARAMETRIZER_parameter_group(PropertyGroup):
#     name: StringProperty()
#     value: FloatProperty(
#         default=0.0,
#         update=lambda self, context: Parametrizer.on_parameter_change(self),
#         get=lambda self: self.on_value_get(self),
#         set=lambda self, value: self.on_value_set(value_property=self, new_value=value)
#     )
#     value_old: FloatProperty()
#     origin: FloatVectorProperty(
#         update=lambda self, context: Parametrizer.reset_value(self, context)
#     )
#     vertex_group_name: StringProperty(
#         default=''
#     )
#     axis: EnumProperty(
#         items=[
#             ('X', 'X', 'X'),
#             ('Y', 'Y', 'Y'),
#             ('Z', 'Z', 'Z'),
#         ],
#         default={'X', 'Y', 'Z'},
#         options={'ENUM_FLAG'},
#         update=lambda self, context: Parametrizer.reset_value(self, context)
#     )
#     mode: EnumProperty(
#         items=[
#             ('TRANSLATION', 'TRANSLATION', 'TRANSLATION'),
#             ('ROTATION', 'ROTATION', 'ROTATION'),
#             ('SCALE', 'SCALE', 'SCALE'),
#         ],
#         default='TRANSLATION',
#         update=lambda self, context: Parametrizer.reset_value(self, context)
#     )
#     transform_orientation_ptr: PointerProperty(
#         type=PARAMETRIZER_transform_orientation_property
#     )
#     parent_object: PointerProperty(
#         type=Object
#     )
#
#     @property
#     def transform_orientation(self):
#         return Matrix(self.transform_orientation_ptr.matrix)
#
#     @transform_orientation.setter
#     def transform_orientation(self, matrix4x4):
#         self.transform_orientation_ptr.matrix = matrix4x4
#         Parametrizer.reset_value(parameter=self, context=None)
#
#     @staticmethod
#     def on_value_get(value_property):
#         # on value get
#         return value_property['value']
#
#     @staticmethod
#     def on_value_set(value_property, new_value):
#         # on value set
#         value_property['value'] = new_value


def register():
    # register_class(PARAMETRIZER_transform_orientation_property)
    # register_class(PARAMETRIZER_parameter_group)
    # Mesh.parametrizer_params = CollectionProperty(type=PARAMETRIZER_parameter_group)
    # Mesh.parametrizer_active_param = IntProperty(
    #     name='active param',
    #     default=0
    # )
    Mesh.specification_text_link = PointerProperty(type=Text)


def unregister():
    del Mesh.specification_text_link
    # del Mesh.parametrizer_active_param
    # del Mesh.parametrizer_params
    # unregister_class(PARAMETRIZER_parameter_group)
    # unregister_class(PARAMETRIZER_transform_orientation_property)
