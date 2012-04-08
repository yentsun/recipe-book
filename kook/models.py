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

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
metadata = MetaData()

class Entity(object):

    def __eq__(self, other) :
        return self.__str__() == other.__str__()

    def save(self):
        DBSession.merge(self)

class Recipe(Entity):
    """Recipe model"""

    def __init__(self, title, description, products_amounts=None):
        self.title = title.lower()
        self.description = description
        self.steps = []
        if products_amounts is not None:
            self.ingredients = []
            for product_title, amount in products_amounts:
                product = Product(product_title)
                self.ingredients.append(Ingredient(product, amount))

    @classmethod
    def construct_from_multidict(cls, multidict):
        recipe = cls(multidict.getone('title'), multidict.getone('description'))
        product_titles = multidict.getall('product_title')
        amounts = multidict.getall('amount')
        unit_titles = multidict.getall('unit_title')
        recipe.ingredients = []
        for product_title, amount, unit_title in zip(product_titles, amounts, unit_titles):
            product = Product(product_title)
            unit = Unit.factory(unit_title)
            recipe.ingredients.append(Ingredient(product, amount, unit))
        steps_numbers = multidict.getall('step_number')
        time_values = multidict.getall('time_value')
        steps_texts = multidict.getall('step_text')
        recipe.steps = []
        for number,\
            text,\
            time_value,\
        in zip(steps_numbers,
               steps_texts,
               time_values):
            step = Step(number, text, time_value)
            recipe.steps.append(step)
        return recipe

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
    def factory(cls, title):
        if title != '':
            unit = cls.fetch(title)
            if unit:
                return unit
            else:
                new_unit = cls(title, title[:2])
                return new_unit
        else:
            return None

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
    def unit_abbr(self):
        if self.unit is not None:
            return self.unit.abbr
        else:
            return u'г'

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
    Column('amount', Integer, nullable=False)
)

ingredients = Table('ingredients', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'), primary_key=True),
    Column('product_title', Unicode, ForeignKey('products.title'), primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title')),
)

steps = Table('steps', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'), primary_key=True),
    Column('number', Integer, nullable=False, primary_key=True),
    Column('time_value', Integer, nullable=False),
    Column('text', Unicode),
    Column('note', Unicode)
)

mapper(Step, steps)
mapper(Unit, units)
mapper(Recipe, recipes, properties={'ingredients': relationship(
                                                        Ingredient,
                                                        backref='recipe',
                                                        lazy='subquery',
                                                        cascade='all, delete, delete-orphan',
                                                        order_by=ingredients.c.amount.desc()),
                                    'steps': relationship(
                                                        Step,
                                                        cascade='all, delete, delete-orphan',
                                                        lazy='subquery',
                                                        order_by=steps.c.number)})
mapper(Product, products, properties={'APUs':relationship(AmountPerUnit,
                                                        cascade='all, delete-orphan')})
mapper(AmountPerUnit, amount_per_unit, properties={'unit':relationship(Unit,
                                                        lazy='joined'),
                                                   'product':relationship(Product)})
mapper(Ingredient, ingredients, properties={'product':relationship(Product,
                                                        uselist=False,
                                                        lazy='joined'),
                                            'unit':relationship(Unit, uselist=False,                                                                     lazy='joined')})