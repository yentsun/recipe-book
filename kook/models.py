# -*- coding: utf-8 -*-

import transaction
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
    u"""Модель сущности"""

    def __eq__(self, other) :
        return self.__str__() == other.__str__()

    def save(self):
        DBSession.merge(self)

class Recipe(Entity):
    u"""Модель рецепта"""

    def __init__(self, title, description, products_amounts=None):
        self.title = title
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
        products = multidict.getall('product')
        amounts = multidict.getall('amount')
        recipe.ingredients = []
        for product_title, amount in zip(products, amounts):
            product = Product(product_title)
            recipe.ingredients.append(Ingredient(product, amount))
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

    def get_ingredient_by_product_title(self, product_title):
        for ingredient in self.ingredients:
            if ingredient.product.title == product_title:
                return ingredient

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

class Action(Entity):
    u"""Модель действия"""

    def __init__(self, title):
        self.title = title

class Product(Entity):
    u"""Модель продукта (молоко, картофель и тд)"""

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
    u"""Модель единицы меры продукта (штука, ст. ложка и тд)"""

    def __init__(self, title, amount, product):
        self.title = title
        self.amount = amount
        self.product_title = product.title

class Ingredient(Entity):
    u"""Модель ингредиента (продукт+количество)"""

    def __init__(self, product, amount, unit=None):
        self.product = product
        self.amount = amount
        self.unit = unit

    def __str__(self) :
        return u'%s %d г' % (self.product.title, self.amount)

    @classmethod
    def dummy(cls):
        """Create an empty object"""
        dummy_product = Product('')
        return cls(dummy_product, '')

    def measure(self, unit_title=None):
        if len(self.product.units) > 0:
            for unit in self.product.units:
                if unit_title is None or \
                   unit_title == unit.title or \
                   unit.title == self.unit.title:
                    return u'%d %s' % ((self.amount / unit.amount), unit.title)
        else:
            return u'%d г' % self.amount

#DB Tables & mappings

recipes = Table('recipes', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('description', Unicode))

products = Table('products', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

units = Table('units', metadata,
    Column('product_title', Unicode, ForeignKey('products.title'),
            primary_key=True, nullable=False),
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('amount', Integer, nullable=False)
)

ingredients = Table('ingredients', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'), primary_key=True),
    Column('product_title', Unicode, ForeignKey('products.title'), primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title')),
)

actions = Table('actions', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

steps = Table('steps', metadata,
    Column('recipe_title', Unicode, ForeignKey('recipes.title'), primary_key=True),
    Column('number', Integer, nullable=False, primary_key=True),
    Column('time_value', Integer, nullable=False),
    Column('text', Unicode),
    Column('note', Unicode)
)

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
mapper(Product, products, properties={'units':relationship(
                                                        Unit,
                                                        backref='product',
                                                        cascade='all, delete-orphan')})
mapper(Unit, units)
mapper(Action, actions)
mapper(Ingredient, ingredients, properties={'product':relationship(
                                                        Product,
                                                        uselist=False,
                                                        lazy='joined'),
                                            'unit':relationship(Unit, uselist=False,
                                                                lazy='joined')})
mapper(Step, steps)