# -*- coding: utf-8 -*-

from sqlalchemy import (Column,
                        Table,
                        Unicode,
                        Integer,
                        ForeignKey,
                        MetaData)
from sqlalchemy.orm import (scoped_session,
                            sessionmaker,
                            relationship,
                            mapper)
from zope.sqlalchemy import ZopeTransactionExtension
from colander import Invalid
from schemas import RecipeSchema

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()))
metadata = MetaData()

class Entity(object):

    def __eq__(self, other) :
        return self.__str__() == other.__str__()

    def save(self):
        DBSession.merge(self)

class Recipe(Entity):
    """Recipe model"""

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.steps = []
        self.ingredients = []

    @classmethod
    def multidict_to_dict(cls, multidict):
        dictionary = {'title': multidict.getone('title'),
                      'description': multidict.getone('description'),
                      'ingredients': [],
                      'steps': []}
        product_titles = multidict.getall('product_title')
        amounts = multidict.getall('amount')
        unit_titles = multidict.getall('unit_title')

        for product_title, amount, unit_title\
        in zip(product_titles, amounts, unit_titles):
            dictionary['ingredients'].append({
                'product_title': product_title,
                'amount': amount,
                'unit_title': unit_title
            })

        steps_numbers = multidict.getall('step_number')
        time_values = multidict.getall('time_value')
        steps_texts = multidict.getall('step_text')

        for number,\
            text,\
            time_value,\
        in zip(steps_numbers,
            steps_texts,
            time_values):
            dictionary['steps'].append({
            'number': number,
            'text': text,
            'time_value': time_value
            })

        return dictionary

    @classmethod
    def construct_from_dict(cls, cstruct):
        recipe_schema = RecipeSchema()
        try:
            appstruct = recipe_schema.deserialize(cstruct)
        except Invalid, e:
            return e.asdict()
        recipe = cls(appstruct['title'],
                     appstruct['description'])
        for ingredient_entry in appstruct['ingredients']:
            if ingredient_entry['unit_title'] is None:
                unit = None
            else:
                unit = Unit.fetch(ingredient_entry['unit_title'])
            recipe.ingredients.append(Ingredient(
                Product(ingredient_entry['product_title']),
                ingredient_entry['amount'],
                unit
            ))
        for step_entry in appstruct['steps']:
            recipe.steps.append(Step(step_entry['number'],
                                     step_entry['text'],
                                     step_entry['time_value']))
        return recipe

    @classmethod
    def construct_from_multidict(cls, multidict):
        dict = cls.multidict_to_dict(multidict)
        return cls.construct_from_dict(dict)

    def to_dict(self):
        result = {
            'title': self.title,
            'description': self.description,
            'ingredients': [],
            'steps': []
        }
        for ingredient in self.ingredients:
            ingredient_dict = {
                'product_title': ingredient.product.title,
                'amount': ingredient.amount
            }
            if ingredient.unit is not None:
                ingredient_dict['unit_title'] = ingredient.unit.title
            else:
                ingredient_dict['unit_title'] = ''
            result['ingredients'].append(ingredient_dict)
        for step in self.steps:
            result['steps'].append({
                'number': step.number,
                'text': step.text,
                'time_value': step.time_value
            })
        return result

    @property
    def products(self):
        products = []
        for ingredient in self.ingredients:
            products.append(ingredient.product)
        return products

    @property
    def total_amount(self):
        total = 0
        if self.ingredients is not None:
            for ingredient in self.ingredients:
                total += ingredient.amount
        return total

    @property
    def ordered_steps(self):
        ordered_steps = dict()
        for step in self.steps:
            ordered_steps[step.number] = step
        return ordered_steps

    def update(self, title):
        old = DBSession.query(Recipe).get(title)
        DBSession.delete(old)
        DBSession.merge(self)

    @classmethod
    def fetch(cls, title):
        return DBSession.query(Recipe).filter(Recipe.title==title).first()

    @classmethod
    def delete(cls, title):
        victim = cls.fetch(title)
        DBSession.delete(victim)
        return victim.title

    @classmethod
    def fetch_all(cls):
        return DBSession.query(cls).all()

