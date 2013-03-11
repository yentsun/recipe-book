# -*- coding: utf-8 -*-

from __future__ import division
import locale
import math
import codecs
from datetime import datetime, timedelta
from urlparse import urlparse
from pyramid.security import Allow, Deny
from colander import Invalid, interpolate
from sqlalchemy import desc
from sqlalchemy.orm import relationship, mapper, subqueryload

from kook.models.sqla_metadata import (ingredients, dishes, amount_per_unit,
                                       products, steps, recipes, dish_tags,
                                       vote_records, comments, tags, units,
                                       dish_images)
from kook.security import (RECIPE_BASE_ACL, AUTHOR_ACTIONS, VOTE_ACTIONS,
                           COMMENT_BASE_ACL)
from kook.mako_filters import pretty_time, markdown
from kook.models.schemas import RecipeSchema, CommentSchema
from kook.models import (Entity, DBSession, UPVOTE, DOWNVOTE,
                         DOWNVOTE_COST, UPVOTE_REP_CHANGE,
                         DOWNVOTE_REP_CHANGE, FRACTIONS, generate_id)

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def to_localized_decimal(input_):
    output_ = input_
    try:
        output_ = locale.atof(input_)
    except ValueError:
        pass
    return output_


class Dish(Entity):
    """Dish model"""
    def __init__(self, title='Dummy dish', description=None, tags=None, image=None):
        self.title = title
        self.tags = tags or []
        self.description = description
        self.image = image

    def __repr__(self):
        return self.title

    def fetch_image(self):
        """Fetch image from Google"""
        import urllib
        import urllib2
        import json

        query = {'q': self.title.encode('utf-8'), 'v': '1.0', 'imgsz': 'large',
                 'rsz': 1}
        url = ('https://ajax.googleapis.com/ajax/services/search/images?%s'
               % urllib.urlencode(query))
        request = urllib2.Request(url, None, {'Referer': 'kook.loc'})
        response = urllib2.urlopen(request)
        print '------------making request...-----------------'
        result = json.load(response)['responseData']['results'][0]
        self.image = DishImage(result['url'], result['visibleUrl'])

    @classmethod
    def fetch_all(cls, limit=None, tag_title=None, order_by='recipe_count'):
        query = DBSession.query(cls).limit(limit)
        if tag_title:
            query = query.filter(cls.tags.any(tags.c.title == tag_title))
        if order_by is not 'recipe_count':
            if order_by is 'title':
                dishes = query.order_by(cls.title).all()
            else:
                dishes = query.order_by(desc(getattr(cls, order_by))).all()
        else:
            dishes = sorted(query.all(), key=lambda dish: len(dish.recipes),
                            reverse=True)
        return dishes


class Recipe(Entity):
    """Recipe model"""
    def __init__(self, dish, author, id_=None, description=None,
                 status_id=1, creation_time=None, rating=0, update_time=None):
        self.dish = dish
        self.ID = id_ or generate_id()
        self.description = description
        self.author = author
        self.status_id = status_id
        self.rating = rating
        self.steps = []
        self.ingredients = []
        self.comments = []
        self.creation_time = creation_time or datetime.now()
        self.update_time = update_time

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
    def dummy(cls, author, dict_=None):
        if dict_:
            dummy = Recipe(Dish(dict_['dish_title']), author)
            dummy.ingredients = list(
                Ingredient(Product(ingredient.get('product_title')),
                           ingredient.get('amount', 0))
                for ingredient in dict_['ingredients'])
            dummy.steps = list(Step(step['no'], step['text'])
                               for step in dict_['steps'])
        else:
            dummy = Recipe(Dish(), author)
            dummy.ingredients = [Ingredient.dummy()]
            dummy.steps = [Step.dummy()]

        return dummy

    @classmethod
    def multidict_to_dict(cls, multidict):
        dictionary = {'dish_title': multidict.getone('dish_title'),
                      'description': multidict.getone('description'),
                      'ingredients': [],
                      'steps': []}
        product_titles = multidict.getall('product_title')
        amounts = multidict.getall('amount')
        unit_titles = multidict.getall('unit_title')
        for product_title, amount, unit_title in zip(product_titles,
                                                     amounts, unit_titles):
            dictionary['ingredients'].append({
                'product_title': product_title,
                'amount': to_localized_decimal(amount),
                'unit_title': unit_title
            })
        steps_numbers = multidict.getall('step_number')
        time_values = multidict.getall('time_value')
        steps_texts = multidict.getall('step_text')
        for number, text, time_value, in zip(steps_numbers,
                                             steps_texts, time_values):
            dictionary['steps'].append({'number': number,
                                        'text': text,
                                        'time_value': time_value})

        return dictionary

    @classmethod
    def construct_from_dict(cls, cstruct, recipe, localizer=None,
                            fetch_dish_image=False):
        recipe_schema = RecipeSchema()
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
        dish = Dish.fetch(appstruct['dish_title']) or \
            Dish(appstruct['dish_title'])
        if not dish.image and fetch_dish_image:
            dish.fetch_image()

        #create the recipe
        recipe = cls(dish=dish, id_=recipe.ID, author=recipe.author,
                     description=appstruct['description'],
                     creation_time=recipe.creation_time,
                     update_time=recipe.update_time)

        #populate ingredient list
        for ingredient_entry in appstruct['ingredients']:
            if ingredient_entry['unit_title'] is None:
                unit = None
            else:
                unit = Unit.fetch(ingredient_entry['unit_title']) or \
                    Unit(ingredient_entry['unit_title'])
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
    def construct_from_multidict(cls, multidict, recipe=None, **kwargs):
        dict_ = cls.multidict_to_dict(multidict)
        return cls.construct_from_dict(dict_, recipe,
                                       kwargs.get('localizer'),
                                       kwargs.get('fetch_dish_image'))

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
            total += step.time_value or 0
        return (datetime.min + timedelta(minutes=total)).time()

    @property
    def ordered_steps(self):
        ordered_steps = dict()
        for step in self.steps:
            ordered_steps[step.number] = step
        return ordered_steps

    @classmethod
    def fetch(cls, id_):
        """Fetch a recipe by id with all children. A costly call"""
        return DBSession.query(cls).options(subqueryload('*')).get(id_)

    @classmethod
    def fetch_all(cls, author_id=None, dish_title=None, limit=None,
                  order_by='rating'):
