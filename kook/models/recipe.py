# -*- coding: utf-8 -*-

from datetime import datetime, time
from pyramid.security import Everyone, Allow, Deny
from colander import Invalid, interpolate
from sqlalchemy import desc
from sqlalchemy.orm import relationship, mapper

from kook.models.schemas import CommentSchema
from kook.models.sqla_metadata import (ingredients, dishes, amount_per_unit,
                                       products, steps, recipes, dish_tags,
                                       vote_records, comments, tags, units, dish_images)
from kook.security import RECIPE_BASE_ACL, AUTHOR_ACTIONS, VOTE_ACTIONS, COMMENT_BASE_ACL
from kook.mako_filters import pretty_time, markdown
from schemas import RecipeSchema
from kook.models import (Entity, DBSession, UPVOTE, DOWNVOTE,
                         DOWNVOTE_COST, UPVOTE_REP_CHANGE, DOWNVOTE_REP_CHANGE)

class Dish(Entity):
    """
    Dish model
    """
    def __init__(self, title, description=None, tags=None, image=None):
        self.title = title
        self.tags = tags or []
        self.description = description
        self.image = image

    def __repr__(self):
        return self.title

    def fetch_image(self):
        """
        Fetch image from Google
        """
        import urllib
        import urllib2
        import json

        query = {'q': self.title.encode('utf-8'),
                 'v': '1.0',
                 'imgsz': 'large',
                 'rsz': 1}
        url = 'https://ajax.googleapis.com/ajax/services/search/images?%s'\
        % urllib.urlencode(query)
        request = urllib2.Request(url, None, {'Referer': 'kook.loc'})
        response = urllib2.urlopen(request)
        print '------------making request...-----------------'
        result = json.load(response)['responseData']['results'][0]
        self.image = DishImage(result['url'], result['visibleUrl'])

    @classmethod
    def fetch_all(cls, limit=10):
        dishes = DBSession.query(cls).limit(limit).all()
        return sorted(dishes, key=lambda dish: len(dish.recipes),
                      reverse=True)