class Step(Entity):
    u"""Модель шага приготовления"""

    def __init__(self, number, text, time_value=None, note=None):
        self.number = number
        self.text = text
        self.time_value = time_value
        self.note = note

    def __str__(self) :
        return u'Шаг %s: %s (%s мин)' % (self.number, self.text, self.time_value)

    @classmethod
    def dummy(cls):
        return cls(1, '', '')

class Product(Entity):
    """Product model"""

    def __init__(self, title):
        self.title = title

    def __str__(self) :
        return self.title

    @classmethod
    def fetch(cls, title):
        return DBSession.query(Product).filter(Product.title==title).first()

    @classmethod
    def fetch_all(cls):
        return DBSession.query(cls).all()

class Unit(Entity):
    """Measure unit"""

    def __init__(self, title, abbr=None):
        self.title = title
        self.abbr = abbr

    @classmethod
    def fetch(cls, title):
        return DBSession.query(cls).filter(cls.title==title).first()


class Ingredient(Entity):
    u"""Модель ингредиента (продукт+количество)"""

    def __init__(self, product, amount, unit=None):
        self.product = product
        self.amount = int(amount)
        self.unit = unit

    def __str__(self) :
        return u'%s %d г' % (self.product.title, self.amount)

    @classmethod
    def dummy(cls):
        """Create an empty object"""
        dummy_product = Product('')
        return cls(dummy_product, 0)

    @property
    def measured(self):
        if len(self.product.APUs) > 0 and self.unit:
            for apu in self.product.APUs:
                if apu.unit.title == self.unit.title:
                    return self.amount / apu.amount
        else:
            if self.amount:
                return self.amount
            else:
                return ''

    @property
    def apu(self):
        if self.unit is not None:
            for apu in self.product.APUs:
                if apu.unit.title == self.unit.title:
                    return apu.amount
        else:
            return 1

    def string_unit_title(self):
        """Return unit title or empty string"""
        if self.unit is None:
            return ''
        else:
            return self.unit.title

class AmountPerUnit(Entity):

    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def measure(self, amount):
        return amount / self.amount

#sqlalchemy stuff

#tables
recipes = Table('recipes', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('description', Unicode))

products = Table('products', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

units = Table('units', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('abbr', Unicode))

amount_per_unit = Table('amount_per_unit', metadata,
    Column('product_title', Unicode, ForeignKey('products.title'),
           primary_key=True, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title'),
           primary_key=True, nullable=False),
    Column('amount', Integer, nullable=False))

ingredients = Table('ingredients', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'),
           primary_key=True),
    Column('product_title', Unicode, ForeignKey('products.title'),
           primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title')))

steps = Table('steps', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'),
           primary_key=True),
    Column('number', Integer, nullable=False, primary_key=True),
    Column('time_value', Integer),
    Column('text', Unicode, nullable=False),
    Column('note', Unicode))

#mappers
mapper(Step, steps)
mapper(Unit, units)
mapper(Recipe, recipes, properties={
    'ingredients': relationship(Ingredient,
                                lazy='subquery',
                                cascade='all, delete, delete-orphan',
                                order_by=ingredients.c.amount.desc()),
    'steps': relationship(Step, cascade='all, delete, delete-orphan',
                          lazy='subquery', order_by=steps.c.number)})

mapper(Product, products, properties={
    'APUs':relationship(AmountPerUnit, cascade='all, delete-orphan',
                        lazy='joined')})

mapper(AmountPerUnit, amount_per_unit, properties={
    'unit':relationship(Unit, lazy='joined'),
    'product':relationship(Product)})

mapper(Ingredient, ingredients, properties={
    'product':relationship(Product, uselist=False, lazy='joined'),
    'unit':relationship(Unit, uselist=False, lazy='joined')})