#        TODO index all relevant tables
        from kook.models.sqla_metadata import recipes
        query = DBSession.query(cls).order_by(desc(getattr(cls, order_by)))
        if author_id:
            query = query.filter(recipes.c.user_id == author_id)
        if dish_title:
            query = query.filter(recipes.c.dish_title == dish_title)
        if limit:
            query = query.limit(limit)
        return query.all()


class Step(Entity):
    u"""Модель шага приготовления"""

    def __init__(self, number, text, time_value=None, note=None):
        self.number = number
        self.text = text
        self.time_value = time_value
        self.note = note

    def __repr__(self):
        return u'Шаг %s: %s (%s мин)' \
               % (self.number, self.text, self.time_value)

    @classmethod
    def dummy(cls):
        return cls(1, '', '')


class Product(Entity):
    """Product model"""

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title

    def update_from_multidict(self, multidict, localizer=None):
        dict_ = self.multidict_to_dict(multidict)
        return self.update_from_dict(dict_, localizer)

    @classmethod
    def multidict_to_dict(cls, multidict):
        dictionary = {'title': multidict.getone('title'),
                      'APUs': []}
        amounts = multidict.getall('amount')
        unit_titles = multidict.getall('unit_title')
        for unit_title, amount in zip(unit_titles, amounts):
            dictionary['APUs'].append({
                'amount': amount,
                'unit_title': unit_title
            })
        return dictionary

    def update_from_dict(self, cstruct, localizer):
        from kook.models.schemas import ProductSchema
        product_schema = ProductSchema()
        try:
            appstruct = product_schema.deserialize(cstruct)
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

        self.title = appstruct['title']

        #populate APU list
        for APU_entry in appstruct['APUs']:
            unit = Unit.fetch(APU_entry['unit_title']) or \
                Unit(APU_entry['unit_title'])
            amount = APU_entry['amount']
            apu = AmountPerUnit.fetch((self.title, unit.title)) or\
                AmountPerUnit(amount, unit)
            apu.amount = amount
            self.APUs.append(apu)

    @classmethod
    def fetch(cls, title):
        return DBSession.query(Product).filter(Product.title == title).first()

    @classmethod
    def dummy(cls):
        dummy = cls(u'')
        dummy.APUs = [AmountPerUnit('', Unit(u''))]
        return dummy


class Unit(Entity):
    """Measure unit"""

    def __init__(self, title, abbr=None):
        self.title = title
        self.abbr = abbr

    @classmethod
    def fetch(cls, title):
        return DBSession.query(cls).filter(cls.title == title).first()
    
    @classmethod
    def dummy(cls):
        return Unit(u'', '')


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
        self.amount = amount
        self.unit = unit

    def __repr__(self):
        return u'%s %d г' % (self.product.title, self.amount)

    @classmethod
    def dummy(cls):
        return cls(Product.dummy(), None)

    def get_measured(self, pretty_fractions=True):
        """Return str formatted measured amount or float amount"""
        result = self.amount
        if len(self.product.APUs) > 0 and self.unit:
            for apu in self.product.APUs:
                if apu.unit.title == self.unit.title:
                    result = self.amount / apu.amount
                    break
        if pretty_fractions:
            fraction_part, int_part = math.modf(result)
            fraction_part = round(fraction_part, 2)
            if fraction_part in FRACTIONS:
                return '%s%s' % (int(int_part) or '',
                                 FRACTIONS[fraction_part])
        try:
            result = locale.format('%g', result)
        except TypeError:
                pass
        return result

    @property
    def apu(self):
        result = 1
        if self.unit:
            for apu in self.product.APUs:
                if apu.unit.title == self.unit.title:
                    result = apu.amount
        return result

    def string_unit_title(self):
        """Return unit title or empty string"""
        #TODO maybe get rid of
        if self.unit is None:
            return ''
        else:
            return self.unit.title

    @classmethod
    def fetch_all(cls, product_title):
        return DBSession.query(Ingredient)\
                        .filter(ingredients.c.product_title == product_title)

    def get_unit(self):
        """Return ingredient's chosen unit or default unit if none"""
        unit = Unit(u'грамм', u'г')
        if self.unit:
            unit = self.unit
        return unit


