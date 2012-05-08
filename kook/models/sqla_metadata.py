from sqlalchemy.orm import relationship, mapper
from sqlalchemy import (Column, Table, Unicode, Integer, String, Date,
                        DateTime, CHAR, ForeignKey, MetaData)
from kook.models.recipe import (Recipe, Dish, Ingredient, Step, Product,
                                AmountPerUnit, Unit, Tag)
from kook.models.user import User, Group, Profile, RepRecord

metadata = MetaData()

dishes = Table('dishes', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('description', Unicode))

recipes = Table('recipes', metadata,
    Column('id', CHAR(36), primary_key=True),
    Column('dish_title', Unicode, ForeignKey('dishes.title')),
    Column('description', Unicode),
    Column('creation_time', DateTime()),
    Column('update_time', DateTime()),
    Column('status_id', Integer, nullable=False),
    Column('user_id', CHAR(36), ForeignKey('users.id'), nullable=False))

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
    Column('recipe_id', Integer, ForeignKey('recipes.id'),
        primary_key=True),
    Column('product_title', Unicode, ForeignKey('products.title'),
        primary_key=True),
    Column('amount', Integer, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title')))

steps = Table('steps', metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'),
        primary_key=True, nullable=False),
    Column('number', Integer, nullable=False, primary_key=True),
    Column('time_value', Integer),
    Column('text', Unicode, nullable=False),
    Column('note', Unicode))

tags = Table('tags', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

dish_tags = Table('dish_tags', metadata,
    Column('dish_title', Unicode, ForeignKey('dishes.title'),
        primary_key=True, nullable=False),
    Column('tag_title', Unicode,  ForeignKey('tags.title'),
        primary_key=True, nullable=False))

users = Table('users', metadata,
    Column('id', CHAR(36), primary_key=True, nullable=False),
    Column('email', String(320), unique=True, nullable=False),
    Column('password_hash', CHAR(60), nullable=False))

groups = Table('groups', metadata,
    Column('title', String(20), primary_key=True, nullable=False))

user_favourites = Table('user_favourites', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('dish_title', Unicode, ForeignKey('dishes.title'), primary_key=True,
           nullable=False))

user_groups = Table('user_groups', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('group_title', String(20), ForeignKey('groups.title'),
           primary_key=True, nullable=False))

profiles = Table('profiles', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('rep', Integer),
    Column('birthday', Date()),
    Column('registration_day', Date()),
    Column('location', String(100)),
    Column('nickname', String(100), unique=True),
    Column('real_name', String(200)))

rep_records = Table('rep_records', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id')),
    Column('rep_value', Integer),
    Column('creation_time', DateTime(), primary_key=True))

#========
# MAPPERS
#========

mapper(Recipe, recipes, properties={
    'dish': relationship(Dish, lazy='join'),
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
    'groups': relationship(Group, secondary=user_groups),
    'favourite_dishes': relationship(Dish, secondary=user_favourites),
    'profile': relationship(Profile, uselist=False,
        cascade='all, delete, delete-orphan')})
mapper(Dish, dishes, properties={
    'recipes': relationship(Recipe),
    'tags': relationship(Tag, secondary=dish_tags)
})
mapper(Step, steps)
mapper(Tag, tags)
mapper(Unit, units)
mapper(Group, groups)
mapper(Profile, profiles)
mapper(RepRecord, rep_records)