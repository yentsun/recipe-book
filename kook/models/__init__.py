# -*- coding: utf-8 -*-

from uuid import uuid4
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Everyone, Allow, ALL_PERMISSIONS, Deny
from kook.security import VOTE_ACTIONS

DBSession = scoped_session(sessionmaker(
    extension=ZopeTransactionExtension()))

UPVOTE = 1
DOWNVOTE = -1
UPVOTE_REP_CHANGE = 10
DOWNVOTE_REP_CHANGE = -2
DOWNVOTE_COST = -1
UPVOTE_REQUIRED_REP = 15
DOWNVOTE_REQUIRED_REP = 125

def form_msg(acl):
    try:
        if acl.ace == (Deny, Everyone, VOTE_ACTIONS):
            return u'Для голосования нужно зарегистрироваться и войти на сайт'
        if acl.ace == (Deny, acl.context.author.id, VOTE_ACTIONS):
            return u'Нельзя голосовать за свои рецепты'
        if acl.ace == (Deny, 'registered', 'upvote'):
            return u'У вас недостаточно репутации, необходимо %s'\
                   % UPVOTE_REQUIRED_REP
        if acl.ace == (Deny, 'registered', 'downvote'):
            return u'У вас недостаточно репутации, необходимо %s'\
                   % DOWNVOTE_REQUIRED_REP
        else:
            return u'действие: %s; кому %s; привилегия: %s' % acl.ace
    except AttributeError:
        pass

class Entity(object):
    """
    Basic (abstract) class for all entities
    """
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def save(self):
        DBSession.merge(self)

    def delete(self):
        DBSession.delete(self)

    @classmethod
    def fetch(cls, primary, **kwargs):
        return DBSession.query(cls).get(primary)

    @classmethod
    def fetch_all(cls, **kwargs):
        return DBSession.query(cls).all()

    @classmethod
    def multidict_to_dict(cls, multidict):
        pass

    @classmethod
    def construct_from_dict(cls, cstruct, **kwargs):
        pass

    @classmethod
    def generate_id(cls):
        return str(uuid4())

class RootFactory(object):
    __acl__ = [(Allow, Everyone, ('read')),
               (Allow, 'registered', ('create', 'update', 'delete',
                                      'vote', 'comment')),
               (Deny, Everyone, ('create', 'update', 'delete', 'vote')),
               (Allow, 'admins', ALL_PERMISSIONS)]

    def __init__(self, request):
        pass  # pragma: no cover