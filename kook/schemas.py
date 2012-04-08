from colander import (SchemaNode, MappingSchema, SequenceSchema,
                      String, Int, Length, Range)

class ProductTitles(SequenceSchema):
    product_title_node = SchemaNode(String(), validator=Length(3))

class Amounts(SequenceSchema):
    amount_node = SchemaNode(Int(), validator=Range(1))

class UnitTitles(SequenceSchema):
    unit_title_node = SchemaNode(String())

class StepNumbers(SequenceSchema):
    step_number_node = SchemaNode(Int(), validator=Range(1, 100))

class StepTexts(SequenceSchema):
    step_text_node = SchemaNode(String(), validator=Length(10))

class TimeValues(SequenceSchema):
    time_value_node = SchemaNode(Int())

class Recipe(MappingSchema):
    title = SchemaNode(String(), validator=Length(3))
    description = SchemaNode(String())
    product_title = ProductTitles()
    amount = Amounts()
    unit_title = UnitTitles()
    step_number = StepNumbers()
    step_text = StepTexts()
    time_value = TimeValues()