class Recipe(Entity):
    """
    Recipe model
    """
    def __init__(self, dish, author, id=None, description=None,
                 status_id=1, creation_time=None, rating=0):
        self.dish = dish
        self.id = id or self.generate_id()
        self.description = description
        self.author = author
        self.status_id = status_id
        self.rating = rating
        self.steps = []
        self.ingredients = []
        self.comments = []
        self.creation_time = creation_time or datetime.now()
        self.update_time = None

    def __repr__(self):
        return u'%s from %s' % (self.dish.title, self.author.email)

    def attach_acl(self, prepend=None):
        acl = prepend or []
        acl.extend([
            (Deny, self.author.id, VOTE_ACTIONS),
            (Allow, self.author.id, AUTHOR_ACTIONS),
        ])
        acl.extend(RECIPE_BASE_ACL)
        self.__acl__ = acl

    def add_vote(self, user, vote_value):
        new_rating = self.rating + vote_value
        self.rating = new_rating
        if vote_value is UPVOTE:
            self.author.add_rep(UPVOTE_REP_CHANGE, 'upvote', self)
        if vote_value is DOWNVOTE:
            self.author.add_rep(DOWNVOTE_REP_CHANGE, 'downvote', self)
            user.add_rep(DOWNVOTE_COST, 'downvote', self)
        record = VoteRecord(user, self, vote_value)
        record.save()

    @classmethod
    def multidict_to_dict(cls, multidict):
        dictionary = {'dish_title': multidict.getone('dish_title'),
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
    def construct_from_dict(cls, cstruct, localizer=None,
                            fetch_dish_image=False, author=None):
        recipe_schema = RecipeSchema()
        if 'author_email' not in cstruct and author:
            cstruct['author_email'] = author.email
        try:
            appstruct = recipe_schema.deserialize(cstruct)
        except Invalid, e:
            errors = {}
            for path in e.paths():
                keyparts = []
                msgs = []
                for exc in path:
                    if exc.msg:
                        msgs.extend(exc.messages())
                    keyname = exc._keyname()
                    if keyname:
                        keyparts.append(keyname)
                    if localizer:
                        msgs = [localizer.translate(s, domain='kook')
                                for s in msgs]
                errors['.'.join(keyparts)] = '; '.join(interpolate(msgs))
            return {'errors': errors,
                    'original_data': cstruct}

        #create the dish first
        dish = Dish.fetch(appstruct['dish_title']) or\
               Dish(appstruct['dish_title'])
        if not dish.image and fetch_dish_image:
            dish.fetch_image()

        #get the author
        author = User.fetch(email=appstruct['author_email'])

        #create the recipe
        recipe = cls(dish=dish, author=author,
                     description=appstruct['description'],
                     creation_time=appstruct['creation_time'])

        #populate ingredient list
        for ingredient_entry in appstruct['ingredients']:
            if ingredient_entry['unit_title'] is None:
                unit = None
            else:
                unit = Unit.fetch(ingredient_entry['unit_title']) \
                       or Unit(ingredient_entry['unit_title'])
            recipe.ingredients.append(Ingredient(
                Product(ingredient_entry['product_title']),
                ingredient_entry['amount'],
                unit
            ))

        #populate step list
        for step_entry in appstruct['steps']:
            recipe.steps.append(Step(step_entry['number'],
                                     step_entry['text'],
                                     step_entry['time_value']))
        return recipe

    @classmethod
    def construct_from_multidict(cls, multidict, **kwargs):
        dict = cls.multidict_to_dict(multidict)
        return cls.construct_from_dict(dict,
                                       kwargs.get('localizer'),
                                       kwargs.get('fetch_dish_image'),
                                       kwargs.get('author'))

    def to_dict(self):
        #TODO try to automate from model attribs
        result = {
            'dish_title': self.dish.title,
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
    def total_time(self):
        total = 0
        for step in self.steps:
            total += step.time_value
        return time(minute=total)

    @property
    def ordered_steps(self):
        ordered_steps = dict()
        for step in self.steps:
            ordered_steps[step.number] = step
        return ordered_steps

    @classmethod
    def fetch(cls, id):
        return DBSession.query(cls).get(id)

    @classmethod
    def fetch_all(cls, author_id=None, dish_title=None, limit=None,
                  order_by='rating'):
#        TODO index all relevant tables
        from kook.models.sqla_metadata import recipes
        query = DBSession.query(cls).order_by(desc(getattr(cls, order_by)))
        if author_id:
            query = query.filter(recipes.c.user_id==author_id)
        if dish_title:
            query = query.filter(recipes.c.dish_title==dish_title)
        if limit:
            query = query.limit(limit)
        return query.all()

class Step(Entity):
    u"""Модель шага приготовления"""

    def __init__(self, number, text, time_value=0, note=None):
        self.number = number
        self.text = text
        self.time_value = time_value
        self.note = note

    def __repr__(self) :
        return u'Шаг %s: %s (%s мин)' % (self.number, self.text, self.time_value)

    @classmethod
    def dummy(cls):
        return cls(1, '', '')

class Product(Entity):
    """Product model"""

    def __init__(self, title):
        self.title = title

    def __repr__(self) :
        return self.title

    @classmethod
    def fetch(cls, title):
        return DBSession.query(Product).filter(Product.title==title).first()

class Unit(Entity):
    """Measure unit"""

    def __init__(self, title, abbr=None):
        self.title = title
        self.abbr = abbr

    @classmethod
    def fetch(cls, title):
        return DBSession.query(cls).filter(cls.title==title).first()

class Tag(Entity):
    """
    Tag model
    """
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title

class Ingredient(Entity):
    u"""Модель ингредиента (продукт+количество)"""

    def __init__(self, product, amount, unit=None):
        self.product = product
        self.amount = int(amount)
        self.unit = unit

    def __repr__(self) :
        return u'%s %d г' % (self.product.title, self.amount)

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
        #TODO maybe get rid of
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

class VoteRecord(Entity):
    """
    A vote record for a recipe
    """
    def __init__(self, user, recipe, value):
        self.user = user
        self.recipe = recipe
        self.value = value
        self.creation_time = datetime.now()

    @classmethod
    def fetch(cls, user_id, latest=True):
        query = DBSession.query(cls)
        if latest:
            return query.filter(cls.user.id==user_id)\
            .order_by(desc(cls.creation_time))\
            .first()
        return None

class Comment(Entity):
    """
    Comment entity
    """
    def __init__(self, author, text):
        self.author = author
        self.text = text
        self.creation_time = datetime.now()
        self.update_time = None

    def attach_acl(self):
        acl = list([(Allow, self.author.id, AUTHOR_ACTIONS)])
        acl.append(COMMENT_BASE_ACL)
        self.__acl__ = acl


    @property
    def markdown_text(self):
        return markdown(self.text)

    @property
    def pretty_time(self):
        return pretty_time(self.creation_time)

    @classmethod
    def delete(cls, author_id, recipe_id, creation_time):
        DBSession.query(cls).filter(
            cls.user_id==author_id,
            cls.recipe_id==recipe_id,
            cls.creation_time==creation_time).delete()

    @classmethod
    def construct_from_dict(cls, cstruct, author):
        schema = CommentSchema()
        try:
            appstruct = schema.deserialize(cstruct)
        except Invalid, e:
            return {'errors': e.asdict()}
        return cls(author, appstruct['text'])

class DishImage(Entity):
    """
    Image for a dish
    """
    def __init__(self, url, credit=None):
        self.url = url
        self.credit = credit

#========
# MAPPERS
#========
from kook.models.user import User

mapper(Recipe, recipes, properties={
    'dish': relationship(Dish, uselist=False),
    'ingredients': relationship(Ingredient,
        cascade='all, delete, delete-orphan',
        order_by=ingredients.c.amount.desc()),
    'steps': relationship(Step, cascade='all, delete, delete-orphan',
        lazy='subquery', order_by=steps.c.number),
    'comments': relationship(Comment, cascade='all, delete, delete-orphan',
        order_by=comments.c.creation_time),
    'author': relationship(User, uselist=False)})

mapper(Product, products, properties={
    'APUs': relationship(AmountPerUnit, cascade='all, delete-orphan')})

mapper(AmountPerUnit, amount_per_unit, properties={
    'unit': relationship(Unit),
    'product': relationship(Product)})

mapper(Ingredient, ingredients, properties={
    'product': relationship(Product, uselist=False),
    'unit': relationship(Unit, uselist=False)})

mapper(Dish, dishes, properties={
    'recipes': relationship(Recipe),
    'image': relationship(DishImage, uselist=False),
    'tags': relationship(Tag, secondary=dish_tags)})

mapper(VoteRecord, vote_records, properties={
    'user': relationship(User, uselist=False),
    'recipe': relationship(Recipe, uselist=False)})

mapper(Comment, comments, properties={
    'recipe': relationship(Recipe, uselist=False),
    'author': relationship(User, uselist=False)})

mapper(Step, steps)
mapper(Tag, tags)
mapper(Unit, units)
mapper(DishImage, dish_images)