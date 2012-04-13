from colander import (SchemaNode, MappingSchema, SequenceSchema,
                      String, Int, Length, Range)

def normalize_string(string):
    """Remove whitespace and bring the string to lowercase"""
    return string.strip().lower()

class IngredientSchema(MappingSchema):
    product_title = SchemaNode(String(), validator=Length(3),
                               preparer=normalize_string)
    amount = SchemaNode(Int(), validator=Range(1))
    unit_title = SchemaNode(String(), validator=Length(3), missing=None)

class Ingredients(SequenceSchema):
    ingredient = IngredientSchema()

class StepSchema(MappingSchema):
    number = SchemaNode(Int(), validator=Range(1, 100))
    text = SchemaNode(String(), validator=Length(10))
    time_value = SchemaNode(Int())

class Steps(SequenceSchema):
    step = StepSchema()

class RecipeSchema(MappingSchema):
    title = SchemaNode(String(), validator=Length(3),
                       preparer=normalize_string)
    description = SchemaNode(String())
    steps = Steps()
    ingredients = Ingredients()