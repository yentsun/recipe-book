# -*- coding: utf-8 -*-

from sqlalchemy import (Column, Table, Unicode, Integer, String,
                        CHAR, ForeignKey, MetaData)
from sqlalchemy.orm import (scoped_session,
                            sessionmaker,
                            relationship,
                            mapper)
from zope.sqlalchemy import ZopeTransactionExtension
from colander import Invalid
from hashlib import md5
from urllib import urlencode
from uuid import uuid4
from schemas import RecipeSchema, UserSchema

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()))
metadata = MetaData()

class Entity(object):

    def __eq__(self, other) :
        return self.__str__() == other.__str__()

    def save(self):
        DBSession.merge(self)

    @classmethod
    def multidict_to_dict(cls, multidict):
        pass

    @classmethod
    def construct_from_dict(cls, cstruct):
        pass

    @classmethod
    def construct_from_multidict(cls, multidict):
        dict = cls.multidict_to_dict(multidict)
        return cls.construct_from_dict(dict)

class Recipe(Entity):
    """Recipe model"""

    def __init__(self, title, description, author=None):
        self.title = title
        self.description = description
        self.author = author
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
            return {'errors': e.asdict(),
                    'original_data': cstruct}
        recipe = cls(appstruct['title'], appstruct['description'])
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

    def update(self, title, author_id):
        self.delete(title, author_id)
        DBSession.merge(self)

    @classmethod
    def fetch(cls, title, author_id):
        return DBSession.query(Recipe)\
                        .filter(Recipe.title==title,
                                User.id==author_id)\
                        .first()

    @classmethod
    def delete(cls, title, author_id):
        victim = cls.fetch(title, author_id)
        DBSession.delete(victim)
        return victim.title

    @classmethod
    def fetch_all(cls, author_id=None):
        query = DBSession.query(cls)
        if author_id:
            query = query.filter(recipes.c.user_id==author_id)
        return query.all()

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

class Group(Entity):

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return 'group:%s' % self.title

class User(Entity):

    salt = u'nRZ防也qI建7Ậ'

    def __init__(self, id, email, password_hash, groups=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.groups = groups or []

    def check_password(self, password):
        return self.password_hash == self.generate_hash(password)

    def generate_password(self):
        """Generate new password and send it to user email"""
        #TODO complete function
        return '000000'

    @property
    def gravatar_url(self):
        default = 'identicon'
        size = 20
        url = 'http://www.gravatar.com/avatar/%s?%s' %\
              (md5(self.email).hexdigest(),
               urlencode({'d':default, 's':str(size)}))
        return url

    @classmethod
    def generate_id(cls):
        return uuid4().hex

    @classmethod
    def generate_hash(cls, password):
        pass_string = (password + cls.salt).encode('utf-8')
        return md5(pass_string).hexdigest()

    @classmethod
    def fetch(cls, id=None, email=None):
        query = DBSession.query(cls)
        if id:
            return query.get(id)
        elif email:
            return query.filter(cls.email==email).first()
        return None

    @classmethod
    def multidict_to_dict(cls, multidict):
        return {'email': multidict.getone('email'),
                'password': multidict.getone('password')}

    @classmethod
    def construct_from_dict(cls, cstruct):
        """The way to construct new user"""
        user_schema = UserSchema()
        try:
            appstruct = user_schema.deserialize(cstruct)
        except Invalid, e:
            return {'errors': e.asdict(),
                    'original_data': cstruct}
        id = cls.generate_id()
        hash = cls.generate_hash(appstruct['password'])
        groups = [Group('applied')]
        user = cls(id, appstruct['email'], hash, groups)
        return user

class UserGroup(object):

    @classmethod
    def fetch_all(cls, email, request):
        return DBSession.query(cls)\
                        .filter(User.email==email)\
                        .all()

#sqlalchemy stuff

#tables
recipes = Table('recipes', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('description', Unicode),
    Column('user_id', CHAR(32), ForeignKey('users.id'), primary_key=True,
           nullable=False))

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

users = Table('users', metadata,
    Column('id', CHAR(32), primary_key=True, nullable=False),
    Column('email', String(320), unique=True, nullable=False),
    Column('password_hash', CHAR(32), nullable=False))

groups = Table('groups', metadata,
    Column('title', String(20), primary_key=True, nullable=False))

user_groups = Table('user_groups', metadata,
    Column('user_id', CHAR(32), ForeignKey('users.id'),
           primary_key=True),
    Column('group_title', String(20), ForeignKey('groups.title')))

#mappers
mapper(Recipe, recipes, properties={
    'ingredients': relationship(Ingredient,
                                lazy='subquery',
                                cascade='all, delete, delete-orphan',
                                order_by=ingredients.c.amount.desc()),
    'steps': relationship(Step, cascade='all, delete, delete-orphan',
                          lazy='subquery', order_by=steps.c.number),
    'author': relationship(User, lazy='joined', uselist=False)})

mapper(Product, products, properties={
    'APUs': relationship(AmountPerUnit, cascade='all, delete-orphan',
                        lazy='joined')})

mapper(AmountPerUnit, amount_per_unit, properties={
    'unit': relationship(Unit, lazy='joined'),
    'product': relationship(Product)})

mapper(Ingredient, ingredients, properties={
    'product': relationship(Product, uselist=False, lazy='joined'),
    'unit': relationship(Unit, uselist=False, lazy='joined')})
mapper(User, users, properties={
    'groups': relationship(Group, secondary=user_groups)})
mapper(Step, steps)
mapper(Unit, units)
mapper(Group, groups)
mapper(UserGroup, user_groups)