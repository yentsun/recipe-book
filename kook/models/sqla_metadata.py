from sqlalchemy import (Column, Table, Unicode, Integer, String, Date,
                        DateTime, CHAR, FLOAT, ForeignKey, MetaData)

metadata = MetaData()

dishes = Table(
    'dishes', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('description', Unicode))

recipes = Table(
    'recipes', metadata,
    Column('ID', CHAR(36), primary_key=True),
    Column('dish_title', Unicode, ForeignKey('dishes.title')),
    Column('description', Unicode),
    Column('creation_time', DateTime()),
    Column('update_time', DateTime()),
    Column('status_id', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('user_id', CHAR(36), ForeignKey('users.id'), nullable=False))

products = Table(
    'products', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

units = Table(
    'units', metadata,
    Column('title', Unicode, primary_key=True, nullable=False),
    Column('abbr', Unicode))

amount_per_unit = Table(
    'amount_per_unit', metadata,
    Column('product_title', Unicode, ForeignKey('products.title'),
           primary_key=True, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title'),
           primary_key=True, nullable=False),
    Column('amount', FLOAT, nullable=False))

ingredients = Table(
    'ingredients', metadata,
    Column('recipe_id', CHAR(36), ForeignKey('recipes.ID'),
           primary_key=True),
    Column('product_title', Unicode, ForeignKey('products.title'),
           primary_key=True),
    Column('amount', FLOAT, nullable=False),
    Column('unit_title', Unicode, ForeignKey('units.title')))

steps = Table(
    'steps', metadata,
    Column('recipe_id', CHAR(36), ForeignKey('recipes.ID'),
           primary_key=True, nullable=False),
    Column('number', Integer, nullable=False, primary_key=True),
    Column('time_value', Integer),
    Column('text', Unicode, nullable=False),
    Column('note', Unicode))

tags = Table(
    'tags', metadata,
    Column('title', Unicode, primary_key=True, nullable=False))

dish_tags = Table(
    'dish_tags', metadata,
    Column('dish_title', Unicode, ForeignKey('dishes.title'),
           primary_key=True, nullable=False),
    Column('tag_title', Unicode,  ForeignKey('tags.title'),
           primary_key=True, nullable=False))

users = Table(
    'users', metadata,
    Column('id', CHAR(36), primary_key=True, nullable=False),
    Column('email', String(320), unique=True, nullable=False),
    Column('password_hash', CHAR(60), nullable=False))

groups = Table(
    'groups', metadata,
    Column('title', String(20), primary_key=True, nullable=False))

user_favourites = Table(
    'user_favourites', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('dish_title', Unicode, ForeignKey('dishes.title'), primary_key=True,
           nullable=False))

user_groups = Table(
    'user_groups', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('group_title', String(20), ForeignKey('groups.title'),
           primary_key=True, nullable=False))

profiles = Table(
    'profiles', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('rep', Integer),
    Column('birthday', Date()),
    Column('registration_day', Date()),
    Column('location', Unicode),
    Column('nickname', Unicode, unique=True),
    Column('real_name', Unicode))

rep_records = Table(
    'rep_records', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id')),
    Column('rep_value', Integer),
    Column('subject', String),
    Column('object_id', CHAR(36)),
    Column('creation_time', DateTime(), primary_key=True))

vote_records = Table(
    'vote_records', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', CHAR(36), ForeignKey('recipes.ID'), primary_key=True),
    Column('value', Integer),
    Column('creation_time', DateTime(), primary_key=True))

comments = Table(
    'comments', metadata,
    Column('user_id', CHAR(36), ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', CHAR(36), ForeignKey('recipes.ID'), primary_key=True),
    Column('text', Unicode, nullable=False),
    Column('creation_time', DateTime(), primary_key=True))

dish_images = Table(
    'dish_images', metadata,
    Column('dish_title', Unicode, ForeignKey('dishes.title'), primary_key=True,
           nullable=False),
    Column('url', Unicode, nullable=False),
    Column('credit', Unicode))