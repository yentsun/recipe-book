# -*- coding: utf-8 -*-

from pyramid.security import Everyone, Allow, Deny, ALL_PERMISSIONS
from colander import Invalid, interpolate
from schemas import RecipeSchema
from kook.models import Entity, DBSession

class Dish(Entity):
    """
    Dish model
    """
    def __init__(self, title, description=None, tags=None):
        self.title = title
        self.description = description
        self.tags = tags or []

    def __repr__(self):
        return self.title

class Recipe(Entity):
    """
    Recipe model
    """
    def __init__(self, dish, id=None, description=None, author=None,
                 status_id=1):
        self.dish = dish
        self.id = id or self.generate_id()
        self.description = description
        self.author = author
        self.status_id = status_id
        self.steps = []
        self.ingredients = []
        self.tags = []

    def __repr__(self):
        return u'%s from %s' % (self.dish.title, self.author.email)

    @property
    def __acl__(self):
        """
        Return acl minding recipe's status
        """
        STATUS_MAP = {
            0: (Deny, Everyone, 'read'),
            1: (Allow, Everyone, 'read')
        }
        acl = [(Allow, self.author.id, ALL_PERMISSIONS)]
        acl.append(STATUS_MAP[self.status_id])
        return acl

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
    def construct_from_dict(cls, cstruct, localizer=None):
        recipe_schema = RecipeSchema()
        try:
            appstruct = recipe_schema.deserialize(cstruct)
        except Invalid, e:
            errors = {}
            for path in e.paths():
                keyparts = []
                msgs = []
                for exc in path:
                    exc.msg and msgs.extend(exc.messages())
                    keyname = exc._keyname()
                    keyname and keyparts.append(keyname)
                    if localizer:
                        msgs = [localizer.translate(s, domain='kook')
                                for s in msgs]
                errors['.'.join(keyparts)] = '; '.join(interpolate(msgs))
            return {'errors': errors,
                    'original_data': cstruct}
        recipe = cls(dish=Dish(appstruct['dish_title']),
                     description=appstruct['description'])
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
        for step_entry in appstruct['steps']:
            recipe.steps.append(Step(step_entry['number'],
                                     step_entry['text'],
                                     step_entry['time_value']))
        return recipe

    def to_dict(self):
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
    def ordered_steps(self):
        ordered_steps = dict()
        for step in self.steps:
            ordered_steps[step.number] = step
        return ordered_steps

    def update(self):
        DBSession.merge(self)

    @classmethod
    def fetch(cls, id):
        return DBSession.query(cls).get(id)

    @classmethod
    def fetch_all(cls, author_id=None, dish_title=None):
#        TODO index all relevant tables
        from kook.models.sqla_metadata import recipes
        query = DBSession.query(cls)
        if author_id:
            query = query.filter(recipes.c.user_id==author_id)
        if dish_title:
            query = query.filter(recipes.c.dish_title==dish_title)
        return query.all()

class Step(Entity):
    u"""Модель шага приготовления"""

    def __init__(self, number, text, time_value=None, note=None):
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

    def __str__(self):
        return self.title

class Ingredient(Entity):
    u"""Модель ингредиента (продукт+количество)"""

    def __init__(self, product, amount, unit=None):
        self.product = product
        self.amount = int(amount)
        self.unit = unit

    def __repr__(self) :
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



