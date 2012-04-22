# -*- coding: utf-8 -*-

from colander import (SchemaNode, MappingSchema, SequenceSchema,
                      String, Int, Length, Range, Email, All, Function,
                      null)

def normalize_string(string):
    """Remove whitespace and bring the string to lowercase"""
    if string is not null:
        return string.strip().lower()
    else:
        return ''

def is_new_record(email):
    from models import User
    if User.fetch(email=email) is not None:
        return False
    else:
        return True

class IngredientSchema(MappingSchema):
    product_title = SchemaNode(String(), validator=Length(3),
                               preparer=normalize_string)
    amount = SchemaNode(Int(), validator=Range(1))
    unit_title = SchemaNode(String(), validator=Length(3), missing=None)

class Ingredients(SequenceSchema):
    ingredient = IngredientSchema()

class StepSchema(MappingSchema):
    number = SchemaNode(Int(), validator=Range(1, 100))
    text = SchemaNode(String())
    time_value = SchemaNode(Int(), validator=Range(1), missing=None)

class Steps(SequenceSchema):
    step = StepSchema()

class RecipeSchema(MappingSchema):
    title = SchemaNode(String(), validator=Length(3),
                       preparer=normalize_string)
    description = SchemaNode(String(), validator=Length(3), missing=None)
    steps = Steps()
    ingredients = Ingredients()

class UserSchema(MappingSchema):
    email = SchemaNode(String(), preparer=normalize_string,
                       validator=All(Email(msg=u'Неверный адрес email'),
                                     Function(is_new_record,
                                              message=u'Пользователь ${val} '
                                                      u'уже '
                                                      u'зарегистрирован')))
    password = SchemaNode(String(), validator=Length(6))