class AmountPerUnit(Entity):

    def __init__(self, amount, unit):
        self.amount = amount
        self.unit = unit

    def __repr__(self):
        return '%s %s' % (self.unit.title, '{:g}'.format(self.amount))

    def measure(self, amount):
        if amount and self.amount:
            return amount / self.amount
        else:
            return 0

    @classmethod
    def dummy(cls):
        return cls('', Unit(''))


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
            return query\
                .filter(cls.user.id == user_id)\
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
        acl.extend(COMMENT_BASE_ACL)
        self.__acl__ = acl

    @property
    def markdown_text(self):
        return markdown(self.text)

    @property
    def pretty_time(self):
        return pretty_time(self.creation_time)

    @classmethod
    def delete_by_id(cls, author_id, recipe_id, creation_time):
        DBSession.query(cls)\
            .filter(cls.user_id == author_id,
                    cls.recipe_id == recipe_id,
                    cls.creation_time == creation_time)\
            .delete()

    @classmethod
    def construct_from_dict(cls, cstruct, author):
        schema = CommentSchema()
        try:
            appstruct = schema.deserialize(cstruct)
        except Invalid, e:
            return {'errors': e.asdict()}
        return cls(author, appstruct['text'])


class DishImage(Entity):
    """Image for a dish"""
    def __init__(self, url, credit=None):
        self.url = url
        self.credit = credit

    def get_credit(self):
        """
        Get domain name from url string.
        Taken from http://stackoverflow.com/a/1069780/216042
        """
        import pkg_resources
        file_name = pkg_resources.resource_filename(
            'kook',
            'static/txt/effective_tld_names.dat.txt')
        with codecs.open(file_name, 'r', 'utf-8') as tldFile:
            tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]

        urlElements = urlparse(self.url)[1].split('.')

        for i in range(-len(urlElements), 0):
            lastIElements = urlElements[i:]
            # abcde.co.uk, co.uk, uk
            candidate = ".".join(lastIElements)
            # *.co.uk, *.uk, *
            wildcardCandidate = ".".join(["*"] + lastIElements[1:])
            exceptionCandidate = "!" + candidate

            # match tlds:
            if exceptionCandidate in tlds:
                return ".".join(urlElements[i:])
            if candidate in tlds or wildcardCandidate in tlds:
                return ".".join(urlElements[i - 1:])

        raise ValueError("Domain not in global list of TLDs")

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
                          order_by=steps.c.number),
    'comments': relationship(Comment, cascade='all, delete, delete-orphan',
                             order_by=comments.c.creation_time),
    'author': relationship(User, uselist=False)})

mapper(Product, products, properties={
    'ingredients': relationship(Ingredient, cascade='all',
                                passive_updates=False),
    'APUs': relationship(AmountPerUnit, cascade='all, delete, delete-orphan',
                         passive_updates=False)})

mapper(AmountPerUnit, amount_per_unit, properties={
    'unit': relationship(Unit),
    'product': relationship(Product)})

mapper(Unit, units, properties={
    'APUs': relationship(AmountPerUnit, cascade='all',
                         passive_updates=False)
})

mapper(Ingredient, ingredients, properties={
    'product': relationship(Product, uselist=False),
    'unit': relationship(Unit, uselist=False)})

mapper(Dish, dishes, properties={
    'recipes': relationship(Recipe, passive_updates=False),
    'image': relationship(DishImage, uselist=False, passive_updates=False,
                          lazy='joined'),
    'tags': relationship(Tag, secondary=dish_tags, passive_updates=False,
                         lazy='joined')})

mapper(VoteRecord, vote_records, properties={
    'user': relationship(User, uselist=False),
    'recipe': relationship(Recipe, uselist=False)})

mapper(Comment, comments, properties={
    'recipe': relationship(Recipe, uselist=False),
    'author': relationship(User, uselist=False)})

mapper(Step, steps)
mapper(Tag, tags)
mapper(DishImage, dish_images)